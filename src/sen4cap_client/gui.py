#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from importlib import import_module

from cuiman.gui import Client

# Force pre-configuration of Sen4CAP configuration
import_module("sen4cap_client.api")

__all__ = [
    "Client",
]
