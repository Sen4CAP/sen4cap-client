# User guide examples

These files supply the code shown in the handwritten Markdown guides. They are
independent of the notebooks in `notebooks/`.

- `api.py`: API functions and the direct Python calls shown in the guide.
  `example_session()` demonstrates client cleanup, submitting once and checking
  results once; follow the guide interactively to check again after processing.
  Optional `inspect`, `submit`, and `results` subcommands call the same functions.
  Run `python examples/guides/api.py --help` from the repository root.
- `app.py`: browser App launcher and reusable helpers for notebook interaction.
- `notebook_app.py`: launch the App from Jupyter with
  `%run -i examples/guides/notebook_app.py`, using the repository root as the
  working directory.
- `cli.sh`: individual CLI recipes, including commands to run the Python files.
  Copy the section you need. The file exits immediately if run as a shell script.
- `ndvi-request.json`: shared process request used by the API and CLI guides.

Live examples require `sen4cap-client configure`. Process and input identifiers
come from the original process 218 example; adapt them to your service. The
submit command creates a real processing job. Use its returned ID for results.

Run `pixi run format` and `pixi run checks` for Python formatting and linting.
`pixi run pytest tests/test_guide_examples.py` checks the examples offline.
Examples are not executed during a documentation build.

## Static image provenance

- `docs/assets/guides/api/ndvi-result.png`: extracted once, unchanged, from the
  saved PNG output in `notebooks/client-api.ipynb` (plot cell 27). The original
  notebook remains unchanged. This is an illustrative historical result.
- `docs/assets/guides/app/process-inputs.png`: captured September 10, 2026 from
  the App bundled with cuiman 0.2.0.dev1 (UI version 0.1.0, build 3), in light
  mode. The App was connected to a local read-only fixture serving process 218's
  saved description from the API notebook, with the example dates and area
  prefilled and an empty job list. No personal configuration or live jobs were
  used. Map attribution is retained in the image.

Refresh App screenshots using the installed App and representative non-sensitive
process data. Refresh result plots using an intentionally selected completed job.
Commit the replacement image and update this provenance when doing so. MkDocs
only displays these files; it does not regenerate them.
