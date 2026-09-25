# Command-line interface

The `sen4cap-client` command discovers processes, submits execution requests, and
manages jobs. Start with [configuration and login](configuration.md).

```bash
sen4cap-client --help
sen4cap-client execute-process --help
```

Help describes the options available in your installed version. Abbreviations
such as `lp` for `list-processes` and `vr` for `validate-request` are supported.

## Commands

| Command | Purpose |
| --- | --- |
| `configure` | Save public service and authentication settings. |
| `login` | Obtain/reuse credentials and save them in the OS keyring. |
| `logout` | Remove locally stored credentials for the profile. |
| `list-processes` | List available processes. |
| `get-process PROCESS_ID` | Inspect process inputs and outputs. |
| `create-request PROCESS_ID` | Create a request template from a process description. |
| `validate-request` | Validate the execution-request structure locally. |
| `execute-process` | Submit a request and return a job. |
| `list-jobs` | List jobs. |
| `get-job JOB_ID` | Inspect a job. |
| `get-job-results JOB_ID` | Retrieve output values/links for a successful job. |
| `dismiss-job JOB_ID` | Cancel a running job or delete a finished job. |
| `show-app` | Open the GUI in a browser; Ctrl+C stops its server. |
| `generate-client` | Generate service-specific Python client functions. |

## Example workflow

Replace `218` with a process ID from your service and edit the generated template
to match its inputs before submitting it:

```bash
sen4cap-client list-processes
sen4cap-client get-process 218
sen4cap-client create-request 218 --format json
```

Save the printed template as UTF-8 `request.json`, then edit its inputs before
continuing. Windows PowerShell 5.1 output redirection creates UTF-16 by default,
so do not use plain `>` there.

```bash
sen4cap-client validate-request --request request.json
sen4cap-client execute-process --request request.json
```

Local validation checks the request model; it does not verify input values
against the remote process schema. See [request format](request-format.md).

Copy the `jobID` returned by execution into the following commands, replacing
`JOB_ID`. The results command does not wait for processing to finish or download
the raster:

```bash
sen4cap-client get-job JOB_ID
sen4cap-client get-job-results JOB_ID
```

Use Python's `open_job_result()` to wait for completion and open a raster.

## Options and exit status

Global options go before the command: `--version`, `--traceback` (alias `--tb`),
`--install-completion`, `--show-completion`, and `--help`.
Command-specific options go after the command. Service commands accept
`--config PATH` (`-c`); data commands generally accept `--format` (`-f`),
with YAML as the default. For example:

```bash
sen4cap-client --traceback list-processes --config ./sen4cap.yaml --format json
```

Normal completion returns `0`. Configuration/authentication failures generally
return `1`; remote API errors return `2`; transport errors return `3`.
CLI argument parsing errors can also return `2`. `--traceback` lets API/transport
exceptions propagate with a traceback (normally exit `1`); it does not change
successful commands or argument-parsing errors to exit `1`.
