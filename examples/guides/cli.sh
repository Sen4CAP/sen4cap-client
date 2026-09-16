#!/usr/bin/env bash
# Command recipes for the guides. Copy the relevant section into your terminal.
# Do not source or run this entire file: configure is interactive, submit creates
# a job, and dismiss cancels or deletes one.
exit 0

# --8<-- [start:configure]
sen4cap-client --help
sen4cap-client configure
# --8<-- [end:configure]

# --8<-- [start:inspect]
sen4cap-client list-processes
sen4cap-client get-process 218
# --8<-- [end:inspect]

# --8<-- [start:template]
sen4cap-client create-request 218 --format json
# --8<-- [end:template]

# --8<-- [start:validate]
sen4cap-client validate-request 218 --request examples/guides/ndvi-request.json
# --8<-- [end:validate]

# --8<-- [start:submit]
sen4cap-client execute-process 218 --request examples/guides/ndvi-request.json
# --8<-- [end:submit]

# --8<-- [start:jobs]
sen4cap-client list-jobs
sen4cap-client get-job YOUR_JOB_ID
# --8<-- [end:jobs]

# --8<-- [start:results]
sen4cap-client get-job-results YOUR_JOB_ID
# --8<-- [end:results]

# --8<-- [start:dismiss]
sen4cap-client dismiss-job YOUR_JOB_ID
# --8<-- [end:dismiss]

# --8<-- [start:app]
sen4cap-client show-app
# --8<-- [end:app]

# --8<-- [start:api-inspect]
python examples/guides/api.py inspect 218
# --8<-- [end:api-inspect]

# --8<-- [start:api-submit]
python examples/guides/api.py submit 218 examples/guides/ndvi-request.json
# --8<-- [end:api-submit]

# --8<-- [start:api-results]
python examples/guides/api.py results YOUR_JOB_ID
# --8<-- [end:api-results]

# --8<-- [start:api-plot]
python examples/guides/api.py results YOUR_JOB_ID --plot --asset SNDVI
# --8<-- [end:api-plot]

# --8<-- [start:python-app]
python examples/guides/app.py
# --8<-- [end:python-app]
