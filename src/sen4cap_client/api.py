#  Copyright (c) 2025-2026 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from pathlib import Path
from typing import Any

from cuiman.api import AsyncClient, Client, ClientConfig
from cuiman.api.auth import AuthConfig, LoginAuthConfig
from pydantic import HttpUrl
from pydantic_settings import SettingsConfigDict

from .opener import Sen4CAPJobResultsOpener


class Sen4CAPConfig(ClientConfig):
    model_config = SettingsConfigDict(
        env_prefix="SEN4CAP_",
        env_file=".env",
        extra="allow",  # ClientConfig uses "forbid"
    )

    cli_name = "sen4cap-client"
    display_name = "Sen4CAP Client"

    default_path = Path("~").expanduser() / ".sen4cap-client"

    api_url: str | None = "https://sen4x.tao.c-s.ro/process"
    auth: AuthConfig = LoginAuthConfig(
        login_url=HttpUrl("https://sen4x.tao.c-s.ro/auth/login"),
        access_token_header="X-Auth-Token",
    )

    extra_job_result_openers = [Sen4CAPJobResultsOpener]


def create_client(**config: Any) -> Client:
    """Create a synchronous Sen4CAP client from given configuration.

    Uses the Sen4CAP profile, environment namespace, and result opener.
    Explicit settings override environment variables and the saved profile
    written by `sen4cap-client configure`. Authentication fields belong in
    the nested `auth` mapping. Call `login()` explicitly if interactive
    authentication is needed, and `close()` when finished.

    Args:
        config: Client options such as `api_url`, `auth`, and `config_path`.
            The default profile is `~/.sen4cap-client`. See
            https://eo-tools.github.io/eozilla/cuiman/configuration/
            for details.
    Returns:
        An instance of a synchronous cuiman client for Sen4CAP. See
        https://eo-tools.github.io/eozilla/cuiman/ for details.
    """
    return Client(config_type=Sen4CAPConfig, **config)


def create_async_client(**config: Any) -> AsyncClient:
    """Create an asynchronous Sen4CAP client from given configuration.

    Uses the same Sen4CAP settings and result opener as `create_client()`.
    Authentication fields belong in the nested `auth` mapping. Await service
    calls, `login()`, and `close()`; client construction is synchronous.

    Args:
        config: Client options such as `api_url`, `auth`, and `config_path`.
            The default profile is `~/.sen4cap-client`. See
            https://eo-tools.github.io/eozilla/cuiman/configuration/
            for details.
    Returns:
        An instance of an asynchronous cuiman client for Sen4CAP. See
        https://eo-tools.github.io/eozilla/cuiman/ for details.
    """
    return AsyncClient(config_type=Sen4CAPConfig, **config)


__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "create_client",
    "create_async_client",
]
