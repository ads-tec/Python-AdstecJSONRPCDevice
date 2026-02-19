# Status Properties

Status properties are queried with `status.get()`. They are read-only and return current device state.

## Usage

```python
# Simple query (no parameters)
version = dev.status("imageversion")

# Query with parameters
ping_result = dev.status("ping4", "127.0.0.1", "3")
```

---

## System Information

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `system_name` | — | string | Device system name |
| `imageversion` | — | string | Current firmware version (e.g., `"Ads-tec/IRF2xxx/2.6.5/SVN-R13781.B-69636"`) |
| `second_imageversion` | — | string | Firmware version on second partition |
| `firmwareupdate_prepared` | — | `"yes"` / `"no"` | Whether second partition has a valid firmware ready to activate |
| `firmwareupdate_progress` | — | `-1` or `0`–`100` | Flashing percent complete, or `-1` if no flashing is active |
| `firmwareupdate_inprogress` | — | `"yes"` / `"no"` | Whether a firmware update is currently in progress |
| `firmware_version_downgrade_check` | version string | `"yes"` / `"no"` | Whether a downgrade to the given version is possible (e.g., `dev.status("firmware_version_downgrade_check", "1.5.0")`) |
| `product` | — | string | Device family identifier (e.g., `"IRF2xxx"`) — used for firmware file matching |
| `version` | — | string | Running firmware main version (e.g., `"1.5.0"`) |
| `buildno` | — | string | Detailed revision and build number |
| `configstate` | — | string | Configuration state (e.g., `"notsaved"` if unsaved changes exist) |
| `redbootserial` | — | string | Device serial number |
| `redbootproduct` | — | string | Hardware revision / product identifier |
| `realproduct` | — | string | Product designation (e.g., `"IF1110"`) |
| `product_alias` | — | string | Product alias name |
| `versionbuild` | — | string | Firmware version with build number (e.g., `"2.0.6 (Build 55290)"`) |
| `boot_finished` | — | `"yes"` / `"no"` | Whether the device has completed its boot process |
| `uptime` | — | string | Time since last reboot + load average |
| `uptimesec` | — | string | Uptime in seconds |
| `cpustat` | — | string | CPU load in percent |
| `memstat` | — | string | Main memory utilization in percent |
| `meminfo` | process name | string | Memory utilization of a specified process |
| `simstate` | — | `"no sim"` / `"synced"` / `"not synced"` | Memory card state |
| `diag_log` | category string | string | Internal diagnostic log for a subsystem (e.g., `dev.status("diag_log", "fw_update")` for firmware update errors). Format may change between versions |
| `eventlog` | `lines` (int), `filter` (regex) | multiline string | Event log output. `lines` limits output (`0` = all); `filter` is an extended regex (grep -E). Both optional |
| `reboot_timer` | — | seconds | Time remaining until scheduled reboot |
| `customersettings_size` | — | number (kB) | Size of customer settings |
| `customersettings_timestamp` | — | unix timestamp | Change date of customer settings |

---

## Network Interfaces

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `if_status` | interface name | string | Physical interface status. Returns negotiated speed/duplex or `"no link"` |
| `if_mac` | interface name | MAC address | Hardware address (e.g., `"00:CC:90:00:71:01"`) |
| `if_ip` | interface name | IP address | Interface IP address |
| `if_rxb` | interface name | number | Bytes received via interface |
| `if_txb` | interface name | number | Bytes sent via interface |
| `symbolic_ifnames_with_umts_with_ipsec` | — | string | Space-separated list of symbolic interface names (e.g., `"lan wan docker vpn10"`) |

Valid interface names for `if_status`, `if_mac`, `if_ip`, `if_rxb`, `if_txb`:

- Physical: `eth0`, `eth1`, `ixp0`, `ixp1`
- Bridge: `br0`, `br1`
- VLAN: `ixp0.101`, `ixp0.102`, `ixp0.103`, `ixp0.104`

---

## Network Diagnostics

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `ping4` | host, count | string | IPv4 ping. Example: `dev.status("ping4", "8.8.8.8", "3")` |
| `traceroute4` | host | string | Traceroute to host |
| `nslookup4` | hostname | string | DNS lookup |
| `arping` | host | `"up"` / `"down"` | ARP-level host check |
| `tcpping` | host, port | `"Host is up"` / `"Host is down"` | TCP SYN check on a port |
| `routes` | — | string | System routing table |
| `nameserver` | — | string | Space-separated list of active DNS servers |
| `dhcp_gateway` | — | IP address | Current DHCP default gateway |

---

## Date & Time

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `date` | — | string | Current system time and timezone (e.g., `"Fri Oct 26 00:00:00 CEST 2012"`) |
| `timezone_list` | — | string | Space-separated list of available timezones |
| `ntpstat_sources` | — | string | NTP sync sources (newline-separated CSV). `*` in second field = active source |

### NTP Source Parsing

```python
ntpstat = dev.status("ntpstat_sources")
for line in ntpstat.split("\n"):
    fields = line.split(",")
    if fields[1] == "*":
        print(f"Synced to: {fields[2]}")
```

---

## Firewall-Only Properties

OpenVPN, CUT & ALARM, 3G/4G UMTS/LTE, and GNSS/GPS status properties are available on firewall models only. See [Status Properties (Firewalls)](firewall/status-properties.md).

---

## Big-LinX

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `blxstat_vpnstate` | — | string | Big-LinX VPN state (see values below) |
| `blxstat` | — | JSON object | Full Big-LinX diagnostic status (see fields below) |
| `wwh_status` | — | `"ERROR"` / `"ONLINE"` / `"OFFLINE"` | Big-LinX WWH connection status |
| `pintries` | — | number | PIN attempts remaining before smart card is blocked |

### `blxstat_vpnstate` Values

| State | Description |
|---|---|
| `""` (empty) | Not running |
| `"OFF"` | VPN off |
| `"INITIAL"` | Initializing |
| `"CONNECTING"` | Connecting |
| `"ASSIGN_IP"` | Assigning IP |
| `"ADD_ROUTES"` | Adding routes |
| `"CONNECTED"` | Tunnel established |
| `"RECONNECTING"` | Reconnecting |
| `"EXITING"` | Shutting down |
| `"WAIT"` | Waiting |
| `"AUTH"` | Authenticating |
| `"GET_CONFIG"` | Retrieving config |
| `"RESOLVE"` | Resolving hostname |
| `"TCP_CONNECT"` | TCP connecting |
| `"WAITINGFORAPPROVAL"` | Pending approval (4-eyes principle) |

### `blxstat` JSON Fields

| Field | Type | Description |
|---|---|---|
| `cardstate` | string | Smart card state machine state |
| `tokenlabel` | string | Common Name of Big-LinX X.509 VPN certificate |
| `vpn_state_name` | string | Current VPN process state |
| `vpn_oldstate_name` | string | Previous VPN state |
| `vpn_ip` | string | VPN interface IP (empty if down) |
| `vpn_server_ip` | string | VPN server public IP and port |
| `vpn_permanent` | string | Whether connection is permanent |
| `vpn_ctrl_state` | integer | Target VPN state: `1` = should be up, `0` = should be down |
| `wwh_lastbeat` | string | Last WWH heartbeat |
| `wwh_service` | string | WWH service state |
| `wwh_delay` | string | WWH delay |
| `wwh_error` | string | WWH error info |

---

## Certificates

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `cacerts` | — | string | List of installed CA certificates |
| `clcerts` | — | string | List of installed client/server certificates |
| `print_cacert` | filename | string | Details of a CA certificate |
| `print_cert` | filename | string | Details of a client/server certificate |

---

## SCEP

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `scep` | — | `"0"` - `"99"` | SCEP state machine: `0` = not activated; `10` = starting; `20` = waiting for CA certs; `40` = waiting for client certs; `50` = success; `60` = error |

