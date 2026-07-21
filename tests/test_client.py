import json
from contextlib import closing
from pathlib import Path

import pytest
from gavicore.models import ProcessDescription

from sen4cap_client.api import Client, create_client


def create_test_client() -> tuple[Client | None, str]:
    credentials_file = Path(__file__).parent.parent / "notebooks" / "credentials.json"

    try:
        credentials = json.loads(credentials_file.read_text())
        return create_client(**credentials), ""
    except Exception as error:
        return None, str(error)


_client, _skip_reason = create_test_client()


@pytest.mark.skipif(_client is None, reason=_skip_reason)
def test_sen4cap_processing():
    assert _client is not None

    with closing(_client):
        process_description = _client.get_process("218")

    assert isinstance(process_description, ProcessDescription)
