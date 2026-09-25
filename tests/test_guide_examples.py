import ast
import json
from pathlib import Path
from unittest.mock import Mock

import pytest
from cuiman.api import Client
from cuiman.app import App
from gavicore.models import JobInfo, ProcessRequest
from remotestate import ServeResult
from typer.testing import CliRunner

from examples.guides import api, app
from scripts.integration_test import _check_server
from sen4cap_client.cli import cli

REQUEST_PATH = Path(__file__).resolve().parents[1] / "examples/guides/ndvi-request.json"


@pytest.mark.parametrize("name", ["client-api.ipynb", "client-gui.ipynb"])
def test_notebook_request_keys_match_shared_example(name):
    root = REQUEST_PATH.parents[2]
    notebook = json.loads((root / "notebooks" / name).read_text(encoding="utf-8"))
    expected = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    requests = []
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        for node in ast.walk(ast.parse("".join(cell["source"]))):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id == "ProcessRequest":
                requests.append(
                    {kw.arg: ast.literal_eval(kw.value) for kw in node.keywords}
                )
            elif (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "set_process_request"
            ):
                requests.append(ast.literal_eval(node.args[1]))
    assert len(requests) == 1
    request = ProcessRequest.model_validate(requests[0])
    assert request.inputs.keys() == expected["inputs"].keys()
    assert request.outputs.keys() == expected["outputs"].keys()


def test_live_check_accepts_uuid_input_names(capsys):
    client = Mock(spec=Client)
    client.get_capabilities.return_value.links = [Mock()]
    client.get_conformance.return_value.conformsTo = ["example-conformance"]
    client.get_processes.return_value.processes = [Mock(id="218")]
    process = client.get_process.return_value
    process.title = "NDVI"
    process.description = "NDVI processing"
    process.inputs = {"c30145a7-029c-4499-98bc-9903ca46531c": Mock(title="Start date")}
    process.outputs = {"result": Mock()}
    client.get_jobs.return_value.jobs = []

    _check_server(client)

    output = capsys.readouterr().out
    assert "Warning:" not in output
    assert "Process list ok" in output


def test_submit_returns_server_job_id_and_validates_request():
    client = Mock(spec=Client)
    client.execute_process.return_value = JobInfo(jobID="new-job-42", status="accepted")

    job_id = api.submit_process(client, "218", REQUEST_PATH)

    assert job_id == "new-job-42"
    request = client.execute_process.call_args.kwargs["request"]
    assert isinstance(request, ProcessRequest)
    assert request.inputs["indicatorname"] == "NDVI"
    assert client.execute_process.call_args.kwargs["process_id"] == "218"


@pytest.mark.parametrize("status", ["accepted", "running", "failed", "dismissed"])
def test_results_are_not_requested_before_success(status):
    client = Mock(spec=Client)
    client.get_job.return_value = JobInfo(jobID="new-job-42", status=status)

    assert api.inspect_results(client, "new-job-42") is None

    client.get_job_results.assert_not_called()


def test_successful_job_uses_requested_id_for_results():
    client = Mock(spec=Client)
    client.get_job.return_value = JobInfo(jobID="new-job-42", status="successful")

    assert (
        api.inspect_results(client, "new-job-42") is client.get_job_results.return_value
    )

    client.get_job_results.assert_called_once_with(job_id="new-job-42")


def test_cli_example_request_validates_without_a_service():
    result = CliRunner().invoke(
        cli, ["validate-request", "218", "--request", str(REQUEST_PATH)]
    )
    assert result.exit_code == 0, result.output


def test_api_command_closes_client_after_request_error(monkeypatch):
    client = Mock(spec=Client)
    client.get_processes.side_effect = RuntimeError("service unavailable")
    monkeypatch.setattr(api, "create_client", lambda: client)
    result = CliRunner().invoke(api.cli, ["inspect", "218"])

    assert result.exit_code == 1
    assert isinstance(result.exception, RuntimeError)
    assert str(result.exception) == "service unavailable"

    client.close.assert_called_once()


def test_app_updates_shared_inputs_without_replacing_outputs():
    client_app = App(App.create_remote_store(), Mock(spec=ServeResult))
    request = ProcessRequest.model_validate_json(
        REQUEST_PATH.read_text(encoding="utf-8")
    )
    client_app.set_process_request("218", request)

    app.set_dates_and_area(client_app)

    updated = client_app.get_process_request("218")
    assert updated.inputs["startdate"] == "2024-06-03"
    assert updated.inputs["enddate"] == "2024-06-11"
    assert updated.inputs["indicatorname"] == "NDVI"
    assert updated.outputs == request.outputs


def test_open_app_passes_notebook_display_and_returns_handles(monkeypatch):
    client = Mock(spec=Client)
    monkeypatch.setattr(app, "create_client", lambda: client)

    assert app.open_app(display="notebook") == (client, client.show_app.return_value)
    client.show_app.assert_called_once_with(display="notebook", height=640)
    client.close.assert_not_called()


@pytest.mark.parametrize("command", [[], ["inspect"], ["submit"], ["results"]])
def test_api_help_does_not_connect(monkeypatch, command):
    create_client = Mock()
    monkeypatch.setattr(api, "create_client", create_client)

    result = CliRunner().invoke(api.cli, [*command, "--help"])

    assert result.exit_code == 0, result.output
    create_client.assert_not_called()


def test_api_submit_command_accepts_request_path(monkeypatch):
    client = Mock(spec=Client)
    client.execute_process.return_value = JobInfo(jobID="new-job-42", status="accepted")
    monkeypatch.setattr(api, "create_client", lambda: client)

    result = CliRunner().invoke(api.cli, ["submit", "218", str(REQUEST_PATH)])

    assert result.exit_code == 0, result.output
    assert "new-job-42" in result.output
    assert isinstance(
        client.execute_process.call_args.kwargs["request"], ProcessRequest
    )
    client.close.assert_called_once()


def test_api_submit_rejects_missing_file_before_connecting(monkeypatch, tmp_path):
    create_client = Mock()
    monkeypatch.setattr(api, "create_client", create_client)

    result = CliRunner().invoke(
        api.cli, ["submit", "218", str(tmp_path / "missing.json")]
    )

    assert result.exit_code == 2, result.output
    create_client.assert_not_called()


@pytest.mark.parametrize("plot", [False, True])
def test_api_results_command_only_plots_when_requested(monkeypatch, plot):
    client = Mock(spec=Client)
    client.get_job.return_value = JobInfo(jobID="new-job-42", status="successful")
    monkeypatch.setattr(api, "create_client", lambda: client)
    plot_result = Mock()
    monkeypatch.setattr(api, "plot_result", plot_result)
    args = ["results", "new-job-42", "--asset", "another-asset"]
    if plot:
        args.append("--plot")

    result = CliRunner().invoke(api.cli, args)

    assert result.exit_code == 0, result.output
    if plot:
        plot_result.assert_called_once_with(client, "new-job-42", "another-asset")
    else:
        plot_result.assert_not_called()
    client.close.assert_called_once()


@pytest.mark.parametrize("status", ["accepted", "successful"])
def test_api_session_reuses_submitted_job_and_closes_client(monkeypatch, status):
    client = Mock(spec=Client)
    client.execute_process.return_value = JobInfo(jobID="new-job-42", status="accepted")
    client.get_job.return_value = JobInfo(jobID="new-job-42", status=status)
    monkeypatch.setattr(api, "create_client", lambda: client)
    monkeypatch.chdir(REQUEST_PATH.parents[2])
    plot_result = Mock()
    monkeypatch.setattr(api, "plot_result", plot_result)

    assert api.example_session() == "new-job-42"

    client.get_process.assert_called_once_with(process_id="218")
    client.execute_process.assert_called_once()
    client.get_job.assert_called_once_with(job_id="new-job-42")
    if status == "successful":
        client.get_job_results.assert_called_once_with(job_id="new-job-42")
        plot_result.assert_called_once_with(client, "new-job-42", asset_name="SNDVI")
    else:
        client.get_job_results.assert_not_called()
        plot_result.assert_not_called()
    client.close.assert_called_once()


def test_api_session_closes_client_after_request_error(monkeypatch):
    client = Mock(spec=Client)
    client.get_processes.side_effect = RuntimeError("service unavailable")
    monkeypatch.setattr(api, "create_client", lambda: client)

    with pytest.raises(RuntimeError, match="service unavailable"):
        api.example_session()

    client.execute_process.assert_not_called()
    client.close.assert_called_once()
