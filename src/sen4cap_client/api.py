#  Copyright (c) 2025-2026 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from pathlib import Path
from typing import Any

from cuiman.api import AsyncClient, Client, ClientConfig
from cuiman.api.auth import LoginAuthConfig
from pydantic_settings import SettingsConfigDict

from .opener import Sen4CAPJobResultsOpener


class Sen4CAPConfig(ClientConfig):
    model_config = SettingsConfigDict(
        env_prefix="SEN4CAP_",
        env_file=".env",
        extra="allow",  # ClientConfig uses "forbid"
    )


Sen4CAPConfig.register_job_result_opener(Sen4CAPJobResultsOpener)

ClientConfig.default_path = Path("~").expanduser() / ".sen4cap-client"
ClientConfig.default_config = Sen4CAPConfig(
    api_url="http://localhost:8080/process/",
    auth=LoginAuthConfig(
        login_url="http://localhost:8080/auth/login",
        access_token_header="X-Auth-Token",
    ),
)


def create_client(**config: Any) -> Client:
    """Create a synchronous Sen4CAP client from given configuration.

    Provided configuration values, if any, override Sen4CAP default
    values or values read from persistent configuration that were
    previously written by the CLI command `sen4cap-client configure`.

    Args:
        config: Configuration overrides. See
            https://eo-tools.github.io/eozilla/cuiman/configuration/
            for details.
    Returns:
        An instance of a synchronous cuiman client for Sen4CAP. See
        https://eo-tools.github.io/eozilla/cuiman/ for details.
    """
    return Client(**config)


def create_async_client(**config: Any) -> AsyncClient:
    """Create an asynchronous Sen4CAP client from given configuration.

    Provided configuration values, if any, override Sen4CAP default
    values or values read from persistent configuration that were
    previously written by the CLI command `sen4cap-client configure`.

    Args:
        config: Configuration overrides. See
            https://eo-tools.github.io/eozilla/cuiman/configuration/
            for details.
    Returns:
        An instance of an asynchronous cuiman client for Sen4CAP. See
        https://eo-tools.github.io/eozilla/cuiman/ for details.
    """
    return AsyncClient(**config)


__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "create_client",
    "create_async_client",
]
