# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # --- read existing rulesets ---
    arp_ruleset = dev.table_get("services", "name", "ARP")
    print(f"ARP ruleset: {arp_ruleset}")

    arp_rules = dev.table_get("serv_Protocols", "service_id", "1")
    print(f"ARP rules: {arp_rules}")

    active = dev.table_get("selected_services", "serv_id", "1")
    print(f"ARP activation: {active}")

    # --- create a custom L3 ruleset ---
    cfg = dev.sess_start()
    dev.table_insert("services", cfg, [
        "",                  # id (auto-assigned)
        "HTTPS_Allow",       # name
        "Allow HTTPS from LAN",  # description
        "2",                 # layer_id: L3 (iptables)
        "0",                 # def_serv: custom ruleset
        "*",                 # src_interf_name: any
        "*",                 # des_interf_name: any
        ""                   # fac_def_pos: not a factory default
    ])
    dev.sess_commit(cfg)

    # query the auto-assigned ID
    ruleset = dev.table_get("services", "name", "HTTPS_Allow")
    service_id = ruleset["id"]
    print(f"Created ruleset HTTPS_Allow with id={service_id}")

    # --- add a rule: allow TCP to port 443 from 192.168.1.0/24 ---
    cfg = dev.sess_start()
    dev.table_insert("serv_Protocols", cfg, [
        "",                  # id (auto-assigned)
        service_id,          # service_id
        "TCP",               # protocol
        "1",                 # action_id: ACCEPT
        "0",                 # log_active
        "0",                 # alarm_active
        "Allow_HTTPS",       # description
        "",                  # icmp_type (not ICMP)
        "",                  # icmp_rej_type
        "",                  # limitpack (no rate limit)
        "1",                 # position
        "",                  # src_mac_add (L3, not used)
        "192.168.1.0",       # src_ip_add
        "255.255.255.0",     # src_netmask
        "",                  # src_port (any)
        "",                  # des_mac_add (L3, not used)
        "*",                 # des_ip_add (any destination)
        "*",                 # des_netmask
        "443",               # des_port
        "",                  # prot_hex (L3, not used)
        "",                  # prot_transport (L3, not used)
        "1",                 # state_type_id: conntrack
        "",                  # nat_ip (reserved)
        "",                  # nat_port (reserved)
        "NEW,ESTABLISHED",   # states
        "",                  # statevalue (L3, not used)
        "1",                 # revert: auto-reverse conntrack
        "0",                 # hide
        "0",                 # sigcheck_vpn
        "0",                 # sig_vpn
        "0",                 # sigcheck_cut
        "0",                 # sig_cut
        "0",                 # sigcheck_vpnup
        "0",                 # sig_vpnup
        "0"                  # audit_active
    ])
    dev.sess_commit(cfg)
    print("Added rule Allow_HTTPS")

    # --- activate the ruleset ---
    cfg = dev.sess_start()
    dev.table_insert("selected_services", cfg, [
        "",                  # id (auto-assigned)
        service_id,          # serv_id
        "",                  # days (all days)
        "0",                 # time_active (no time restriction)
        "",                  # time_start
        "",                  # time_stop
        "10"                 # position
    ])
    dev.sess_commit(cfg)
    print("Activated ruleset HTTPS_Allow at position 10")

    # --- modify the rule ---
    cfg = dev.sess_start()
    dev.table_up("serv_Protocols", cfg,
        condition={"description": "Allow_HTTPS"},
        values={"des_port": "8443", "log_active": "1"}
    )
    dev.sess_commit(cfg)
    print("Modified rule: port 443 -> 8443, logging enabled")

    # --- delete the ruleset (order matters: deactivate, rules, ruleset) ---
    cfg = dev.sess_start()
    dev.table_del("selected_services", cfg, condition={"serv_id": service_id})
    dev.table_del("serv_Protocols", cfg, condition={"service_id": service_id})
    dev.table_del("services", cfg, condition={"name": "HTTPS_Allow"})
    dev.sess_commit(cfg)
    print("Deleted ruleset HTTPS_Allow")

    dev.logout()
