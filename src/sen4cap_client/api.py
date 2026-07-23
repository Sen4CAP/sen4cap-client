#  Copyright (c) 2025-2026 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from pathlib import Path
from typing import Any

from cuiman.api import AsyncClient, Client, ClientConfig
from cuiman.api.auth import AuthConfig, login
from pydantic_settings import SettingsConfigDict

from .opener import Sen4CAPJobResultsOpener


class Sen4CAPConfig(ClientConfig):
    model_config = SettingsConfigDict(
        env_prefix="SEN4CAP_",
        env_file=".env",
        extra="allow",  # ClientConfig uses "forbid"
    )


_CONFIG_BASE = Sen4CAPConfig(
    api_url="http://localhost:8080/process/",
    auth_url="http://localhost:8080/auth/login",
    auth_type="login",
    token_header="X-Auth-Token",
    use_bearer=False,
)
_DEBUG = False

Sen4CAPConfig.register_job_result_opener(Sen4CAPJobResultsOpener)

ClientConfig.default_path = Path("~").expanduser() / ".sen4cap-client"
ClientConfig.default_config = _CONFIG_BASE


def _create_config(**config_overrides: Any) -> ClientConfig:
    """
    Create the S2GOS-specific configuration instance
    from given configuration overrides.
    """
    # ClientConfig.create() will ready any previous configuration from
    # ~/.sen4cap-client written by command "sen4cap-client configure":
    config = ClientConfig.create(**config_overrides)
    if config.auth_type != "login":
        # already logged in
        return config

    # Login to get an (initial) access token and change auth_type to "token":
    token = login(config)
    config_dict = config.to_dict()
    config_dict.update(auth_type="token", token=token)
    return Sen4CAPConfig(**config_dict)


def create_client(**config: Any) -> Client:
    """Create a synchronous Sen4CAP client from given configuration.

    Provided configuration values, if any, override values
    read from persistent configuration that were previously
    written by the CLI command `sen4cap-client configure`.

    Args:
        config: Configuration overrides. See
            https://eo-tools.github.io/eozilla/cuiman/configuration/
            for details.
    Returns:
        An instance of a synchronous cuiman client for Sen4CAP. See
        https://eo-tools.github.io/eozilla/cuiman/ for details.
    """
    return Client(config=_create_config(**config), _debug=_DEBUG)


def create_async_client(**config: Any) -> AsyncClient:
    """Create an asynchronous Sen4CAP client from given configuration.

    Provided configuration values, if any, override values
    read from persistent configuration that were previously
    written by the CLI command `sen4cap-client configure`.

    Args:
        config: Configuration overrides. See
            https://eo-tools.github.io/eozilla/cuiman/configuration/
            for details.
    Returns:
        An instance of an asynchronous cuiman client for Sen4CAP. See
        https://eo-tools.github.io/eozilla/cuiman/ for details.
    """
    return AsyncClient(config=_create_config(**config), _debug=_DEBUG)


__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "create_client",
    "create_async_client",
]
