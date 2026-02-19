# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # simple status
    imageversion = dev.status("imageversion")
    print(f"imageversion: {imageversion}")

    # status with parameters
    ping = dev.status("ping4", "127.0.0.1", "3")
    print(f"ping: {ping}")

    # event log: last 100 lines, filtered by "audispd" (audit events)
    audit_log = dev.status("eventlog", "100", "audispd")
    print(f"\n--- Audit events (last 100 lines) ---\n{audit_log}")

    dev.logout()