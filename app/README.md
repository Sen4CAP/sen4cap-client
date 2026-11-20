# Standalone Sen4CAP Processes app

Extract `sen4cap-app.zip` and serve its contents from an HTTPS static host. Open
the app URL with a trailing slash if it is hosted in a subdirectory. The package
includes `index.html`, the Eozilla assets, Sen4CAP branding, and the runtime
`config.json`. Users can open it in a browser and sign in with their own
Sen4CAP credentials. The static host and users need no Python installation.

The app uses the endpoints from `Sen4CAPConfig` in `src/sen4cap_client/api.py`.
It posts the user's credentials to `https://sen4x.tao.c-s.ro/auth/login` and
sends the returned token in `X-Auth-Token` on requests to
`https://sen4x.tao.c-s.ro/process/`. The runtime file is public and contains
only connection and branding settings. Enter credentials through the browser.

If the client uses a different Sen4CAP deployment, edit the `service` settings
in the deployed `config.json`. The login and Processes endpoints must permit the
final hosting origin. The API must allow the token header and the methods used
by the app. Serve `config.json` as JSON alongside `index.html`.

## Test sign-in locally

From the Sen4CAP repository root, run this in PowerShell using the project's
Pixi environment:

```powershell
.\.pixi\envs\default\python.exe -u -m http.server 4173 --bind 127.0.0.1 --directory .\app\dist
```

Open [http://127.0.0.1:4173/](http://127.0.0.1:4173/) in a private browser window
to test first sign-in with a fresh session. Press Ctrl+C in PowerShell to stop
the server.

## Findings

The previous local Eozilla build treated the configured service as an active
session on first visit. It attempted to create the service before prompting
for credentials and showed “Please provide a username.” Runtime configuration
now opens the prefilled sign-in form when there is no matching saved session.

The current form still shows editable service and authentication settings.
The proposal to use those settings from `config.json` and show only the
username and password fields and a **Sign in** button is tracked in
[Eozilla App #118 — Improve stand-alone mode](https://github.com/eo-tools/eozilla-app/issues/118).

A browser test served the bundle under a subdirectory and verified the
branding, prefilled login form, login request, and token header on the process
list request. It used a mock service and checked that changing the login URL
returns the user to a fresh sign-in form without reusing credentials.

Both live endpoints accepted CORS preflights from a test origin on November 20,
2026. The Processes endpoint allowed `X-Auth-Token`. Confirm these responses
from the final hosting origin and use a Sen4CAP test account for a live sign-in.

## Prepare a new bundle

Build Eozilla App with the runtime configuration and first-visit startup fix.
With the standard sibling checkouts, run these commands from the Eozilla App
checkout after installing its dependencies.

```sh
npm run typecheck
npx vite build --outDir ../../sen4cap-client/app/build/eozilla
```

Then run `node app/prepare.mjs` from the Sen4CAP repository root. It assembles
`app/dist` using this folder's `config.json` and the Sen4CAP branding assets.
You can pass the build directory and a fresh output directory as the first two
arguments. For a nonstandard checkout, pass the Eozilla MIT license file as the
third argument. Archive the contents of the output directory for handoff.
