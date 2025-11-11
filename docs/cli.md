# Client CLI Reference

 The `sen4cap-client` command-line interface is used to interact with the 
 ESA Sen4CAP processing service using a terminal window.

 `sen4cap-client` can be used to get the available processes, get process 
 details, execute processes, and manage the jobs originating from the latter. It         
 herewith resembles the core functionality of the OGC API - Processes, Part 1.
 For details see https://ogcapi.ogc.org/processes/.

 You can use shorter command name aliases, e.g., use command name `vr`
 for `validate-request`, or `lp` for `list-processes`.

 The tool's exit codes are as follows:

 * `0` - normal exit
 * `1` - user errors, argument errors
 * `2` - remote API errors 
 * `3` - local network transport errors

 If the `--traceback` flag is set, the original Python exception traceback
 will be shown and the exit code will always be `1`. 
 Otherwise, only the error message is shown. 

╭─ Options ─────────────────────────────────────────────────────────────────────────────╮
│ --version                     Show version and exit.                                  │
│ --traceback,--tb              Show server exception traceback, if any.                │
│ --install-completion          Install completion for the current shell.               │
│ --show-completion             Show completion for the current shell, to copy it or    │
│                               customize the installation.                             │
│ --help                        Show this message and exit.                             │
╰───────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────╮
│ configure          Configure the client tool.                                         │
│ list-processes     List available processes.                                          │
│ get-process        Get process details.                                               │
│ create-request     Create an execution request (template) for a given process.        │
│ validate-request   Validate a process execution request.                              │
│ execute-process    Execute a process in asynchronous mode.                            │
│ list-jobs          List all jobs.                                                     │
│ get-job            Get job details.                                                   │
│ dismiss-job        Cancel a running or delete a finished job.                         │
│ get-job-results    Get job results.                                                   │
╰───────────────────────────────────────────────────────────────────────────────────────╯

