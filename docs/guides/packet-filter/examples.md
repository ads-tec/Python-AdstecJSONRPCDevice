# Examples

All examples use [table operations](../../api-reference/tables.md#table-operations) on the packet filter tables ([`services`](../../api-reference/firewall/tables.md#services-packet-filter-rulesets), [`serv_Protocols`](../../api-reference/firewall/tables.md#serv_protocols-packet-filter-rules), [`selected_services`](../../api-reference/firewall/tables.md#selected_services-active-packet-filter-rulesets)). See the [Table Reference](tables.md) for full column schemas.

## Exporting the Entire Packet Filter

Use `config.export_pages` with page ID `FILTERCONF` to export all three tables and related config variables in one call. The output format is compatible with `config.import_config`.

```python
import json
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

export = dev.call("config", "export_pages", pages=["FILTERCONF"])
print(json.dumps(export, indent=2))

dev.logout()
```

## Importing a Complete Filter Configuration

Use `config.import_config` to apply an entire packet filter configuration in one atomic call. This is the counterpart to `export_pages` — useful for deploying a known-good configuration to multiple devices.

!!! warning "Flush all three tables before insert to keep foreign keys consistent"
    Use `tableflush` on all three tables (`selected_services`, `serv_Protocols`, `services`) before re-inserting. This ensures a clean state where all foreign key references (`serv_id`, `service_id`) match the actual IDs in the inserted data. The factory default rulesets are automatically re-created by the system after flushing `services`.

The example below rebuilds the entire packet filter from scratch: it flushes all three tables, re-inserts the factory default rulesets and rules, adds a custom L3 ruleset that drops and logs TCP port 80, and activates everything.

```python
import json
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

filter_config = {
    "tableflush": [
        {"tablename": "selected_services"},
        {"tablename": "serv_Protocols"},
        {"tablename": "services"}
    ],
    "tableinsert": [
        {
            "tablename": "services",
            "data": [
                # Factory default rulesets
                {"id": "1", "name": "ARP", "description": "ARP address resolution",
                 "layer_id": "1", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": "1"},
                {"id": "2", "name": "ICMP_L2",
                 "description": "Allow all Layer 2 ICMP packets",
                 "layer_id": "1", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": ""},
                {"id": "3", "name": "ICMP_L3",
                 "description": "Allow all Layer 3 ICMP packets",
                 "layer_id": "2", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": ""},
                {"id": "4", "name": "Allow_L2",
                 "description": "Allow all L2 traffic",
                 "layer_id": "1", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": "2"},
                {"id": "5", "name": "Allow_L3",
                 "description": "Allow all L3 traffic",
                 "layer_id": "2", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": "3"},
                {"id": "6", "name": "Block_L2",
                 "description": "Block all L2 traffic",
                 "layer_id": "1", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": ""},
                {"id": "7", "name": "Block_L3",
                 "description": "Block all L3 traffic",
                 "layer_id": "2", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": ""},
                {"id": "8", "name": "Log_L2",
                 "description": "Log and block all packets.",
                 "layer_id": "1", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": ""},
                {"id": "999", "name": "Log_L3",
                 "description": "Log and block all packets.",
                 "layer_id": "2", "def_serv": "1",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": ""},
                # Custom ruleset
                {"id": "1000", "name": "FATT_Block_TCP80",
                 "description": "Drop and Log TCP Port 80",
                 "layer_id": "2", "def_serv": "0",
                 "src_interf_name": "*", "des_interf_name": "*", "fac_def_pos": ""}
            ]
        },
        {
            "tablename": "serv_Protocols",
            "data": [
                # Factory default rules
                {"id": "1", "service_id": "1", "protocol": "ARP",
                 "action_id": "1", "log_active": "0", "alarm_active": "0",
                 "description": "allow_all_arp", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "*", "src_ip_add": "", "src_netmask": "",
                 "src_port": "", "des_mac_add": "*", "des_ip_add": "",
                 "des_netmask": "", "des_port": "",
                 "prot_hex": "10", "prot_transport": "", "state_type_id": "",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "2", "service_id": "2", "protocol": "IPV4",
                 "action_id": "1", "log_active": "0", "alarm_active": "0",
                 "description": "any_ICMP_type", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "*", "src_ip_add": "*", "src_netmask": "*",
                 "src_port": "", "des_mac_add": "*", "des_ip_add": "*",
                 "des_netmask": "*", "des_port": "",
                 "prot_hex": "", "prot_transport": "1", "state_type_id": "",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "3", "service_id": "3", "protocol": "ICMP",
                 "action_id": "1", "log_active": "0", "alarm_active": "0",
                 "description": "ICMP_L3", "icmp_type": "any", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "", "src_ip_add": "*", "src_netmask": "*",
                 "src_port": "", "des_mac_add": "", "des_ip_add": "*",
                 "des_netmask": "*", "des_port": "",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "1",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "4", "service_id": "4", "protocol": "*",
                 "action_id": "1", "log_active": "0", "alarm_active": "0",
                 "description": "allow_all", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "*", "src_ip_add": "", "src_netmask": "",
                 "src_port": "", "des_mac_add": "*", "des_ip_add": "",
                 "des_netmask": "", "des_port": "",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "5", "service_id": "5", "protocol": "*",
                 "action_id": "1", "log_active": "0", "alarm_active": "0",
                 "description": "allow_all", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "", "src_ip_add": "*", "src_netmask": "*",
                 "src_port": "", "des_mac_add": "", "des_ip_add": "*",
                 "des_netmask": "*", "des_port": "",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "1",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "6", "service_id": "6", "protocol": "*",
                 "action_id": "2", "log_active": "0", "alarm_active": "0",
                 "description": "drop_all", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "*", "src_ip_add": "", "src_netmask": "",
                 "src_port": "", "des_mac_add": "*", "des_ip_add": "",
                 "des_netmask": "", "des_port": "",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "7", "service_id": "7", "protocol": "*",
                 "action_id": "2", "log_active": "0", "alarm_active": "0",
                 "description": "drop_all", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "", "src_ip_add": "*", "src_netmask": "*",
                 "src_port": "", "des_mac_add": "", "des_ip_add": "*",
                 "des_netmask": "*", "des_port": "",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "1",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "8", "service_id": "8", "protocol": "*",
                 "action_id": "2", "log_active": "1", "alarm_active": "0",
                 "description": "Log", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "*", "src_ip_add": "", "src_netmask": "",
                 "src_port": "", "des_mac_add": "*", "des_ip_add": "",
                 "des_netmask": "", "des_port": "",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                {"id": "9", "service_id": "999", "protocol": "*",
                 "action_id": "2", "log_active": "1", "alarm_active": "0",
                 "description": "Log", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "", "src_ip_add": "*", "src_netmask": "*",
                 "src_port": "", "des_mac_add": "", "des_ip_add": "*",
                 "des_netmask": "*", "des_port": "",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "1",
                 "nat_ip": "", "nat_port": "", "states": "", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "", "sig_vpn": "",
                 "sigcheck_cut": "", "sig_cut": "",
                 "sigcheck_vpnup": "", "sig_vpnup": "", "audit_active": "0"},
                # Custom forward rule
                {"id": "1000", "service_id": "1000", "protocol": "TCP",
                 "action_id": "2", "log_active": "1", "alarm_active": "1",
                 "description": "drop80", "icmp_type": "", "icmp_rej_type": "",
                 "limitpack": "", "position": "1",
                 "src_mac_add": "", "src_ip_add": "*", "src_netmask": "255.255.255.255",
                 "src_port": "*", "des_mac_add": "", "des_ip_add": "*",
                 "des_netmask": "255.255.255.255", "des_port": "80",
                 "prot_hex": "", "prot_transport": "", "state_type_id": "1",
                 "nat_ip": "", "nat_port": "",
                 "states": "NEW,RELATED,ESTABLISHED", "statevalue": "",
                 "revert": "", "hide": "",
                 "sigcheck_vpn": "0", "sig_vpn": "0",
                 "sigcheck_cut": "1", "sig_cut": "1",
                 "sigcheck_vpnup": "0", "sig_vpnup": "0",
                 "audit_active": "1"}
            ]
        },
        {
            "tablename": "selected_services",
            "data": [
                # Activate factory defaults
                {"id": "1", "serv_id": "1", "days": "", "time_active": "0",
                 "time_start": "", "time_stop": "", "position": "1"},     # ARP
                {"id": "2", "serv_id": "4", "days": "", "time_active": "0",
                 "time_start": "", "time_stop": "", "position": "2"},     # Allow_L2
                {"id": "3", "serv_id": "5", "days": "", "time_active": "0",
                 "time_start": "", "time_stop": "", "position": "2"},     # Allow_L3
                # Activate custom ruleset
                {"id": "4", "serv_id": "1000", "days": "", "time_active": "0",
                 "time_start": "", "time_stop": "", "position": "1"}
            ]
        }
    ]
}

dev.call("config", "import_config", jsondata=filter_config)
print("Packet filter configuration imported successfully")

# Reload both L3 and L2 filters to apply changes
import time
trigger = str(int(time.time()))
dev.config_set_commit({"l3_forward": trigger, "l2_forward": trigger})

dev.logout()
```

!!! tip "Export → edit → import workflow"
    A practical workflow is to export the current configuration with `export_pages`, modify the JSON, then apply it with `import_config`. Add `tableflush` entries for any tables where you need to replace (not just append) rows.

## Reading Existing Rulesets

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Get the ARP ruleset
arp_ruleset = dev.table_get("services", "name", "ARP")
print(arp_ruleset)

# Get all rules in the ARP ruleset (service_id = "1")
arp_rules = dev.table_get("serv_Protocols", "service_id", "1")
print(arp_rules)

# List active rulesets
active = dev.table_get("selected_services", "serv_id", "1")
print(active)

dev.logout()
```

## Creating a Ruleset with an L3 Rule

This example creates an L3 ruleset that allows TCP traffic from `192.168.1.0/24` to port 443, then activates it.

!!! warning "Integer `id` columns require explicit values — `1000`+ for custom entries"
    Tables with an `id` primary key do **not** auto-increment. You must provide a unique non-zero integer for every insert. **Custom entries must use IDs starting at `1000` or higher.** IDs below 1000 are reserved for factory defaults — rules inserted with lower IDs may not appear in the device web UI.

**Step 1 — Create the ruleset:**

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

SERVICE_ID = "1000"      # custom ruleset ID (must not conflict with existing)
RULE_ID = "1000"         # custom rule ID
ACTIVATION_ID = "1000"   # custom activation ID

# Create the ruleset in a config session
cfg = dev.sess_start()
dev.table_insert("services", cfg, [
    SERVICE_ID,          # id (explicit, unique, non-zero)
    "HTTPS_Allow",       # name
    "Allow HTTPS from LAN",  # description
    "2",                 # layer_id: L3 (iptables)
    "0",                 # def_serv: custom ruleset
    "*",                 # src_interf_name: any
    "*",                 # des_interf_name: any
    ""                   # fac_def_pos: not a factory default
])
dev.sess_commit(cfg)
```

**Step 2 — Add a forward rule and its reverse rule:**

!!! tip "Always consider the reverse path"
    For ACCEPT rules, you must handle return traffic. The web UI creates a **pair** of rules: a forward rule matching `NEW,RELATED,ESTABLISHED` and a hidden companion reverse rule matching `RELATED,ESTABLISHED` with `revert="1"` and `hide="1"`. Follow the same pattern when inserting rules via the API.

    DROP rules do not need a reverse rule — there is no return traffic to handle.

```python
REVERSE_RULE_ID = "1001"  # companion reverse rule

# Add an L3 rule: allow TCP to port 443 from 192.168.1.0/24
cfg = dev.sess_start()

# Forward rule
dev.table_insert("serv_Protocols", cfg, [
    RULE_ID,             # id (explicit, unique, >= 1000)
    SERVICE_ID,          # service_id
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
    "255.255.255.255",   # des_netmask
    "443",               # des_port
    "",                  # prot_hex (L3, not used)
    "",                  # prot_transport (L3, not used)
    "1",                 # state_type_id: conntrack
    "",                  # nat_ip (reserved)
    "",                  # nat_port (reserved)
    "NEW,RELATED,ESTABLISHED",  # states
    "",                  # statevalue (L3, not used)
    "",                  # revert: not set on forward rule
    "0",                 # hide
    "0",                 # sigcheck_vpn
    "0",                 # sig_vpn
    "0",                 # sigcheck_cut
    "0",                 # sig_cut
    "0",                 # sigcheck_vpnup
    "0",                 # sig_vpnup
    "0"                  # audit_active
])

# Companion reverse rule (return traffic)
dev.table_insert("serv_Protocols", cfg, [
    REVERSE_RULE_ID,     # id
    SERVICE_ID,          # service_id (same ruleset)
    "TCP",               # protocol
    "1",                 # action_id: ACCEPT
    "0",                 # log_active
    "0",                 # alarm_active
    "",                  # description (empty for reverse rules)
    "",                  # icmp_type
    "",                  # icmp_rej_type
    "",                  # limitpack
    "1",                 # position
    "",                  # src_mac_add
    "*",                 # src_ip_add
    "255.255.255.255",   # src_netmask
    "",                  # src_port
    "",                  # des_mac_add
    "*",                 # des_ip_add
    "255.255.255.255",   # des_netmask
    "",                  # des_port
    "",                  # prot_hex
    "",                  # prot_transport
    "1",                 # state_type_id: conntrack
    "",                  # nat_ip
    "",                  # nat_port
    "RELATED,ESTABLISHED",  # states (return traffic only)
    "",                  # statevalue
    "1",                 # revert: marks this as a reverse rule
    "1",                 # hide: hidden in web UI
    "",                  # sigcheck_vpn (empty for reverse rules)
    "",                  # sig_vpn
    "",                  # sigcheck_cut
    "",                  # sig_cut
    "",                  # sigcheck_vpnup
    "",                  # sig_vpnup
    "0"                  # audit_active
])

dev.sess_commit(cfg)
```

**Step 3 — Activate the ruleset:**

```python
cfg = dev.sess_start()
dev.table_insert("selected_services", cfg, [
    ACTIVATION_ID,       # id (explicit, unique, non-zero)
    SERVICE_ID,          # serv_id
    "",                  # days (all days)
    "0",                 # time_active (no time restriction)
    "",                  # time_start
    "",                  # time_stop
    "10"                 # position
])
dev.sess_commit(cfg)
```

**Step 4 — Reload the packet filter:**

```python
import time
dev.config_set_commit({"l3_forward": str(int(time.time()))})

dev.logout()
```

!!! note
    Without the `l3_forward` trigger, table changes are stored but the running filter is not updated. See [Applying Changes](index.md#applying-changes).

## Modifying a Rule

Update specific fields of an existing rule using `table_up`:

```python
cfg = dev.sess_start()
dev.table_up("serv_Protocols", cfg,
    condition={"description": "Allow_HTTPS"},
    values={"des_port": "8443", "log_active": "1"}
)
dev.sess_commit(cfg)

# Reload the filter to apply changes
dev.config_set_commit({"l3_forward": str(int(time.time()))})
```

## Deleting a Rule

Delete a rule and its companion reverse rule (if any). Reverse rules have `revert="1"` and the same `service_id`/`position`:

```python
cfg = dev.sess_start()
# Delete the forward rule
dev.table_del("serv_Protocols", cfg,
    condition={"description": "Allow_HTTPS"}
)
# Delete the companion reverse rule (revert="1", same service_id)
dev.table_del("serv_Protocols", cfg,
    condition={"id": "1001"}
)
dev.sess_commit(cfg)

# Reload the filter to apply changes
dev.config_set_commit({"l3_forward": str(int(time.time()))})
```

## Deleting a Ruleset

!!! warning "Deletion order matters"
    Always delete in this order: deactivate the ruleset, delete its rules, then delete the ruleset itself. Deleting a ruleset while it still has rules or is still active may leave orphaned data.

```python
ruleset = dev.table_get("services", "name", "HTTPS_Allow")
service_id = ruleset["id"]

cfg = dev.sess_start()

# 1. Deactivate: remove from selected_services
dev.table_del("selected_services", cfg,
    condition={"serv_id": service_id}
)

# 2. Delete all rules in the ruleset
dev.table_del("serv_Protocols", cfg,
    condition={"service_id": service_id}
)

# 3. Delete the ruleset itself
dev.table_del("services", cfg,
    condition={"name": "HTTPS_Allow"}
)

dev.sess_commit(cfg)

# Reload the filter to apply changes
dev.config_set_commit({"l3_forward": str(int(time.time()))})
```

## Using IP Groups

Reference entries from the [`ipgroups`](../../api-reference/firewall/tables.md#ipgroups-network-groups) table using the `@groupname` syntax in address fields:

```python
# First, create the IP group
cfg = dev.sess_start()
dev.table_insert("ipgroups", cfg, ["office", "192.168.1.0/24"])
dev.table_insert("ipgroups", cfg, ["office", "10.0.0.0/8"])
dev.sess_commit(cfg)

# Then reference it in a rule's src_ip_add field
cfg = dev.sess_start()
dev.table_insert("serv_Protocols", cfg, [
    "1002",              # id (explicit, unique, >= 1000)
    service_id,          # service_id
    "TCP",               # protocol
    "1",                 # action_id: ACCEPT
    "0", "0",            # log_active, alarm_active
    "Office_HTTPS",      # description
    "", "",              # icmp_type, icmp_rej_type
    "",                  # limitpack
    "1",                 # position
    "",                  # src_mac_add
    "@office",           # src_ip_add: reference IP group
    "",                  # src_netmask (ignored with groups)
    "",                  # src_port
    "",                  # des_mac_add
    "*", "255.255.255.255",  # des_ip_add, des_netmask
    "443",               # des_port
    "", "",              # prot_hex, prot_transport
    "1",                 # state_type_id
    "", "",              # nat_ip, nat_port
    "NEW,RELATED,ESTABLISHED",  # states
    "",                  # statevalue
    "",                  # revert (not set on forward rule)
    "0",                 # hide
    "0", "0",            # sigcheck_vpn, sig_vpn
    "0", "0",            # sigcheck_cut, sig_cut
    "0", "0",            # sigcheck_vpnup, sig_vpnup
    "0"                  # audit_active
])
dev.sess_commit(cfg)
```

## Time-Based Scheduling

Restrict a ruleset to business hours on weekdays:

```python
cfg = dev.sess_start()
dev.table_insert("selected_services", cfg, [
    "1001",                      # id (explicit, unique, non-zero)
    service_id,                  # serv_id
    "Mon,Tue,Wed,Thu,Fri",       # days
    "1",                         # time_active: enabled
    "08:00",                     # time_start
    "17:00",                     # time_stop
    "10"                         # position
])
dev.sess_commit(cfg)
```

---

## Monitoring Packet Filter Counters

The [`datacollection`](../../api-reference/jsonrpc-methods.md#datacollection-traffic-statistics) API provides real-time byte counters for every active packet filter rule. This is essential for verifying that rules are matching traffic as expected — confirming that packets are being accepted, dropped, or rejected by the correct rules.

### How Metric Names Map to Rules

When a ruleset is activated, the device creates iptables/ebtables chains and tracks byte counts per rule. These counters are exposed as `datacollection` metrics with the following naming pattern:

| Pattern | Example | Description |
|---|---|---|
| `filter.rule._{ruleset}.{action}.{index}.bcnt` | `filter.rule._Allow_L3.ACCEPT.0.bcnt` | Bytes matched by a rule inside the ruleset's chain |
| `filter.rule.FORWARD._{ruleset}.{index}.bcnt` | `filter.rule.FORWARD._Allow_L3.2.bcnt` | Bytes hitting the jump from FORWARD into the ruleset's chain |
| `filter.policy.FORWARD.DROP.bcnt` | `filter.policy.FORWARD.DROP.bcnt` | Bytes hitting the FORWARD chain's default policy (DROP) |

Note the leading underscore (`_`) before the ruleset name — this is how the device names its internal iptables chains.

!!! tip "Use counters to debug rules"
    If a rule's counter stays at zero while you expect traffic to match, check the rule's position, protocol, and address fields. If the FORWARD DROP policy counter increases instead, traffic is reaching the end of the chain without matching any ACCEPT rule.

### Discovering Available Filter Metrics

List all filter-related metrics on the device:

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

raw = dev.call("datacollection", "get_metrics")
filter_metrics = sorted(
    m for m in raw["result"] if m.startswith("filter.")
)
for m in filter_metrics:
    print(m)

dev.logout()
```

Example output on an IRF3000 with `Allow_L3` and a custom `FATT_Block_TCP80` ruleset active:

```
filter.policy.FORWARD.DROP.bcnt
filter.policy.INPUT.ACCEPT.bcnt
filter.policy.OUTPUT.ACCEPT.bcnt
filter.rule.FORWARD.ACCEPT.0.bcnt
filter.rule.FORWARD._Allow_L3.2.bcnt
filter.rule.FORWARD._FATT_Block_TCP80.3.bcnt
filter.rule._Allow_L3.ACCEPT.0.bcnt
filter.rule._FATT_Block_TCP80.DROP.0.bcnt
```

### Querying Counters for a Specific Ruleset

Query the byte counters of the `Allow_L3` ruleset from the last 10 minutes:

```python
import time
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Find all metrics for Allow_L3
raw = dev.call("datacollection", "get_metrics")
allow_l3_metrics = sorted(
    m for m in raw["result"]
    if "_Allow_L3" in m
)
print(f"Allow_L3 metrics: {allow_l3_metrics}")

# Query the last 10 minutes of data
now = int(time.time())
raw = dev.call("datacollection", "get_values_as_table",
    metrics=allow_l3_metrics,
    **{"from": now - 600, "to": now, "resolution": 1})
data = raw["result"]

for metric, points in data.items():
    non_null = [p for p in points if p["val"] is not None]
    total = sum(p["val"] for p in non_null)
    print(f"{metric}: {len(non_null)} samples, {total:.0f} bytes total")

dev.logout()
```

### Monitoring the Custom Rule from the Import Example

The [import example](#importing-a-complete-filter-configuration) above creates a ruleset `FATT_Block_TCP80` (service ID 1000) that drops and logs TCP port 80 traffic. Once deployed, you can verify it is catching packets:

```python
import time
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# The custom ruleset's metrics
metrics = [
    "filter.rule._FATT_Block_TCP80.DROP.0.bcnt",   # the DROP rule itself
    "filter.rule.FORWARD._FATT_Block_TCP80.3.bcnt", # jump from FORWARD
    "filter.policy.FORWARD.DROP.bcnt"                # default policy
]

now = int(time.time())
raw = dev.call("datacollection", "get_values_as_table",
    metrics=metrics,
    **{"from": now - 600, "to": now, "resolution": 1})
data = raw["result"]

for metric in metrics:
    points = data.get(metric, [])
    non_null = [p for p in points if p["val"] is not None]
    total = sum(p["val"] for p in non_null)
    latest = non_null[-1]["val"] if non_null else 0
    label = metric.replace("filter.rule.", "").replace("filter.policy.", "").replace(".bcnt", "")
    print(f"{label:45s}  total={total:>10.0f} B  latest={latest:>8.0f} B")

dev.logout()
```

Example output when HTTP traffic is being blocked:

```
_FATT_Block_TCP80.DROP.0                        total=     24680 B  latest=     1240 B
FORWARD._FATT_Block_TCP80.3                     total=     24680 B  latest=     1240 B
FORWARD.DROP                                    total=         0 B  latest=        0 B
```

In this output:

- The `DROP.0` counter confirms the rule is matching and dropping TCP port 80 traffic.
- The `FORWARD._FATT_Block_TCP80.3` counter matches — all traffic that enters the ruleset chain hits the rule.
- The `FORWARD.DROP` policy counter is zero — no traffic is falling through to the default policy, which means all forwarded traffic is handled by explicit rules.

### Continuous Monitoring Loop

Poll counters every 10 seconds and print non-zero deltas:

```python
import time
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Collect all filter metrics
raw = dev.call("datacollection", "get_metrics")
filter_metrics = sorted(m for m in raw["result"] if m.startswith("filter."))

prev = {}
print("Monitoring filter counters (Ctrl+C to stop)...\n")

try:
    while True:
        now = int(time.time())
        raw = dev.call("datacollection", "get_values_as_table",
            metrics=filter_metrics,
            **{"from": now - 30, "to": now, "resolution": 1})
        data = raw["result"]

        ts = time.strftime("%H:%M:%S")
        for metric in filter_metrics:
            points = data.get(metric, [])
            # Use the latest non-null value
            current = None
            for p in reversed(points):
                if p["val"] is not None:
                    current = p["val"]
                    break
            if current is None:
                continue

            delta = current - prev.get(metric, current)
            prev[metric] = current

            if delta != 0:
                label = metric.replace("filter.", "")
                print(f"[{ts}] {label:50s} delta={delta:>+10.0f} B")

        time.sleep(10)
except KeyboardInterrupt:
    pass
finally:
    dev.logout()
```

!!! info "Data collection interval"
    The device collects counter data every **10 seconds**. Polling faster than this interval will not produce additional data points. Each value represents the byte count **delta** for that 10-second interval, not an absolute counter.

See also the [`examples/filter_monitor.py`](https://github.com/ads-tec/Python-AdstecJSONRPCDevice/tree/main/examples/filter_monitor.py) script for a ready-to-run version that auto-discovers metrics for a given ruleset.
