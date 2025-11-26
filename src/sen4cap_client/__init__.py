#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from importlib.metadata import version

from pydantic_settings import SettingsConfigDict

from cuiman.api import AsyncClient, Client, ClientConfig, ClientError
from cuiman.api.auth import AuthType

from .defaults import DEFAULT_API_URL


__version__ = version("sen4cap-client")

__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "ClientError",
    "__version__",
]

# TODO: remove this note before PR
# IMPORTANT NOTE: changes here require Eozilla branch
# https://github.com/eo-tools/eozilla/tree/forman-26-client_auth


class Sen4CAPConfig(ClientConfig):
    model_config = SettingsConfigDict(
        env_prefix="SEN4CAP_",
        extra="forbid",
    )


ClientConfig.set_default(
    Sen4CAPConfig(
        api_url=DEFAULT_API_URL,
        auth_url=DEFAULT_AUTH_URL,
        auth_type=AuthType.LOGIN,
    )
)
