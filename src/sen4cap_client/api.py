#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from pathlib import Path

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


def create_config(username: str, password: str) -> ClientConfig:
    auth_config = AuthConfig(
        auth_url=_CONFIG_BASE.auth_url,
        auth_type="login",
        username=username,
        password=password,
    )
    token = login(auth_config)
    config_dict = _CONFIG_BASE.model_dump()
    config_dict.update(
        auth_type="token",
        token=token,
    )
    return Sen4CAPConfig(**config_dict)


def create_client(username: str, password: str) -> Client:
    return Client(config=create_config(username, password), _debug=_DEBUG)


def create_async_client(username: str, password: str) -> AsyncClient:
    return AsyncClient(config=create_config(username, password), _debug=_DEBUG)


__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "Sen4CAPConfig",
    "create_client",
    "create_async_client",
]
