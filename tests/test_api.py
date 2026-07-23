#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from unittest.mock import Mock, patch

import sen4cap_client.api


def test_api_exports_ok():
    assert {
        "AsyncClient",
        "Client",
        "ClientConfig",
        "create_client",
        "create_async_client",
    }.issubset(dir(sen4cap_client.api))


def test_create_client():
    config = Mock(auth_type="token")

    with (
        patch.object(
            sen4cap_client.api.ClientConfig, "create", return_value=config
        ) as create_config,
        patch.object(sen4cap_client.api, "Client") as client_type,
    ):
        client = sen4cap_client.api.create_client(api_url="https://example.test")

    create_config.assert_called_once_with(api_url="https://example.test")
    client_type.assert_called_once_with(config=config, _debug=False)
    assert client is client_type.return_value


def test_create_async_client():
    config = Mock(auth_type="token")

    with (
        patch.object(
            sen4cap_client.api.ClientConfig, "create", return_value=config
        ) as create_config,
        patch.object(sen4cap_client.api, "AsyncClient") as client_type,
    ):
        client = sen4cap_client.api.create_async_client(api_url="https://example.test")

    create_config.assert_called_once_with(api_url="https://example.test")
    client_type.assert_called_once_with(config=config, _debug=False)
    assert client is client_type.return_value
