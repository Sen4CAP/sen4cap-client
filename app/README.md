# Standalone Sen4CAP Processes app

This folder packages the Eozilla App frontend as a standalone Sen4CAP
Processes app. The finished bundle in `app/dist` includes the frontend,
Sen4CAP branding, and a runtime `config.json` that points to the Sen4CAP service.
Users open the app in a browser and sign in with their own Sen4CAP credentials.

## 1. Create a fresh Eozilla App build

Start in the `sen4cap-client` repository root in a shell. Use an Eozilla App
checkout that includes runtime configuration and the first-visit sign-in fix,
with its `npm` dependencies installed.

```shell
cd path/to/your/projects
git clone https://github.com/eo-tools/eozilla-app.git
cd eozilla-app
npx vite build --outDir ../sen4cap-client/app/build/eozilla --emptyOutDir
```

`--emptyOutDir` clears the generated build directory before Vite writes the 
new files.

## 2. Brand the build for Sen4CAP

Return to `sen4cap-client` and run the packaging script. If `app/dist` already
exists, move it aside first so the script can create a fresh output directory.

```bash
cd ../sen4cap-client
node app/prepare.mjs
```

The script copies the production build, adds the Sen4CAP branding, runtime
configuration, and licenses, and prints `Static app assembled at` followed by
the absolute path to `app/dist`.

## 3. Serve and test the branded app

From the `sen4cap-client` root, start a local server in the Pixi environment:

```bash
pixi shell
python -u -m http.server 4173 --bind 127.0.0.1 --directory ./app/dist
```

Open [http://127.0.0.1:4173/](http://127.0.0.1:4173/) in a private browser window
to test first sign-in with a fresh session. Press Ctrl+C to stop the server.

## Deploy the bundle

For handoff, archive the contents of `app/dist` as `sen4cap-app.zip`. Extract
the archive on an HTTPS static host. If you host the app under a subdirectory,
open its URL with a trailing slash. Serve `config.json` as JSON alongside
`index.html`. The host and browser users need no Python installation.

The default configuration uses the endpoints from `Sen4CAPConfig` in
`src/sen4cap_client/api.py`. The app posts credentials to
`https://sen4x.tao.c-s.ro/auth/login` and sends the returned token in
`X-Auth-Token` on requests to `https://sen4x.tao.c-s.ro/process/`.
The public runtime file contains connection and branding settings. Enter
credentials in the browser.

For a different Sen4CAP deployment, edit the `service` settings in the
deployed `config.json`. The login and Processes endpoints must allow the
app's hosting origin, and the API must allow the token header and request
methods the app uses.

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
