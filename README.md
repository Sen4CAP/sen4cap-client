# ESA Sen4CAP Client

[![CI](https://github.com/Sen4CAP/sen4cap-client/actions/workflows/ci.yml/badge.svg)](https://github.com/Sen4CAP/sen4cap-client/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/Sen4CAP/sen4cap-client/graph/badge.svg?token=T3EXHBMD0G)](https://codecov.io/gh/Sen4CAP/sen4cap-client)
[![Pixi](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![License](https://img.shields.io/github/license/Sen4CAP/sen4cap-client)](https://github.com/Sen4CAP/sen4cap-client)


Python client for the processing service of the [ESA Sen4CAP project](https://www.esa-sen4cap.org/)

![logo.png](docs/assets/logo.png)

---

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

```bash
pixi add sen4cap-client
```

### Using GitHub

To install and use the `sen4cap-client` package from its sources
on GitHub you'll need to install both `git` and `pixi` first.

Then:

```bash
git clone https://github.com/eo-tools/sen4cap-client.git
cd sen4cap-client
pixi install
pixi shell
sen4cap-client --help
```

## Getting started

After installing the `sen4cap-client` package in your Python environment
you'll need to configure it first. Open a shell with your Python environment
activated (conda/mamba: `conda activate <your-env>`, pixi: `pixi shell`).

Get an overview of the available commands and options:

```bash
sen4cap-client --help
```

Configure the CLI, which will also serve as default configuration for the API and CUI:

```bash
sen4cap-client configure
```

List the available processes of the Sen4CAP processing service:

```bash
sen4cap-client list-processes
```

