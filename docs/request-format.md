# Process execution requests

Inspect `sen4cap-client get-process PROCESS_ID` or
`client.get_process(process_id)` for the input and output names supported by
your deployment. The following example uses the Sen4CAP NDVI process `218`.

## CLI request files

The CLI accepts JSON or YAML. Save this as `request.json` and adapt the values:

```json
{
  "process_id": "218",
  "inputs": {
    "startdate": "2024-06-01",
    "enddate": "2024-06-07",
    "indicatorname": "NDVI",
    "geom": "POLYGON ((9.66 53.75,10.38 53.75,10.38 53.35,9.66 53.35,9.66 53.75))"
  },
  "outputs": {
    "stacitemsfile": {
      "format": {"mediaType": "application/json"},
      "transmissionMode": "reference"
    }
  }
}
```

```bash
sen4cap-client validate-request --request request.json
sen4cap-client execute-process --request request.json
```

`process_id` can instead be supplied as a positional argument. That argument and
repeated `--input NAME=VALUE` (`-i`) options override matching file values.
Use `--request -` to read from standard input. `--dotpath` interprets dots in input
names as nested object paths; check `execute-process --help` for all options.

`create-request PROCESS_ID` generates a template from the server description.
Review and fill in its inputs. `validate-request` checks the local request model,
not whether a remote processor accepts the specific input values.

## Python requests

Pass a `gavicore.models.ProcessRequest` to `client.execute_process()`. The process
ID is a separate argument and is not part of this model. To reuse a CLI file:

```python
import json
from pathlib import Path

from gavicore.util.request import ExecutionRequest

execution = ExecutionRequest.model_validate(
    json.loads(Path("request.json").read_text(encoding="utf-8"))
)
# client is an instance returned by create_client().
job = client.execute_process(
    process_id=execution.process_id,
    request=execution.to_process_request(),
)
```

The conversion removes CLI-only fields and applies any requested dot-path
nesting. Keep `job.jobID` for status and result calls; output availability depends
on successful completion. See the [Python API guide](api.md).
