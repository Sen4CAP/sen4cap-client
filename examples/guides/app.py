"""Launch the App using the saved Sen4CAP configuration.

Run this file to open a browser, or call open_app(display="notebook") from
Jupyter. Close the returned client and stop app.serve_result when finished.
"""

import time

# --8<-- [start:open]
from sen4cap_client.api import create_client


def open_app(display="browser"):
    client = create_client()
    try:
        app = client.show_app(display=display, height=640)
    except Exception:
        client.close()
        raise
    return client, app


# --8<-- [end:open]


# --8<-- [start:request]
def set_dates_and_area(app, process_id="218"):
    request = app.process_requests[process_id]
    request.inputs["c30145a7-029c-4499-98bc-9903ca46531c"] = "2024-06-03"
    request.inputs["472efeab-514a-4e15-9dba-d5812d653065"] = "2024-06-11"
    request.inputs["bed1920e-51c0-406e-b22e-70d1f86d95d4"] = (
        "POLYGON ((9.66 53.75,10.38 53.75,10.38 53.35,9.66 53.35,9.66 53.75))"
    )


# --8<-- [end:request]


def main():
    client, app = open_app()
    print("App is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # --8<-- [start:close]
        app.serve_result.stop()
        client.close()
        # --8<-- [end:close]


if __name__ == "__main__":
    main()
