#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from pathlib import Path
from typing import Annotated, Any, Literal, Optional, TypeAlias

from cuiman.api import AsyncClient, Client, ClientConfig, ClientError
from gavicore.models import InputDescription, ProcessDescription
from gavicore.util.model import extend_model
from pydantic import Field
from pydantic_settings import SettingsConfigDict

UiLevel: TypeAlias = Literal["common", "advanced"]


class InputDescriptionX(InputDescription):
    level: Annotated[
        Optional[UiLevel],
        Field(
            alias="x-uiLevel",
            title="UI level",
            description="Describes the level of this input.",
        ),
    ] = "common"


class ProcessDescriptionX(ProcessDescription):
    inputs: Optional[dict[str, InputDescriptionX]] = None


extend_model(InputDescription, InputDescriptionX)


class Sen4CAPConfig(ClientConfig):
    model_config = SettingsConfigDict(
        env_prefix="SEN4CAP_",
        env_file=".env",
        extra="allow",  # ClientConfig uses "forbid"
    )

    @classmethod
    def accept_input(
        cls,
        process_description: ProcessDescription,
        input_name: str,
        input_description: InputDescription,
        **params: Any,
    ):
        requested_level = params.get("level") or "common"
        input_level = getattr(input_description, "level", "common")
        if input_level == "advanced":
            return requested_level in ("common", "advanced")
        return True


ClientConfig.default_path = Path("~").expanduser() / ".sen4cap-client"
ClientConfig.default_config = Sen4CAPConfig(
    api_url="http://localhost:8080/process/",
    auth_url="http://localhost:8080/auth/login",
    auth_type="login",
    token_header="X-Auth-Token",
    use_bearer=False,
)
ClientConfig.return_type_map[ProcessDescription] = ProcessDescriptionX
ClientConfig.return_type_map[InputDescription] = InputDescriptionX

__all__ = [
    "AsyncClient",
    "Client",
    "ClientConfig",
    "ClientError",
    "Sen4CAPConfig",
]
