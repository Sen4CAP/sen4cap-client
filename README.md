# ESA Sen4CAP Client

[![CI](https://github.com/Sen4CAP/sen4cap-client/actions/workflows/ci.yml/badge.svg)](https://github.com/Sen4CAP/sen4cap-client/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/Sen4CAP/sen4cap-client/graph/badge.svg?token=T3EXHBMD0G)](https://codecov.io/gh/Sen4CAP/sen4cap-client)
[![Pixi](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![License](https://img.shields.io/github/license/Sen4CAP/sen4cap-client)](https://github.com/Sen4CAP/sen4cap-client)


Python client for the processing service of the [ESA Sen4CAP project](https://www.esa-sen4cap.org/)

![logo.png](docs/assets/logo.png)

---

See the [documentation](https://Sen4CAP.github.io/sen4cap-client/) for guides and reference material.

## Installation

Requires Python **3.11 or newer**. This checkout targets Cuiman 0.3.1+ and
Gavicore 0.3.0+; older packaged releases may expose a different API.

### Using pip

The `sen4cap-client` package is available on PyPI, and can be
installed with `pip`:

```bash
pip install sen4cap-client
```

### Using conda/mamba 

The `sen4cap-client` package is available on conda-forge and can be
installed using `mamba` or `conda`. To install into an existing,
activated conda environment:

```bash
mamba install --channel conda-forge sen4cap-client
```

To create and activate a new environment containing `sen4cap-client`:

```bash
mamba create --channel conda-forge --name sen4cap-client sen4cap-client
mamba activate sen4cap-client
```

### Using pixi

You can use the pixi package manager to install the conda-forge package:

```bash
mkdir sen4cap-test
cd sen4cap-test

pixi init
pixi add python
pixi add sen4cap-client
pixi shell
```

Pixi can also install the PyPI package:

```bash
mkdir sen4cap-test
cd sen4cap-test

pixi init
pixi add python
pixi add --pypi sen4cap-client
pixi shell
```

### Using GitHub

To install and use the `sen4cap-client` package from its sources on GitHub you'll 
need to install both [git](https://git-scm.com/install/) and 
[pixi](https://pixi.sh/latest/installation/) first. Then:

```bash
git clone https://github.com/Sen4CAP/sen4cap-client.git
cd sen4cap-client
pixi install
pixi shell
```

Start with the [Python API](docs/guides/api.md), [CLI](docs/guides/cli.md), or
[App](docs/guides/app.md) guide. Their runnable examples live in `examples/guides/`.
The development environment also includes JupyterLab for the independent
notebooks in `notebooks/`.

```bash
cd notebooks
jupyter-lab
```

## Getting started

After installing the `sen4cap-client` package in your Python environment
and activating it (conda/mamba: `conda activate <your-env>`, pixi: `pixi shell`)
make sure the `sen4cap-client` command-line tool is accessible: Type

```bash
sen4cap-client --help
```

to get an overview of the available commands and options. The first step is to 
configure the client, which will also serve as default configuration for the client's 
Python API and its GUI:

```bash
sen4cap-client configure
sen4cap-client login
```

The built-in defaults point to the default Sen4CAP processing service: the
processing API is `/process/` and the login endpoint is `/auth/login`. Use the
URLs supplied by your administrator for another deployment. Configuration saves
public settings in `~/.sen4cap-client`; login saves credentials in the OS keyring.
Existing profiles and environment settings override the defaults. If you log in
during configuration, the separate login command is optional.

List the available processes of the Sen4CAP processing service:

```bash
sen4cap-client list-processes
```

## Python API

Use the Sen4CAP factories so that Python shares the CLI's configuration and
registers the Sen4CAP STAC result opener:

```python
from contextlib import closing

from sen4cap_client.api import create_client

with closing(create_client()) as client:
    print(client.get_processes())
```

Use `create_async_client()` for asynchronous calls and `await client.close()`
when finished. Authentication overrides are nested, for example
`create_client(auth={"auth_type": "none"})` for an unauthenticated service.
See [configuration](docs/configuration.md), the [Python API](docs/api.md), and
[CLI guide](docs/cli.md) for details.

## Development

Install the `sen4cap-client` as described in [Installation / Using GitHub](#using-github) 
above.

### Linting and Testing

To run all checks, execute

```bash
pixi run checks
```

To run all tests, execute

```bash
pixi run tests
```

Build and preview the Markdown documentation with `pixi run docs-build` and
`pixi run docs-serve`. Builds include the shared examples without executing them
and do not copy the independent notebooks.

To generate a coverage report, execute

```bash
pixi run coverage
```

### Implementing Enhancements

The `sen4cap-client` code relies heavily on the 
[Eozilla](https://eo-tools.github.io/eozilla/) packages 

* [cuiman](https://github.com/eo-tools/eozilla/tree/main/cuiman),
  which provides the client implementation, and 
* [gavicore](https://github.com/eo-tools/eozilla/tree/main/gavicore)
  which provides common OGC model classes and basic utilities.  

For changes shared with other Eozilla clients, check out Eozilla beside this
repository, matching the editable paths in `pyproject.toml`:

```bash
cd ..
git clone https://github.com/eo-tools/eozilla.git
cd sen4cap-client
```

The layout is `<projects>/sen4cap-client/` and `<projects>/eozilla/`.
Keep `cuiman` and `gavicore` in the project's `dependencies` list. In
`[tool.pixi.pypi-dependencies]`, comment out their version-based entries and
uncomment only these editable entries:

```toml
cuiman = { path = "../eozilla/cuiman", editable = true }
gavicore = { path = "../eozilla/gavicore", editable = true }
```

Then run `pixi install` and `pixi run tests`. The local packages must satisfy the
project's version requirements. The server packages `wraptile` and `procodile`
are not needed for client development against an existing service.

### Integration tests

After configuring and logging in to a running service:

```bash
pixi run pytest -s scripts/integration_test.py
```

This makes live service calls. The separate `tests/test_client.py` smoke test
requires `notebooks/credentials.json` containing factory configuration overrides
(such as `api_url` and nested `auth`); it is skipped when that file is absent.

### Running the client in a remote VM (Windows 11)

***JupyterLab***

On the remote VM start JupyterLab without opening a browser and listening on all interfaces:

```bash
cd sen4cap-client
pixi shell
jupyter lab --no-browser --ip=0.0.0.0 --port=8888
```

It will print something like `http://127.0.0.1:8888/lab?token=1e751cd...` - keep this running.
On your local desktop machine (e.g., Windows or WSL2) SSH into the VM with port forwarding:

```bash
ssh -L 8888:localhost:8888 user@remote-vm
```

Now open your local browser:

```
http://127.0.0.1:8888/lab?token=1e751cd20cd...
```
