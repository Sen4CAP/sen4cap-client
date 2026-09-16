"""Optional App interaction from an IPython session at the repository root.

Run with `%run -i examples/guides/notebook_app.py` in Jupyter, then use
`set_dates_and_area(app)` after opening process 218 in the App.
"""

# --8<-- [start:notebook]
from examples.guides.app import open_app, set_dates_and_area  # noqa: F401

if __name__ == "__main__":
    client, app = open_app(display="notebook")
# --8<-- [end:notebook]
