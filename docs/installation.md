# Getting Started

## Installation

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

Start with the [Python API](guides/api.md), [command-line](guides/cli.md), or
[App](guides/app.md) guide. The development environment also includes JupyterLab
for exploring the original examples in the `notebooks` folder:

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
