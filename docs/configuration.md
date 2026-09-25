# Configuration and authentication

The CLI and both Python factories use `Sen4CAPConfig`. The default profile is
the YAML file `~/.sen4cap-client` (`~` is your home directory).

## Configure and log in

Run these commands in a terminal, including a JupyterLab terminal:

```bash
sen4cap-client configure
sen4cap-client login
sen4cap-client list-processes
```

The built-in defaults point to the default Sen4CAP processing service.
For another deployment, enter the processing API and authentication URLs
supplied by your service administrator:

| Setting | Default                               |
| --- |---------------------------------------|
| `api_url` | `https://your-service.example/process/`           |
| `auth.auth_type` | `login`                               |
| `auth.login_url` | `https://your-service.example/auth/login` |
| `auth.access_token_header` | `X-Auth-Token`                        |

These are defaults for new configurations; an existing profile or environment
setting takes precedence. Access requires credentials for the selected service.
`configure` saves public settings and may offer to log in afterwards. `login` obtains credentials and
stores them in the OS keyring; `logout` removes locally stored credentials for
that profile. If you logged in during configuration, a separate login is optional.

Use `sen4cap-client login --force` to sign in again. For unattended use,
`login --no-input` uses supplied credentials without prompting or opening a
browser. Interactive configuration requires a terminal; notebook shell commands
must supply all required configuration options.

To use another profile, pass `--config` to each command:

```bash
sen4cap-client configure --config ./sen4cap.yaml
sen4cap-client login --config ./sen4cap.yaml
sen4cap-client list-processes --config ./sen4cap.yaml
```

Select the same profile in Python with
`create_client(config_path="./sen4cap.yaml")` or `create_async_client(...)`.
CLI service commands require a saved profile. Python factories can also work
entirely from explicit settings and environment variables.

## Python overrides

Authentication fields belong inside `auth`. A partial override retains the
profile's authentication type and provider settings:

```python
import os

from sen4cap_client.api import create_client

client = create_client(
    api_url="https://your-service.example/process/",
    auth={
        "login_url": "https://your-service.example/auth/login",
        "username": os.environ["SEN4CAP_AUTH__USERNAME"],
        "password": os.environ["SEN4CAP_AUTH__PASSWORD"],
    },
)
try:
    client.login(interactive=False)
    print(client.get_processes())
finally:
    client.close()
```

This example assumes the selected profile uses `login` authentication (the
Sen4CAP default). An `auth` dictionary **with** `auth_type` replaces the whole
authentication configuration; supply its provider settings as well. For example:

```python
client = create_client(auth={"auth_type": "none"})
client.close()
```

Use `none` only for a service that requires no authentication. Other supported
types include `basic`, `token`, `login`, `oauth2`, `oidc`, and `api-key`.
See [Cuiman configuration](https://eo-tools.github.io/eozilla/cuiman/configuration/)
for their fields. Top-level `auth_type`, `username`, or `password` are not the
current authentication interface.

## Environment variables and precedence

Settings use the `SEN4CAP_` prefix and `__` for nested fields. They can be set in
the process environment or in a `.env` file in the working directory:

```dotenv
SEN4CAP_API_URL=https://your-service.example/process/
SEN4CAP_AUTH__LOGIN_URL=https://your-service.example/auth/login
SEN4CAP_AUTH__USERNAME=your-username
SEN4CAP_AUTH__PASSWORD=your-password
```

Keep files containing credentials out of version control. The CLI profile stores
public settings; credentials saved by `login` belong in the OS keyring.

For a freshly created client, explicit keyword overrides take precedence over a
supplied configuration object, then environment variables, `.env`, and the saved
profile. Defaults fill missing fields. Matching keyring credentials can fill
missing secrets after settings resolution. A previously resolved configuration
object is a snapshot and does not reread those sources when reused.

## Updating older setups

Changing the built-in defaults does not rewrite an existing profile. To switch
a profile that still points to localhost or another endpoint to the current
default service, set the URLs explicitly and log in:

```bash
sen4cap-client configure --api-url https://your-service.example/process/ --auth-type login --login-url https://sen4x.tao.c-s.ro/auth/login --access-token-header X-Auth-Token
sen4cap-client login
```

For a custom profile, add `--config PATH` to both commands. Check your `.env` and
`SEN4CAP_` environment variables as well, because they override saved settings.


If an earlier CLI version wrote a Cuiman profile at `~/.eozilla/config`, run
`sen4cap-client configure` and `sen4cap-client login` again to set up the shared
Sen4CAP profile. Stored credentials are associated with the profile path and
service URL, so copying a public profile alone does not transfer its keyring
credentials. Update Python examples using flat authentication fields to the
nested `auth` structure shown above.
