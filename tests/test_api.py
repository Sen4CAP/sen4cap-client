#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from gavicore.models import InputDescription, ProcessDescription

import sen4cap_client.api


def test_api_exports_ok():
    assert {
        "AsyncClient",
        "Client",
        "ClientConfig",
        "ClientError",
        "Sen4CAPConfig",
    }.issubset(dir(sen4cap_client.api))


def test_process_description_has_level():
    from sen4cap_client.api import InputDescriptionX, ProcessDescriptionX

    process_json = {
        "id": "5",
        "version": "1.0",
        "inputs": {
            "ipath": {
                "schema": {"type": "string"},
                "x-uiLevel": "advanced",
            }
        },
    }
    process_obj = ProcessDescriptionX.model_validate(process_json)
    assert isinstance(process_obj, ProcessDescription)
    assert isinstance(process_obj.inputs, dict)
    input_obj = process_obj.inputs.get("ipath")
    assert isinstance(input_obj, InputDescriptionX)
    assert hasattr(input_obj, "level")
    assert input_obj.level == "advanced"


def test_input_description_has_level():
    input_json = {
        "schema": {"type": "string"},
        "x-uiLevel": "advanced",
    }
    input_obj = InputDescription.model_validate(input_json)
    assert isinstance(input_obj, InputDescription)
    assert hasattr(input_obj, "level")
    assert input_obj.level == "advanced"
    input_json_2 = input_obj.model_dump(
        mode="json",
        by_alias=True,
        exclude_unset=True,
        exclude_defaults=True,
        exclude_none=True,
    )
    assert input_json_2 == input_json

    input_json = {
        "schema": {"type": "string"},
    }
    input_obj = InputDescription.model_validate(input_json)
    assert isinstance(input_obj, InputDescription)
    assert hasattr(input_obj, "level")
    assert input_obj.level == "common"
    input_json_2 = input_obj.model_dump(
        mode="json",
        by_alias=True,
        exclude_unset=True,
        exclude_defaults=True,
        exclude_none=True,
    )
    assert input_json_2 == input_json


def test_input_description_filtering():
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

    config = sen4cap_client.api.Sen4CAPConfig()
    assert config.accept_input(process, "com_input", com_input, level="common") is True
    assert (
        config.accept_input(process, "com_input", com_input, level="advanced") is True
    )
    assert config.accept_input(process, "adv_input", adv_input, level="common") is False
    assert (
        config.accept_input(process, "adv_input", adv_input, level="advanced") is True
    )
