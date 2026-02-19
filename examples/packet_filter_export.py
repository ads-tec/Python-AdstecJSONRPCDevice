# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import json
import jsonrpcdevice

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # export the entire packet filter configuration (all 3 tables)
    export = dev.call("config", "export_pages", pages=["FILTERCONF"])
    print(json.dumps(export, indent=2))

    dev.logout()
