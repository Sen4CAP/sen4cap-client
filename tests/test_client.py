import json
from pathlib import Path
import pytest
from gavicore.models import ProcessDescription

from sen4cap_client.api import create_client

test_dir = Path(__file__).parent
credentials_file = test_dir / ".." / "notebooks" / "credentials.json"


@pytest.mark.skipif(
    not credentials_file.is_file(),
    reason=f"Not found: {credentials_file}",
)
def test_sen4cap_processing():
    credentials = json.loads(credentials_file.read_text())
    client = create_client(**credentials)
    process_description = client.get_process("218")
    assert isinstance(process_description, ProcessDescription)
    print(process_description)
