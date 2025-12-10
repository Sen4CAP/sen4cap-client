#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

from sen4cap_client.api import Client


def test_with_server():
    """
    Server integration test. To run it:

    ```bash
    git clone https://github.com/Sen4CAP/sen4cap-client.git
    cd sen4cap-client
    git clone https://github.com/eo-tools/eozilla.git
    pixi install
    pixi shell
    sen4cap-client configure
    pytest -s scripts/integration_test.py
    ```
    """
    client = Client()

    capabilities = client.get_capabilities()
    assert len(capabilities.links) > 0, "empty capability links"
    print("Capabilities ok")

    conformance = client.get_conformance()
    assert len(conformance.conformsTo) > 0, "empty conformance classes"
    print("Conformance ok")

    process_list = client.get_processes()
    processes = process_list.processes
    assert len(processes) > 0, "empty processes list"
    print("Process list ok")

    warnings = 0
    for process_summary in processes:
        process_id = process_summary.id
        process = client.get_process(process_id=process_id)
        w_prefix = f"Warning: prefix {process_id!r}"
        w = 0
        if not process.title:
            print(f"{w_prefix}: missing title")
            w += 1
        if not process.description:
            print(f"{w_prefix}: missing description")
            w += 1
        if not process.inputs:
            print(f"{w_prefix}: missing inputs")
            w += 1
        else:
            for input_name, input_desc in process.inputs.items():
                if not input_name.isidentifier():
                    print(f"{w_prefix}: input {input_name!r}: inappropriate name")
                #if not hasattr(input_desc, "level"):
                #    print(f"{w_prefix}: input {input_name!r}: missing level")
                if not input_desc.title:
                    print(f"{w_prefix}: input {input_name!r}: missing title")
        if not process.outputs:
            print(f"{w_prefix}: missing outputs")
            w += 1
        if w == 0:
            print(f"Process process {process_id!r} ok")
        warnings += 1
    if not warnings:
        print("Process list ok")

    job_list = client.get_jobs()
    jobs = job_list.jobs
    print("Job list ok")

    for job_info in jobs:
        job_id = job_info.jobID
        job = client.get_job(job_id=job_id)
        print(f"Job {job_id!r} ok")
    print("Jobs ok")
