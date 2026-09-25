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

Configure and log in to a running Sen4CAP service before running live examples:

```bash
sen4cap-client configure
sen4cap-client login
pixi run pytest -s scripts/integration_test.py
```

The default development environment installs the client dependencies, not an
Eozilla test server. To develop Eozilla alongside the client, follow
[the editable-dependency instructions](installation.md#implementing-enhancements).

See the [Python API](guides/api.md), [App](guides/app.md), and
[command-line](guides/cli.md) guides for client usage and runnable examples.

### Formatting, checks, and tests

```commandline
pixi run format
pixi run checks
```

### Testing & Coverage

```commandline
pixi run tests
pixi run coverage
```

The live-service test in `tests/test_client.py` is skipped without its local
credentials file. Unit tests do not require a running service.

### Documentation

The Sen4CAP-client's documentation is built using the 
[mkdocs](https://www.mkdocs.org/) tool.

With repository root as current working directory:

```bash
pixi run docs-build
pixi run docs-serve
```

#### Editing guides and examples

Maintain the three user guides directly in `docs/guides/`. Python, shell, and
JSON examples live in `examples/guides/`; Markdown includes them using
[PyMdown Snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/).
The notebooks in `notebooks/` remain independent examples. Documentation builds
neither copy nor execute them. Any copies left under `docs/notebooks/` by an
older build are excluded from the site.

To display part of a Python file, surround it with named section comments:

```python
# ;--8<-- [start:example-name]
print("Hello from the example")
# ;--8<-- [end:example-name]
```

Include that section inside a Markdown code fence:

````markdown
```python
;--8<-- "examples/guides/example.py:example-name"
```
````

Use stable section names instead of line numbers. Whole files, such as a JSON
request, can be included without a section suffix. Includes resolve from the
repository root; `check_paths: true` makes missing includes fail the build.
Subsections are dedented for display. Include enough context for a reader to
understand each excerpt, and link to the complete example file.

Format and check Python examples with the existing tools:

```bash
pixi run format
pixi run checks
pixi run pytest tests/test_guide_examples.py
pixi run docs-build
```

`checks` lints the Python example files and verifies their formatting. Type
checking examples is optional and is not enabled by default. The guide tests
run offline with mocked clients; they check submission and job-result handling
without credentials or processing jobs. The documentation test builds the site
and checks local links, anchors, and assets, including snippet-expanded pages. Run the example scripts manually
against a configured service when testing a complete workflow. Shell recipes
are copied section by section, not executed as a batch.

Store screenshots and plots in `docs/assets/guides/`, use descriptive filenames
and alt text, and record their origin in `examples/guides/README.md`. Refresh
images deliberately when the relevant interface or result changes; the build
only copies the committed assets. Review guides in `docs-serve` because GitHub
Markdown previews do not expand Snippets directives.

Keep `docs/cli.md` aligned with CLI changes by checking the installed command's
`--help` output.

### Releasing

Making a GitHub release triggers a workflow which publishes corresponding
packages to PyPI.

## License

The Sen4CAP-client is open source made available under the terms and conditions of the 
[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).
