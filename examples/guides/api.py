"""Run the API guide examples against a configured Sen4CAP service.

Use --help for the inspect, submit, and results commands. Importing this module
does not connect to a service or submit a processing job.
"""

from contextlib import closing
from pathlib import Path
from typing import Annotated

# --8<-- [start:imports]
import typer
from gavicore.models import JobStatus, ProcessRequest

from sen4cap_client.api import create_client

# --8<-- [end:imports]


# --8<-- [start:inspect]
def inspect_process(client, process_id):
    processes = client.get_processes()
    print(processes.model_dump_json(indent=2))

    process = client.get_process(process_id=process_id)
    print(process.model_dump_json(indent=2))
    return process


# --8<-- [end:inspect]


# --8<-- [start:submit]
def submit_process(client, process_id, request_path):
    request = ProcessRequest.model_validate_json(
        request_path.read_text(encoding="utf-8")
    )
    job = client.execute_process(process_id=process_id, request=request)
    print(job.model_dump_json(indent=2))
    return job.jobID


# --8<-- [end:submit]


# --8<-- [start:results]
def inspect_results(client, job_id):
    job = client.get_job(job_id=job_id)
    print(job.model_dump_json(indent=2))
    if job.status != JobStatus.successful:
        print("Results are available only after the job is successful.")
        return None

    results = client.get_job_results(job_id=job_id)
    print(results.model_dump_json(indent=2))
    return results


# --8<-- [end:results]


# --8<-- [start:plot]
def plot_result(client, job_id, asset_name="SNDVI"):
    import matplotlib.pyplot as plt

    data_array = client.open_job_result(job_id=job_id, asset_name=asset_name)
    try:
        data_array.isel(band=0).plot.imshow(figsize=(10, 6), vmin=0, vmax=1000)
        plt.show()
    finally:
        data_array.close()


# --8<-- [end:plot]


cli = typer.Typer(help=__doc__, add_completion=False, no_args_is_help=True)


@cli.command("inspect")
def inspect_command(process_id: str):
    """List available processes and describe the selected process."""
    with closing(create_client()) as client:
        inspect_process(client, process_id)


@cli.command("submit")
def submit_command(
    process_id: str,
    request_path: Annotated[
        Path, typer.Argument(exists=True, dir_okay=False, readable=True)
    ],
):
    """Submit one processing job using a JSON request file."""
    with closing(create_client()) as client:
        submit_process(client, process_id, request_path)


@cli.command("results")
def results_command(
    job_id: str,
    plot: Annotated[
        bool, typer.Option("--plot", help="Plot the selected asset.")
    ] = False,
    asset: Annotated[str, typer.Option(help="Asset to plot.")] = "SNDVI",
):
    """Inspect a job and its results, optionally plotting a raster asset."""
    with closing(create_client()) as client:
        if inspect_results(client, job_id) is not None and plot:
            plot_result(client, job_id, asset)


if __name__ == "__main__":
    cli()
