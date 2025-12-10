#  Copyright (c) 2025 by ESA Sen4CAP team and contributors
#  Permissions are hereby granted under the terms of the Apache 2.0 License:
#  https://opensource.org/license/apache-2-0.

import sen4cap_client.gui


def test_gui_exports_ok():
    assert {"Client"}.issubset(dir(sen4cap_client.gui))
