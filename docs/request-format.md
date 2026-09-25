# Process execution requests

Inspect `sen4cap-client get-process PROCESS_ID` or
`client.get_process(process_id)` for the input and output names supported by
your deployment. The following example uses the Sen4CAP NDVI process `218`.

## CLI request files

The CLI accepts JSON or YAML. Save this as a UTF-8 file named `request.json` and adapt the values:

```json
--8<-- "examples/guides/ndvi-request.json"
```

Its UUID keys come from the example service's process description. Use the
actual input/output keys returned by your deployment, even when its labels
say "Start date" or "NDVI". Supply the process ID separately:

```bash
sen4cap-client validate-request 218 --request request.json
sen4cap-client execute-process 218 --request request.json
```

A CLI request file may also include a top-level `"process_id": "218"`; in that
case the positional argument is optional. The positional argument and
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
from gavicore.util.request import ExecutionRequest

execution = ExecutionRequest.create(process_id="218", request_path="request.json")
# client is an instance returned by create_client().
job = client.execute_process(
    process_id=execution.process_id,
    request=execution.to_process_request(),
)
```

The conversion removes CLI-only fields and applies any requested dot-path
nesting. Keep `job.jobID` for status and result calls; output availability depends
on successful completion. See the [Python API guide](api.md).
