#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

import os

import pytest
from cuiman.api.auth import LoginAuthConfig, NoAuthConfig

import sen4cap_client.api
from sen4cap_client.opener import Sen4CAPJobResultsOpener


def test_api_exports_ok():
    assert {
        "AsyncClient",
        "Client",
        "ClientConfig",
        "create_client",
        "create_async_client",
    }.issubset(dir(sen4cap_client.api))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "factory, client_type",
    [
        (sen4cap_client.api.create_client, sen4cap_client.api.Client),
        (sen4cap_client.api.create_async_client, sen4cap_client.api.AsyncClient),
    ],
)
@pytest.mark.parametrize("override_defaults", [False, True])
async def test_create_client(
    factory, client_type, override_defaults, tmp_path, monkeypatch
):
    # Keep local profiles, dotenv files, and environment settings out of this test.
    monkeypatch.chdir(tmp_path)
    for name in os.environ:
        if name.upper().startswith("SEN4CAP_"):
            monkeypatch.delenv(name)
    monkeypatch.setattr(
        sen4cap_client.api.Sen4CAPConfig, "default_path", tmp_path / "config"
    )
    overrides = (
        {"api_url": "https://example.test/process/", "auth": {"auth_type": "none"}}
        if override_defaults
        else {}
    )

    client = factory(**overrides)
    try:
        assert isinstance(client, client_type)
        assert isinstance(client.config, sen4cap_client.api.Sen4CAPConfig)
        assert Sen4CAPJobResultsOpener in (
            client.config.get_job_result_opener_registry().opener_types
        )
        if override_defaults:
            assert client.config.api_url == "https://example.test/process/"
            assert isinstance(client.config.auth, NoAuthConfig)
        else:
            assert client.config.api_url == "https://sen4x.tao.c-s.ro/process"
            assert isinstance(client.config.auth, LoginAuthConfig)
            assert (
                str(client.config.auth.login_url)
                == "https://sen4x.tao.c-s.ro/auth/login"
            )
            assert client.config.auth.access_token_header == "X-Auth-Token"
    finally:
        if isinstance(client, sen4cap_client.api.AsyncClient):
            await client.close()
        else:
            client.close()
