# Tables (Firewall)

!!! note "Firewall models only"
    The tables on this page are available on IRF1000, IRF2000, and IRF3000 firewalls.

---

## `ipgroups` — Network Groups

Used for grouping IP subnets (e.g., for packet filter rules with `@groupname` syntax).

| Column | Type | Constraint | Description |
|---|---|---|---|
| `name` | string (max 14 chars) | unique with `network` | Name of the network group |
| `network` | IP/mask | unique with `name` | Subnet (e.g., `"192.168.1.0/24"`) |

```python
cfg_session_id = dev.sess_start()
dev.table_insert("ipgroups", cfg_session_id, ["office", "192.168.1.0/24"])
dev.table_insert("ipgroups", cfg_session_id, ["office", "10.0.0.0/8"])
dev.sess_commit(cfg_session_id)
```

---

## `macgroups` — Hardware Groups

Used for grouping devices by MAC address (e.g., for L2 packet filter rules with `@groupname` syntax).

| Column | Type | Constraint | Description |
|---|---|---|---|
| `name` | string (max 14 chars) | unique with `hwaddr` | Name of the hardware group |
| `hwaddr` | MAC address | unique with `name` | Hardware address (e.g., `"00:10:20:45:67:89"`) |

```python
cfg_session_id = dev.sess_start()
dev.table_insert("macgroups", cfg_session_id, ["printers", "00:10:20:45:67:89"])
dev.sess_commit(cfg_session_id)
```

---

## `services` — Packet Filter Rulesets

Defines rulesets (groups of rules) for the packet filter. Each ruleset operates at Layer 2 (ebtables) or Layer 3 (iptables). 8 columns.

| Index | Column | Type | Description |
|---|---|---|---|
| 0 | `id` | integer | Primary key — unique non-zero integer (no auto-increment); custom rulesets must use `1000`+ |
| 1 | `name` | string | Ruleset name (max 32, `[-0-9A-Za-z_]`) |
| 2 | `description` | string | Human-readable description (max 255) |
| 3 | `layer_id` | `"1"` / `"2"` | `"1"` = L2 (ebtables), `"2"` = L3 (iptables) |
| 4 | `def_serv` | `"0"` / `"1"` | `"1"` = factory default; `"0"` = custom |
| 5 | `src_interf_name` | string | Source interface or `"*"` for any |
| 6 | `des_interf_name` | string | Destination interface or `"*"` for any |
| 7 | `fac_def_pos` | integer | Factory default position (leave `""` for custom) |

See the [Packet Filter guide](../../guides/packet-filter/index.md) for factory defaults, interface names, and [examples](../../guides/packet-filter/examples.md).

---

## `serv_Protocols` — Packet Filter Rules

Individual filter rules within a packet filter ruleset. Each rule specifies match criteria (protocol, addresses, ports) and an action. 35 columns, grouped by function.

**Core** (index 0–10):

| Index | Column | Type | Description |
|---|---|---|---|
| 0 | `id` | integer | Primary key — unique non-zero integer (no auto-increment); custom rules must use `1000`+ |
| 1 | `service_id` | integer | FK to `services.id` |
| 2 | `protocol` | string | `"TCP"`, `"UDP"`, `"ICMP"`, `"*"` for any; prefix `"! "` to negate |
| 3 | `action_id` | `"1"`–`"8"` | `1`=ACCEPT, `2`=DROP, `5`=CUT, `6`=REJECT, `7`=INACTIVE, `8`=CUTANDACCEPT |
| 4 | `log_active` | `"0"` / `"1"` | `"1"` = log matched packets |
| 5 | `alarm_active` | `"0"` / `"1"` | `"1"` = trigger alarm signal |
| 6 | `description` | string | Rule name (max 32); also used as LOG prefix |
| 7 | `icmp_type` | string | ICMP type (e.g. `"echo-request"`, `"any"`); empty for non-ICMP |
| 8 | `icmp_rej_type` | string | ICMP reject type; only for REJECT action |
| 9 | `limitpack` | integer | Rate limit (packets/sec); empty for no limit |
| 10 | `position` | integer | Rule order within ruleset; lowest first |

**Addresses** (index 11–18):

| Index | Column | Type | Description |
|---|---|---|---|
| 11 | `src_mac_add` | string | Source MAC, `"*"`, `"@groupname"`, or `""` (L2 only) |
| 12 | `src_ip_add` | string | Source IP, `"*"`, `"@groupname"`, or `""` |
| 13 | `src_netmask` | string | Source netmask (e.g. `"255.255.255.0"`), `"*"`, or `""` |
| 14 | `src_port` | string | Source port, range (`"80:443"`), `"*"`, or `""` |
| 15 | `des_mac_add` | string | Destination MAC (L2 only) |
| 16 | `des_ip_add` | string | Destination IP, `"*"`, `"@groupname"`, or `""` |
| 17 | `des_netmask` | string | Destination netmask |
| 18 | `des_port` | string | Destination port or range |

**Behavior** (index 19–26):

| Index | Column | Type | Description |
|---|---|---|---|
| 19 | `prot_hex` | string | L2 protocol hex (e.g. `"0800"`); empty for L3 |
| 20 | `prot_transport` | string | L2 transport protocol number; empty for L3 |
| 21 | `state_type_id` | `"1"`–`"4"` / `""` | `"1"`/`"3"` = conntrack; `"2"` = stateless (TCP flags) |
| 22 | `nat_ip` | string | Reserved — must be `""` |
| 23 | `nat_port` | string | Reserved — must be `""` |
| 24 | `states` | string | Conntrack states or TCP flags (depends on `state_type_id`) |
| 25 | `statevalue` | integer | L2 TCP flag bitmask; empty for L3 |
| 26 | `revert` | `"0"` / `"1"` | `"1"` = auto-generate reverse conntrack rule |

**Signal & Visibility** (index 27–34):

All `sigcheck_*`, `sig_*`, and `audit_active` fields must be `"0"` or `"1"` — never empty string. See the [Table Reference](../../guides/packet-filter/tables.md#signal-visibility-columns) for details.

| Index | Column | Type | Description |
|---|---|---|---|
| 27 | `hide` | `"0"` / `"1"` | `"1"` = suppress ALARM/CUT targets and logging |
| 28 | `sigcheck_vpn` | `"0"` / `"1"` | `"1"` = apply VPN signal condition; must be `"0"` or `"1"`, not empty |
| 29 | `sig_vpn` | `"0"` / `"1"` | Expected VPN signal value; must be `"0"` or `"1"`, not empty |
| 30 | `sigcheck_cut` | `"0"` / `"1"` | `"1"` = apply CUT signal condition; must be `"0"` or `"1"`, not empty |
| 31 | `sig_cut` | `"0"` / `"1"` | Expected CUT signal value; must be `"0"` or `"1"`, not empty |
| 32 | `sigcheck_vpnup` | `"0"` / `"1"` | `"1"` = apply VPN-up signal condition; must be `"0"` or `"1"`, not empty |
| 33 | `sig_vpnup` | `"0"` / `"1"` | Expected VPN-up signal value; must be `"0"` or `"1"`, not empty |
| 34 | `audit_active` | `"0"` / `"1"` | `"1"` = enable AUDIT target; must be `"0"` or `"1"`, not empty |

See the [Packet Filter guide](../../guides/packet-filter/tables.md) for action IDs, rule modes, and [examples](../../guides/packet-filter/examples.md).

---

## `selected_services` — Active Packet Filter Rulesets

Activates a packet filter ruleset with optional time-based scheduling. 7 columns.

| Index | Column | Type | Description |
|---|---|---|---|
| 0 | `id` | integer | Primary key — unique non-zero integer (no auto-increment); custom entries must use `1000`+ |
| 1 | `serv_id` | integer | FK to `services.id` |
| 2 | `days` | string | Comma-separated weekdays (e.g. `"Mon,Tue,Wed,Thu,Fri"`) or `""` for all |
| 3 | `time_active` | `"0"` / `"1"` | `"1"` = enable time restriction |
| 4 | `time_start` | string | Start time `HH:MM` (e.g. `"08:00"`) or `""` |
| 5 | `time_stop` | string | Stop time `HH:MM` (e.g. `"17:00"`) or `""` |
| 6 | `position` | integer | Ruleset evaluation order; lowest first |

See the [Packet Filter guide](../../guides/packet-filter/index.md) for scheduling details and [examples](../../guides/packet-filter/examples.md).
