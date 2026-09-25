# Command-line guide

Use `sen4cap-client` in a terminal to inspect processes, submit work, and manage
jobs. Follow the [installation instructions](../installation.md) first.
The same saved configuration is used by the Python API and the App.

The commands below are included from
[cli.sh](https://github.com/Sen4CAP/sen4cap-client/blob/main/examples/guides/cli.sh).
Copy individual sections into your terminal; the file is a collection of recipes
and exits without running them when invoked as a script. Run file-based examples
from the repository root. The commands shown also work in PowerShell; Bash
is not required.

## Configure the client

```bash
--8<-- "examples/guides/cli.sh:configure"
```

The built-in defaults point to the default Sen4CAP processing service.
Accept the defaults, or enter the service URLs supplied for another deployment. 
`configure` saves public settings and may offer to log in.
`login` obtains credentials and saves them in the OS keyring; if you already
logged in during configuration, the separate login command is optional.
See [configuration](../configuration.md) for profiles and authentication options.
Use `--help` after any command to inspect its arguments and options.

## Inspect a process

```bash
--8<-- "examples/guides/cli.sh:inspect"
```

Process `218` is the example used in the [API guide](api.md). If your service
uses different process IDs, select one from `list-processes`. Inspect its input
and output definitions before preparing a request.

## Prepare and validate a request

To start with a template for the selected process:

```bash
--8<-- "examples/guides/cli.sh:template"
```

Copy the printed JSON into a UTF-8 file named `request.json` and edit it;
generated defaults are only a starting point. Saving explicitly as UTF-8 also
avoids [Windows PowerShell 5.1's UTF-16 redirection default](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding).
For process `218`, the repository also provides the
[NDVI example request](api.md#prepare-and-submit-a-request). Validate that request:

```bash
--8<-- "examples/guides/cli.sh:validate"
```

`validate-request` checks the execution request's structure locally. It does not
guarantee that the selected service will accept every process-specific value.
To use your edited template, replace the example path with `request.json` in
the validation and submission commands.

## Submit a job

```bash
--8<-- "examples/guides/cli.sh:submit"
```

The command submits work asynchronously and prints job information. Save the
returned job ID. Replace `YOUR_JOB_ID` in the commands below with that value.

## Monitor and retrieve results

```bash
--8<-- "examples/guides/cli.sh:jobs"
```

Repeat `get-job` while the job is accepted or running. Once its status is
`successful`, retrieve the result references:

```bash
--8<-- "examples/guides/cli.sh:results"
```

Use the [Python API](api.md#open-and-plot-an-asset) to open and plot raster assets.

## Cancel or delete a job

The following command cancels a running job or deletes a finished job. Run it
only for a job you intend to dismiss:

```bash
--8<-- "examples/guides/cli.sh:dismiss"
```

## Open the App

```bash
--8<-- "examples/guides/cli.sh:app"
```

Keep the terminal running while using the App; press Ctrl+C when finished.
See the [App guide](app.md) for the visual workflow and the
[CLI reference](../cli.md) for the full command list.

The [original CLI notebook](https://github.com/Sen4CAP/sen4cap-client/blob/main/notebooks/client-cli.ipynb)
remains available separately.
