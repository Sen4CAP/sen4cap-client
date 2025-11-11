#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from cuiman.cli import new_cli

from sen4cap_client import __version__ as version


cli = new_cli(
    "sen4cap-client",
    summary="Interact with the ESA Sen4CAP processing service.",
    version=version,
)

__all__ = [
    "cli",
]

if __name__ == "__main__":  # pragma: no cover
    cli()
