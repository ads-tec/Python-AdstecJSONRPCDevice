# Table Reference

See also the [Firewall Tables API Reference](../../api-reference/firewall/tables.md) for the table schemas alongside [`ipgroups`](../../api-reference/firewall/tables.md#ipgroups-network-groups) and [`macgroups`](../../api-reference/firewall/tables.md#macgroups-hardware-groups). For table operations (`table_get`, `table_insert`, `table_up`, `table_del`), see [Tables](../../api-reference/tables.md#table-operations).

## `services`

Rulesets group related filter rules. Each ruleset is either Layer 2 (ebtables) or Layer 3 (iptables).

| Index | Column | Type | Constraint | Description |
|---|---|---|---|---|
| 0 | `id` | integer | unique, non-zero | Primary key (no auto-increment); custom rulesets must use `1000`+ |
| 1 | `name` | string | max 32, `[-0-9A-Za-z_]` | Ruleset name |
| 2 | `description` | string | max 255 | Human-readable description |
| 3 | `layer_id` | `"1"` / `"2"` | required | `"1"` = L2 (ebtables), `"2"` = L3 (iptables) |
| 4 | `def_serv` | `"0"` / `"1"` | | `"1"` = factory default (read-only); must be `"0"` or `"1"`, not emptyets |
| 5 | `src_interf_name` | string | | Source interface or `"*"` for any |
| 6 | `des_interf_name` | string | | Destination interface or `"*"` for any |
| 7 | `fac_def_pos` | integer | | Factory default position (leave `""` for custom rulesets) |

### Factory Default Rulesets

The device ships with these pre-configured rulesets (`def_serv="1"`):

| ID | Name | Layer | Description |
|---|---|---|---|
| 1 | `ARP` | L2 | ARP address resolution |
| 2 | `ICMP_L2` | L2 | Allow all Layer 2 ICMP packets |
| 3 | `ICMP_L3` | L3 | Allow all Layer 3 ICMP packets |
| 4 | `Allow_L2` | L2 | Allow all L2 traffic |
| 5 | `Allow_L3` | L3 | Allow all L3 traffic |
| 6 | `Block_L2` | L2 | Block all L2 traffic |
| 7 | `Block_L3` | L3 | Block all L3 traffic |
| 8 | `Log_L2` | L2 | Log and block all packets |
| 999 | `Log_L3` | L3 | Log and block all packets |

By default, only `ARP` (position 1) and `Allow_L2` (position 2) are activated in `selected_services`.

---

## `serv_Protocols`

Individual filter rules within a ruleset. Each rule has 35 columns, grouped here by function.

### Core Columns

| Index | Column | Type | Description |
|---|---|---|---|
| 0 | `id` | integer | Primary key (no auto-increment); custom rules must use `1000`+ |
| 1 | `service_id` | integer | FK to `services.id` |
| 2 | `protocol` | string | Protocol name (`"TCP"`, `"UDP"`, `"ICMP"`, `"*"` for any); prefix `"! "` to negate |
| 3 | `action_id` | `"1"`–`"8"` | Action to take (see [Action IDs](#action-ids)) |
| 4 | `log_active` | `"0"` / `"1"` | `"1"` = log matched packets |
| 5 | `alarm_active` | `"0"` / `"1"` | `"1"` = trigger alarm signal |
| 6 | `description` | string | Rule name (max 32 chars); also used as LOG prefix |
| 7 | `icmp_type` | string | ICMP type (e.g. `"echo-request"`, `"any"`); empty for non-ICMP |
| 8 | `icmp_rej_type` | string | ICMP reject type (e.g. `"port-unreachable"`); only for REJECT action |
| 9 | `limitpack` | integer | Rate limit in packets/second; empty for no limit |
| 10 | `position` | integer | Rule order within ruleset; lowest value first |

### Address Columns

| Index | Column | Type | Description |
|---|---|---|---|
| 11 | `src_mac_add` | string | Source MAC, `"*"`, `"@groupname"`, or `""` (L2 only) |
| 12 | `src_ip_add` | string | Source IP, `"*"`, `"@groupname"`, or `""` |
| 13 | `src_netmask` | string | Source netmask (e.g. `"255.255.255.0"`), `"*"`, or `""` |
| 14 | `src_port` | string | Source port, range (`"80:443"`), `"*"`, or `""` (TCP/UDP only) |
| 15 | `des_mac_add` | string | Destination MAC (L2 only) |
| 16 | `des_ip_add` | string | Destination IP, `"*"`, `"@groupname"`, or `""` |
| 17 | `des_netmask` | string | Destination netmask |
| 18 | `des_port` | string | Destination port or range |

### Behavior Columns

| Index | Column | Type | Description |
|---|---|---|---|
| 19 | `prot_hex` | string | L2 protocol hex (e.g. `"0800"` for IPv4); empty for L3 |
| 20 | `prot_transport` | string | L2 transport protocol number (e.g. `"6"` for TCP); empty for L3 |
| 21 | `state_type_id` | `"1"`–`"4"` / `""` | `"1"`/`"3"` = conntrack; `"2"` = stateless (TCP flags) |
| 22 | `nat_ip` | string | Reserved — must be `""` |
| 23 | `nat_port` | string | Reserved — must be `""` |
| 24 | `states` | string | Conntrack states or TCP flags (depends on `state_type_id`) |
| 25 | `statevalue` | integer | L2 TCP flag bitmask; empty for L3 |
| 26 | `revert` | `"0"` / `"1"` | `"0"` = normal; `"1"` = auto-generate reverse conntrack rule |

### Signal & Visibility Columns

!!! warning "Signal fields must be `\"0\"` or `\"1\"`, never empty"
    All `sigcheck_*`, `sig_*`, and `audit_active` fields must be set to `"0"` or `"1"` explicitly — never left as empty string `""`. Factory default rules use empty strings internally, but the web UI expects all custom rules to have explicit values. Rules with empty signal fields may not display correctly in the web UI.

| Index | Column | Type | Description |
|---|---|---|---|
| 27 | `hide` | `"0"` / `"1"` | `"1"` = suppress ALARM/CUT targets and logging for this rule |
| 28 | `sigcheck_vpn` | `"0"` / `"1"` | `"1"` = apply VPN signal condition; must be `"0"` or `"1"`, not empty |
| 29 | `sig_vpn` | `"0"` / `"1"` | Expected VPN signal value; must be `"0"` or `"1"`, not empty |
| 30 | `sigcheck_cut` | `"0"` / `"1"` | `"1"` = apply CUT signal condition; must be `"0"` or `"1"`, not empty |
| 31 | `sig_cut` | `"0"` / `"1"` | Expected CUT signal value; must be `"0"` or `"1"`, not empty |
| 32 | `sigcheck_vpnup` | `"0"` / `"1"` | `"1"` = apply VPN-up signal condition; must be `"0"` or `"1"`, not empty |
| 33 | `sig_vpnup` | `"0"` / `"1"` | Expected VPN-up signal value; must be `"0"` or `"1"`, not empty |
| 34 | `audit_active` | `"0"` / `"1"` | `"1"` = enable AUDIT target; must be `"0"` or `"1"`, not empty |

### Action IDs

| `action_id` | Name | Description |
|---|---|---|
| `"1"` | ACCEPT | Allow the packet |
| `"2"` | DROP | Silently discard the packet |
| `"5"` | CUT | Drop the packet and activate the CUT signal |
| `"6"` | REJECT | Reject with ICMP response (uses `icmp_rej_type`) |
| `"7"` | INACTIVE | Rule is disabled — generates no iptables rule |
| `"8"` | CUTANDACCEPT | Accept the packet and activate the CUT signal |

!!! info
    Action IDs 3 and 4 do not exist.

---

## `selected_services`

Activates a ruleset and optionally restricts it to a time window.

| Index | Column | Type | Description |
|---|---|---|---|
| 0 | `id` | integer | Primary key (no auto-increment); custom entries must use `1000`+ |
| 1 | `serv_id` | integer | FK to `services.id` |
| 2 | `days` | string | Comma-separated weekdays (e.g. `"Mon,Tue,Wed,Thu,Fri"`) or `""` for all days |
| 3 | `time_active` | `"0"` / `"1"` | `"1"` = enable time restriction |
| 4 | `time_start` | string | Start time `HH:MM` (e.g. `"08:00"`) or `""` |
| 5 | `time_stop` | string | Stop time `HH:MM` (e.g. `"17:00"`) or `""` |
| 6 | `position` | integer | Ruleset evaluation order; lowest value first |

---

## Quick Reference

### Wildcard and Negation Syntax

| Syntax | Applies to | Meaning |
|---|---|---|
| `"*"` | IP, MAC, port, interface | Match any |
| `""` (empty) | IP, MAC, port, netmask | Same as `"*"` (match any) |
| `"! value"` | IP, MAC, protocol, ICMP type | Negation (space after `!` is required) |
| `"@groupname"` | IP, MAC | Reference an `ipgroups` / `macgroups` entry |
| `"! @groupname"` | IP, MAC | Negated group reference |
| `"80:443"` | port | Port range |
| `":1024"` | port | Ports up to 1024 |
| `"1024:"` | port | Ports from 1024 |

### Layer IDs

| `layer_id` | Layer | Backend | Use for |
|---|---|---|---|
| `"1"` | L2 | ebtables | MAC-level filtering, ARP, non-IP protocols |
| `"2"` | L3 | iptables | IP-level filtering, TCP/UDP/ICMP |
