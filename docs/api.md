# Python API

Use the factories in `sen4cap_client.api`. They select the Sen4CAP configuration,
saved profile, and job-result opener. The re-exported `Client`, `AsyncClient`, and
`ClientConfig` classes are Cuiman classes; constructing `Client()` directly uses
Cuiman's defaults instead.

## Create a client

After [configuring and logging in](configuration.md), you can list processes:

```python
from contextlib import closing

from sen4cap_client.api import create_client

with closing(create_client()) as client:
    processes = client.get_processes()
    for process in processes.processes:
        print(process.id, process.title)
```

The factory accepts `api_url`, `auth`, and `config_path` overrides. See
[configuration](configuration.md) for nested authentication settings and precedence.
Creating a client does not contact the service or prompt for credentials.
Call `client.login()` explicitly when interactive authentication is needed;
ordinary API calls do not prompt. Use `client.login(save=True)` to persist
credentials in the OS keyring for the selected profile.

## Execute a process and open its result

Process IDs, input names, and output names come from the service. Inspect
`client.get_process(process_id)` before building a request. The example below
uses the Sen4CAP NDVI process `218`; adapt it to your deployment.

```python
from contextlib import closing

from gavicore.models import ProcessRequest
from sen4cap_client.api import create_client

with closing(create_client()) as client:
    request = ProcessRequest(
        inputs={
            "startdate": "2024-06-01",
            "enddate": "2024-06-07",
            "indicatorname": "NDVI",
            "geom": "POLYGON ((9.66 53.75,10.38 53.75,10.38 53.35,9.66 53.35,9.66 53.75))",
        },
        outputs={
            "stacitemsfile": {
                "format": {"mediaType": "application/json"},
                "transmissionMode": "reference",
            }
        },
    )
    job = client.execute_process(process_id="218", request=request)
    print(job.jobID, job.status)
    data = client.open_job_result(
        job_id=job.jobID, asset_name="SNDVI", timeout=3600
    )
    try:
        print(data)
    finally:
        data.close()
```

`execute_process()` submits a server-side job and returns a `JobInfo`; it does
not wait for processing to finish. Keep its `jobID` for subsequent calls.
`open_job_result()` polls accepted/running jobs until completion or timeout.
If results contain several outputs, pass `output_name` to select one.

The Sen4CAP opener requires a result link to a STAC item with
`/collections/…/items/…` in its URL and an `asset_name` option. The selected asset
must have `alternate.s3.href`; it is opened with `rioxarray.open_rasterio()`.
For the single-raster NDVI example this returns an `xarray.DataArray`. The STAC
and raster URLs must be accessible independently: this opener does not forward
the processing API's authentication headers. Other output formats may be handled
by Cuiman's built-in openers.

## Asynchronous calls

```python
import asyncio

from sen4cap_client.api import create_async_client

async def main():
    client = create_async_client()
    try:
        processes = await client.get_processes()
        print(processes)
    finally:
        await client.close()

asyncio.run(main())
```

In a notebook use `await main()` instead of `asyncio.run(main())`. Await the
async client's API operations, `login()`, `open_job_result()`, and `close()`.
`show_app()` is a regular method on either client.

## Methods and errors

| Method | Purpose |
| --- | --- |
| `get_capabilities()` / `get_conformance()` | Inspect the service and supported standards. |
| `get_processes()` / `get_process(process_id)` | Discover processes and their input/output schemas. |
| `execute_process(process_id, request)` | Submit a `ProcessRequest`; return a `JobInfo`. |
| `get_jobs()` / `get_job(job_id)` | List jobs or inspect one job's status. |
| `get_job_results(job_id)` | Retrieve output values or links for a successful job. |
| `open_job_result(job_id, **options)` | Wait for completion and open a selected output. |
| `dismiss_job(job_id)` | Cancel a running job or delete a finished job. |
| `show_app()` | Open the GUI and return an app object. |

Models such as `ProcessRequest`, `JobInfo`, and `JobResults` are provided by
`gavicore.models`. Import API errors from `cuiman.api`, for example
`from cuiman.api import ClientError`; they are not exported by `sen4cap_client`.
Result opening can also raise `JobResultOpenError`, `JobResultStatusError`
(from `cuiman.api.opener`), or `TimeoutError`.

For the full inherited API, see [Cuiman](https://eo-tools.github.io/eozilla/cuiman/).
The [API notebook](notebooks/client-api.ipynb) and
[GUI notebook](notebooks/client-gui.ipynb) demonstrate the workflow interactively.

## Sen4CAP factory reference

::: sen4cap_client.api.create_client

::: sen4cap_client.api.create_async_client
