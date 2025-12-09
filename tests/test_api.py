#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from gavicore.models import InputDescription, ProcessDescription


def test_api_ok():
    import sen4cap_client.api

    assert {
        "AsyncClient",
        "Client",
        "ClientConfig",
        "ClientError",
        "Sen4CAPConfig",
    }.issubset(dir(sen4cap_client.api))


def test_ui_input_filtering():
    from sen4cap_client.api import Sen4CAPConfig

    # level = "common" (the default)
    com_input = InputDescription(**{"schema": {"type": "number"}})
    # level = "advanced"
    adv_input = InputDescription(
        **{"schema": {"type": "number"}, "x-uiLevel": "advanced"}
    )

    process = ProcessDescription(
        id="p",
        version="0",
        inputs={
            "com_input": com_input,
            "adv_input": adv_input,
        },
    )

    config = Sen4CAPConfig()
    assert config.accept_input(process, "com_input", com_input, level="common") is True
    assert (
        config.accept_input(process, "com_input", com_input, level="advanced") is True
    )
    assert config.accept_input(process, "adv_input", adv_input, level="common") is False
    assert (
        config.accept_input(process, "adv_input", adv_input, level="advanced") is True
    )
