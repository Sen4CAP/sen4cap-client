#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from pathlib import Path

from cuiman.api import AsyncClient, Client, ClientConfig, ClientError
from pydantic_settings import SettingsConfigDict

# TODO: remove this note before PR
# IMPORTANT NOTE: changes here require Eozilla branch
# https://github.com/eo-tools/eozilla/tree/forman-26-client_auth


class Sen4CAPConfig(ClientConfig):
    model_config = SettingsConfigDict(
        env_prefix="SEN4CAP_",
        env_file=".env",
        extra="allow",  # ClientConfig uses "forbid"
    )


ClientConfig.default_path = Path("~").expanduser() / ".sen4cap-client"
ClientConfig.default_config = Sen4CAPConfig(
    api_url="http://localhost:8080/process/",
    auth_url="http://localhost:8080/auth/login",
    auth_type="login",
    token_header="X-Auth-Token",
    use_bearer=False,
)

__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "ClientError",
    "Sen4CAPConfig",
]
