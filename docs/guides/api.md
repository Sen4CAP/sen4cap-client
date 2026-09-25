# Python API guide

Use the Python API to discover processes, submit requests, monitor jobs, and
open their results. Start with [installation](../installation.md) and
[configuration and login](../configuration.md). The examples below use the
profile saved by `sen4cap-client configure` and credentials saved by
`sen4cap-client login`.

Run the Python blocks below in order in the same Python session or notebook.
Each step defines a small function and then calls it, reusing the same `client`
and the `job_id` returned by submission. Start from the repository root in the
development environment so the example request file can be found.
The functions and calls are maintained in the
[API example](https://github.com/Sen4CAP/sen4cap-client/blob/main/examples/guides/api.py).
The [original notebook](https://github.com/Sen4CAP/sen4cap-client/blob/main/notebooks/client-api.ipynb)
is also available for interactive exploration.

## Create a client

The examples use `create_client()` to load the saved service configuration and
credentials. Construction does not contact the service or prompt for login.
Service calls authenticate using the resolved credentials; call `client.login()`
first if interactive authentication is needed. Explicit keyword arguments can
override configuration values; see the [configuration reference](../configuration.md).
Import the dependencies and create the client:

```python
--8<-- "examples/guides/api.py:imports"

--8<-- "examples/guides/api.py:create-client"
```

## Discover processes

List available processes, then inspect a process's inputs and outputs:

```python
--8<-- "examples/guides/api.py:inspect"
```

Call the function with the client and the process ID:

```python
--8<-- "examples/guides/api.py:inspect-call"
```

This guide uses process `218` and the NDVI request from the original notebook.
Process IDs, input IDs, and available outputs depend on the service. Check its
process description and adapt the request before submitting it.

## Prepare and submit a request

The example request selects dates, NDVI, an area of interest, and an output
returned by reference. It is maintained in
[ndvi-request.json](https://github.com/Sen4CAP/sen4cap-client/blob/main/examples/guides/ndvi-request.json):

```json
--8<-- "examples/guides/ndvi-request.json"
```

Load the JSON as a `ProcessRequest` and submit it. Submission starts a job and
returns its information without waiting for processing to finish. Retain the
returned `jobID` for subsequent calls:

```python
--8<-- "examples/guides/api.py:submit"
```

Call it with the request file's path. Run this call once to create the job:

```python
--8<-- "examples/guides/api.py:submit-call"
```

## Monitor the job and inspect results

Use the `job_id` returned above to inspect the same job. While the job is
accepted or running, repeat the `inspect_results(client, job_id)` call later;
do not repeat the submission call. If it fails or is dismissed, inspect the
job information before submitting another request.

```python
--8<-- "examples/guides/api.py:results"
```

```python
--8<-- "examples/guides/api.py:results-call"
```

`client.get_jobs()` lists jobs. To cancel a running job or delete a finished
one, use `client.dismiss_job(job_id)`; see the [CLI guide](cli.md#cancel-or-delete-a-job)
for the corresponding command.

## Open and plot an asset

For the example process, the output links to a STAC item. Its assets identify
the available data products. `open_job_result()` opens the selected `SNDVI`
asset as an xarray data array. The asset must expose `alternate.s3.href`, and
the STAC and raster URLs must be accessible independently of the processing
API's authentication. Other processes may have different asset names or result
types. For multiple outputs, pass `output_name` to `open_job_result()`.

`open_job_result()` polls accepted/running jobs and can raise `TimeoutError`;
use its `timeout` and `poll_interval` options to control waiting. Failed or
dismissed jobs raise a job-status error. The example below is called after the
job has succeeded.

```python
--8<-- "examples/guides/api.py:plot"
```

Once `inspect_results` returns results, plot the asset for that same job:

```python
--8<-- "examples/guides/api.py:plot-call"
```

Plotting requires Matplotlib, which is included in the development environment.
The image below is a saved result from the original example; a new job's
result can differ.

![NDVI raster plotted for the example area of interest](../assets/guides/api/ndvi-result.png)

## Close the client

When you have finished inspecting and plotting results, close the client:

```python
--8<-- "examples/guides/api.py:close-client"
```

In a script, put the calls in a `try` block and `client.close()` in its `finally`
block so the client is also closed if a request fails. The `example_session()`
function in the source file demonstrates this pattern.

## Optional: run the functions from a terminal

The same source file provides Typer commands that create and close a client and
call the functions introduced above. These are an alternative to the Python
session. Run only the stage you need from the repository root:

| Command | Function called |
| --- | --- |
| `inspect` | `inspect_process` |
| `submit` | `submit_process` |
| `results` | `inspect_results` |
| `results --plot` | `inspect_results`, then `plot_result` if results are ready |

```bash
--8<-- "examples/guides/cli.sh:api-inspect"
```

To submit a new job:

```bash
--8<-- "examples/guides/cli.sh:api-submit"
```

Replace `YOUR_JOB_ID` with the ID printed by submission to inspect that job:

```bash
--8<-- "examples/guides/cli.sh:api-results"
```

Once the job succeeds, inspect and plot its result:

```bash
--8<-- "examples/guides/cli.sh:api-plot"
```

See the [API reference](../api.md) for the client interfaces, or the
[App guide](app.md) to explore processes visually.
