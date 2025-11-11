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

### Testing the Sen4CAP-client

Run local test server

```commandline
wraptile run -- wraptile.services.local.testing:service
```

The dev mode is useful if you are changing server code:

```commandline
wraptile dev wraptile.services.local.testing:service
```

Run client API

```python
from sen4cap_client import Client

client = Client()
client.get_processes()
client.get_jobs()
```

Run client GUI (in Jupyter notebooks)

```python
from sen4cap_client.gui import Client

client = Client()
client.show()
client.show_jobs()
```

Run client CLI

```commandline
$ sen4cap_client --help
```

### Formatting & Linting

```commandline
pixi run isort .
pixi run ruff format 
pixi run ruff check
```

### Testing & Coverage

```commandline
pixi run test
pixi run coverage
```

### Documentation

The Sen4CAP-client's documentation is built using the 
[mkdocs](https://www.mkdocs.org/) tool.

With repository root as current working directory:

```bash
mkdocs build
mkdocs serve
mkdocs gh-deploy
```

After changing the CLI code, always update its documentation `docs/cli.md` 
by running

```bash
pixi run gen-client
```

## License

The Sen4CAP-client is open source made available under the terms and conditions of the 
[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).
