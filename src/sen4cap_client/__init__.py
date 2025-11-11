#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from importlib.metadata import version

from cuiman.api import AsyncClient, Client, ClientConfig, ClientError

from .defaults import DEFAULT_SERVER_URL, DEFAULT_USER_NAME, DEFAULT_ACCESS_TOKEN


__version__ = version("sen4cap-client")

__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "ClientError",
    "__version__",
]

ClientConfig.set_default(
    ClientConfig(
        server_url=DEFAULT_SERVER_URL,
        user_name=DEFAULT_USER_NAME,
        access_token=DEFAULT_ACCESS_TOKEN,
    )
)
