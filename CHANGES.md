## Changes in version 0.2.0 (in development)

- Added client factory functions `create_client()` and `create_async_client()`
  which are now the preferred way to create a Sen4CAP client.
- Added a _job result opener_ so that the client's `open_job_result()` method
  can open the datasets created by processor runs. 
- Changed `notebooks/client-gui.ipynb` to demonstrate the new Eozilla App UI
  which is shown by `client.show_app()`.
- Depend on eozilla 0.2.x packages.
- Update installation instructions. (#30)

## Changes in version 0.1.0

- Depend on eozilla releases, not repository (#15)
- Remove prefix.dev auth credentials from unit test workflow (#13)
- Add workflow for publishing PyPI packages (#16, #20)
