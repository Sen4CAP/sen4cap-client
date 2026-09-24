#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

import os

from typer.testing import CliRunner

import sen4cap_client.cli
from sen4cap_client.api import ClientConfig, Sen4CAPConfig, create_client


def test_cli_exports_ok():
    assert {"cli"}.issubset(dir(sen4cap_client.cli))


def test_cli_uses_sen4cap_profile(tmp_path, monkeypatch):
    profile = tmp_path / "sen4cap-config"
    other_profile = tmp_path / "eozilla-config"
    monkeypatch.setattr(Sen4CAPConfig, "default_path", profile)
    monkeypatch.setattr(ClientConfig, "default_path", other_profile)
    monkeypatch.chdir(tmp_path)
    for name in os.environ:
        if name.upper().startswith("SEN4CAP_"):
            monkeypatch.delenv(name)

    result = CliRunner().invoke(
        sen4cap_client.cli.cli,
        [
            "configure",
            "--api-url",
            "https://example.test/process/",
            "--auth-type",
            "none",
        ],
    )

    assert result.exit_code == 0, result.output
    assert profile.is_file()
    assert not other_profile.exists()
    client = create_client()
    try:
        assert client.config.api_url == "https://example.test/process/"
        assert client.config.auth.auth_type == "none"
    finally:
        client.close()
