# ESA Sen4CAP Client

[![CI](https://github.com/Sen4CAP/sen4cap-client/actions/workflows/ci.yml/badge.svg)](https://github.com/Sen4CAP/sen4cap-client/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/Sen4CAP/sen4cap-client/graph/badge.svg?token=T3EXHBMD0G)](https://codecov.io/gh/Sen4CAP/sen4cap-client)
[![Pixi](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![License](https://img.shields.io/github/license/Sen4CAP/sen4cap-client)](https://github.com/Sen4CAP/sen4cap-client)


Python client for the processing service of the [ESA Sen4CAP project](https://www.esa-sen4cap.org/)

![logo.png](docs/assets/logo.png)

---

_Note, this project and its documentation is still in an early development stage._

## Installation

### Using pip

The `sen4cap-client` package is not yet deployed on PyPI, therefore
installing it as a package using `pip` is not yet available. 

### Using conda/mamba 

The `sen4cap-client` package is not yet deployed on conda-forge, therefore
installing it using as a conda package using `conda` or `mamba` is not yet available. 

### Using pixi

The `sen4cap-client` package is not yet deployed on conda-forge, therefore
installing it as a conda package using `pixi` is not yet available. 

### Using GitHub

To install and use the `sen4cap-client` package from its sources on GitHub you'll 
need to install both [git](https://git-scm.com/install/) and 
[pixi](https://pixi.sh/latest/installation/) first. Then:

```bash
git clone https://github.com/eo-tools/sen4cap-client.git
cd sen4cap-client
pixi install
pixi shell
```

The installed development environment includes also JupyterLab so the recommended
way to get started is to take a look at the notebooks in the `notebooks` folder.

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
```

List the available processes of the Sen4CAP processing service:

```bash
sen4cap-client list-processes
```

## Development

Install the `sen4cap-client` as described in [Installation / Using GitHub](#using-github) 
above.

### Linting and Testing

To run all checks, execute

```commandline
pixi run checks
```

To run all tests, execute

```commandline
pixi run tests
```

To generate a coverage report, execute

```commandline
pixi run coverage
```

### Implementing Enhancements

The `sen4cap-client` code relies heavily on the 
[Eozilla](https://eo-tools.github.io/eozilla/) packages 

* [cuiman](https://github.com/eo-tools/eozilla/tree/main/cuiman),
  which provides the client implementation, and 
* [gavicore](https://github.com/eo-tools/eozilla/tree/main/gavicore)
  which provides common OGC model classes and basic utilities.  

Should `sen4cap-client` require non-Sen4CAP-specific enhancements it 
would likely be best to implement the required changes in the respective 
Eozilla packages. For this, check out the Eozilla sources directly next 
to this project's sources to achieve this folder structure:

```commandline
    <projects>/
    ├── sen4cap-client/
    └── eozilla/
        ├── cuiman/
        ├── gavicore/
        └── ...
```

Then, during development, change `sen4cap-client/pyproject.toml` as follows

1. Comment out the dependencies `cuiman` and `gavicore` in the 
   `[project.dependencies]` table.

2. Uncomment the editable PyPI dependencies for `cuiman` and `gavicore` in 
   the `[tool.pixi.pypi-dependencies]` table.

Then run once more

```commandline
pixi install
```

### Running the client in a remote VM (Windows 11)

***JupyterLab***

On the remote VM

Start JupyterLab without opening a browser and listening on all interfaces:


```commandline
jupyter lab --no-browser --ip=0.0.0.0 --port=8888
```

It will print something like:

```commandline
http://127.0.0.1:8888/lab?token=1e751cd20cd15464f373358e85c940c076298d28a6af9ff6
```

Keep this running.

On your local machine (Windows or WSL2)

SSH into the VM with port forwarding:

```commandline
ssh -L 8888:localhost:8888 user@remote-vm
```

Now open your local browser: `http://localhost:8888`
