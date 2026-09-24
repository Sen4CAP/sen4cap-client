# Contributing to the project

## Changelog

You can find the complete changelog 
[here](https://github.com/Sen4CAP/sen4cap-client/blob/main/CHANGES.md). 

## Reporting

If you have suggestions, ideas, feature requests, or if you have identified
a malfunction or error, then please 
[post an issue](https://github.com/Sen4CAP/sen4cap-client/issues). 

## Contributions

The Sen4CAP project welcomes contributions of any form as long as you 
respect our 
[code of conduct](https://github.com/Sen4CAP/sen4cap-client/blob/main/CODE_OF_CONDUCT.md)
and follow our 
[contribution guide](https://github.com/Sen4CAP/sen4cap-client/blob/main/CONTRIBUTING.md).

If you'd like to submit code or documentation changes, we ask you to provide a 
pull request (PR) 
[here](https://github.com/Sen4CAP/sen4cap-client/pulls). 
For code and configuration changes, your PR must be linked to a 
corresponding issue. 

## Development

### Setup

Before you start, make sure you have [pixi](https://pixi.sh) installed.

Checkout sources

```commandline
git clone https://github.com/Sen4CAP/sen4cap-client.git
cd ./sen4cap-client
```

Create a new Python environment and activate it:

```commandline
pixi install 
pixi shell
```

### Test against a service

Configure the processing API and authentication endpoints for a running service,
then log in. The default client environment does not install the Eozilla server
packages. See [installation](installation.md#implementing-enhancements) if you
need to develop Eozilla alongside the client.

```bash
sen4cap-client configure
sen4cap-client login
sen4cap-client list-processes
pixi run pytest -s scripts/integration_test.py
```

Use the Sen4CAP factory in Python:

```python
from contextlib import closing

from sen4cap_client.api import create_client

with closing(create_client()) as client:
    print(client.get_processes())
    print(client.get_jobs())
```

To open the GUI in a notebook, keep the client alive while using the app:

```python
from sen4cap_client.api import create_client

client = create_client()
client.login()
app = client.show_app()
```

When finished, call `app.serve_result.stop()` and `client.close()`.
The [GUI notebook](notebooks/client-gui.ipynb) demonstrates shared request state.

### Formatting, checks, and tests

```bash
pixi run format
pixi run checks
pixi run tests
pixi run coverage
```

The live-service test in `tests/test_client.py` is skipped without its local
credentials file. Unit tests do not require a running service.

### Documentation

From the repository root:

```bash
pixi run mkdocs build --strict
pixi run mkdocs serve
```

Edit active notebook sources in `notebooks/`; the build copies them into
`docs/notebooks/` and renders them without executing requests. Clear stale
outputs when changing examples. Keep the hand-maintained CLI reference aligned
with `sen4cap-client --help` and each command's `--help`. The Python factory
reference is generated from its docstrings.

### Releasing

Making a GitHub release triggers a workflow which publishes corresponding
packages to PyPI.

## License

The Sen4CAP-client is open source made available under the terms and conditions of the 
[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).
