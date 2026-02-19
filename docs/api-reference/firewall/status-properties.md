# Status Properties (Firewalls)

!!! info "Firewall models only"
    The status properties on this page apply to **IRF1000, IRF2000, and IRF3000** firewalls only. For properties available on all devices, see [Status Properties](../status-properties.md).

---

## OpenVPN

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `vpnconnstat` | `tap0` - `tap9` | `"up"` / `"down"` | VPN connection status for a specific interface |
| `vpnclients` | `tap0` - `tap9` | number | Number of connected clients on a VPN interface |

---

## CUT & ALARM

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `alarm` | — | `"off"` / `"on"` | ALARM signal state |
| `intcut` | — | `"off"` / `"on"` | Internal CUT signal state |
| `extcut` | — | `"off"` / `"on"` | External CUT signal state |

---

## 3G/4G (UMTS/LTE)

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `umts_multistat` | — | multiline string | Full detailed UMTS/LTE module status |
| `umts_iccid` | — | string | SIM card ICCID; `"Error"` if no card |
| `umts_pinstate` | — | string | `"READY"` if PIN correct; `"bad pin"` if incorrect |
| `umts_signal` | — | dBm value | Reception strength in dBm |
| `umts_regstate` | — | `"0"` - `"5"` | Registration state: `0` = not registered; `1` = home network; `2` = searching; `3` = denied; `4` = unknown; `5` = roaming |
| `umts_localip` | — | IP address | Device IP if connected |
| `umts_remoteip` | — | IP address | Remote station IP |
| `umts_operator` | — | string | Operator name (e.g., `"vodafone.de"`); `"0"` on error |
| `umts_stat` | — | string | Connection status: `"connected"` / `"standby - connect on demand"` / `"not connected"` / `"connecting..."` |
| `umts_serving_system` | — | JSON object | Contains: `registration`, `plmn_mcc`, `plmn_mnc`, `plmn_description`, `roaming` |
| `umts_supported_bands_json` | — | JSON object | Nested object with `"2G"` / `"3G"` / `"4G"` keys, each containing band-name:value pairs. Band names are valid values for `umts_bands_*` config variables |

---

## GNSS / GPS

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `gnss_devices` | — | string | List of GNSS modems |
| `gnss_tpv` | — | JSON object | Position data: `time` (ISO8601), `lat`, `lon`, `alt` (meters), `track` (m/s) |
| `gnss_sky` | — | JSON array | Received satellites. Each entry has `PRN` (satellite ID) |

---

## Packet Filter Log Format

When a packet filter rule has `log_active="1"`, matched packets are logged to syslog in standard iptables/ebtables LOG format. These entries can be retrieved via the [`eventlog`](../status-properties.md#event-log) status property.

The log prefix is `{services.name}.{serv_Protocols.description}`, allowing you to identify which ruleset and rule matched the packet.

### Examples

**ICMP** (echo reply):

```
Feb 19 19:19:30 IRF3851-AX20291598 kernel: [13460.442264] LOG_ALL.LOG_ALL
  IN=ETH7 OUT=ETH2
  MAC=3e:18:92:08:1c:79:2a:18:92:07:d2:fb:08:00
  SRC=192.168.12.254 DST=192.168.0.190
  LEN=84 TOS=0x00 PREC=0x00 TTL=63 ID=50556
  PROTO=ICMP TYPE=0 CODE=0 ID=5 SEQ=452
```

**TCP** (SYN — connection initiation to port 80):

```
Feb 19 19:23:20 IRF3851-AX20291598 kernel: [13689.627510] LOG_ALL.LOG_ALL
  IN=ETH2 OUT=ETH7
  MAC=2a:18:92:08:1c:79:cc:96:e5:40:d0:52:08:00
  SRC=192.168.0.190 DST=192.168.12.254
  LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=46464 DF
  PROTO=TCP SPT=34440 DPT=80 WINDOW=64240 RES=0x00 SYN URGP=0
```

### Common Fields

| Field | Description |
|---|---|
| `LOG_ALL.LOG_ALL` | Log prefix: `{services.name}.{serv_Protocols.description}` |
| `IN=ETH7` | Ingress interface (uses [UI alias name](../../guides/packet-filter/index.md#interface-name-aliases)) |
| `OUT=ETH2` | Egress interface (uses UI alias name) |
| `MAC=3e:18:...` | Ethernet header: destination MAC (6 bytes), source MAC (6 bytes), EtherType (`08:00` = IPv4) |
| `SRC=192.168.12.254` | Source IP address |
| `DST=192.168.0.190` | Destination IP address |
| `LEN=84` | Total IP packet length (bytes) |
| `TOS=0x00` | Type of Service / DSCP field |
| `PREC=0x00` | IP Precedence |
| `TTL=63` | Time to Live (decremented by each hop) |
| `ID=50556` | IP identification field |
| `DF` | Don't Fragment flag (present or absent) |
| `PROTO=ICMP` | IP protocol (`ICMP`, `TCP`, `UDP`, or numeric) |

### Protocol-Specific Fields

| Protocol | Additional Fields |
|---|---|
| **ICMP** | `TYPE=` (e.g., `8`=echo request, `0`=echo reply), `CODE=`, `ID=`, `SEQ=` |
| **TCP** | `SPT=` (source port), `DPT=` (dest port), `WINDOW=` (TCP window size), `RES=` (reserved bits), flags (`SYN`, `ACK`, `FIN`, `RST`, `PSH`, `URG`), `URGP=` (urgent pointer) |
| **UDP** | `SPT=` (source port), `DPT=` (dest port), `LEN=` (UDP payload length) |
