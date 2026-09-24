The build copies active `.ipynb` files from the repository's `notebooks/` folder
into this folder on each `mkdocs serve` or `mkdocs build`, using
`docs/hooks/notebooks_json_output.py`. Edit the original notebooks, not these
generated copies. Local configuration files and `notebooks/deprecated/` are
excluded. The build renders saved notebook contents without running service calls.
