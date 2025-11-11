# Getting Started

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

To install and use the `sen4cap-client` package from its sources
on GitHub you'll need to install both `git` and `pixi` first. Then:

```bash
git clone https://github.com/eo-tools/sen4cap-client.git
cd sen4cap-client
pixi install
pixi shell
```

The installed development environment includes also JuypterLab so the recommended
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

