# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # --- resolve WAN interface name ---
    wan_ifname = dev.config_get(["wan_ifname"])["result"][0]["wan_ifname"]
    print(f"WAN interface: {wan_ifname}")

    # --- add forwarding rules ---
    cfg = dev.sess_start()

    # Rule 1: Forward RDP (TCP 3389) to internal host
    dev.table_insert("forwarding", cfg, [
        wan_ifname,       # fwifname: public interface (Linux name)
        "TCP",            # fwproto: TCP, UDP, or * (both)
        "",               # fwlocalip: empty = any IP on this interface
        "3389",           # fwlocalport: external port
        "192.168.10.200", # fwtargetip: internal host
        "3389",           # fwtargetport: port on internal host
        "disabled",       # fwsnat: no source NAT
        "",               # fwsrcnet: no source restriction
        "RDP access",     # fwcomment
        "enabled",        # fwenabled
        "",               # fwposition
        "disabled",       # fwrsnat
    ])

    # Rule 2: Forward HTTPS to PLC with SNAT (PLC has no default gateway)
    dev.table_insert("forwarding", cfg, [
        wan_ifname,       # fwifname
        "TCP",            # fwproto
        "",               # fwlocalip
        "443",            # fwlocalport
        "192.168.10.100", # fwtargetip
        "443",            # fwtargetport
        "enabled",        # fwsnat: required, PLC has no gateway
        "10.0.0.0/24",    # fwsrcnet: only allow this network
        "PLC HTTPS",      # fwcomment
        "enabled",        # fwenabled
        "",               # fwposition
        "disabled",       # fwrsnat
    ])

    # Rule 3: Port remapping — external 50022 to internal SSH 22
    dev.table_insert("forwarding", cfg, [
        wan_ifname,       # fwifname
        "TCP",            # fwproto
        "",               # fwlocalip
        "50022",          # fwlocalport (external)
        "192.168.10.50",  # fwtargetip
        "22",             # fwtargetport (internal)
        "disabled",       # fwsnat
        "",               # fwsrcnet
        "SSH remapped",   # fwcomment
        "enabled",        # fwenabled
        "",               # fwposition
        "disabled",       # fwrsnat
    ])

    dev.sess_commit(cfg)
    print("Added 3 forwarding rules")

    # --- list all forwarding rules ---
    export = dev.call("config", "export_pages", pages=["FORWARDCONF"])
    print(json.dumps(export, indent=2))

    # --- disable a rule ---
    cfg = dev.sess_start()
    dev.table_up("forwarding", cfg,
        condition={"fwcomment": "SSH remapped"},
        values={"fwenabled": "disabled"}
    )
    dev.sess_commit(cfg)
    print("Disabled SSH remapped rule")

    # --- delete a rule ---
    cfg = dev.sess_start()
    dev.table_del("forwarding", cfg,
        condition={"fwcomment": "SSH remapped"}
    )
    dev.sess_commit(cfg)
    print("Deleted SSH remapped rule")

    dev.logout()
