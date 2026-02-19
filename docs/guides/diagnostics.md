# Status & Diagnostics

## Querying Device Information

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

system_name = dev.status("system_name")
print(f"System name: {system_name}")

imageversion = dev.status("imageversion")
print(f"Firmware version: {imageversion}")

cpustat = dev.status("cpustat")
print(f"CPU stats: {cpustat}")

serial = dev.status("redbootserial")
print(f"Serial number: {serial}")

hardware = dev.status("redbootproduct")
print(f"Hardware revision: {hardware}")

dev.logout()
```

## Status with Parameters

Some status properties accept parameters:

```python
# Ping a host 3 times
ping_result = dev.status("ping4", "127.0.0.1", "3")
print(f"Ping result: {ping_result}")
```

## Event Log

The `eventlog` status property returns the device's syslog. It reads from file-based syslog if enabled, from SD card if available, or from the kernel ring buffer as fallback.

### Parameters

| Parameter | Position | Type | Description |
|---|---|---|---|
| `lines` | 1st | integer as string | Number of most recent lines to return. `"0"` = all lines |
| `filter` | 2nd | string | Extended regex pattern (grep -E) to filter log lines. Empty = no filter |

Both parameters are optional. When omitted, the full unfiltered log is returned.

### Basic Usage

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Get the last 10 log lines
log = dev.status("eventlog", "10")
print(log)

# Get all log lines (can be large)
full_log = dev.status("eventlog")

dev.logout()
```

### Filtering with Regex

The filter parameter uses extended regular expressions (grep -E), supporting `|` for alternation, `()` for grouping, and other ERE syntax:

```python
# Authentication events
auth_log = dev.status("eventlog", "20", "login|auth|session")

# Kernel messages
kern_log = dev.status("eventlog", "50", "kernel:")

# Network-related events
net_log = dev.status("eventlog", "0", "eth[0-9]|br[0-9]|link")
```

### Packet Filter Log Entries

When a packet filter rule has `log_active="1"`, matched packets are logged to syslog. Use the filter to find these entries:

```python
# Get recent packet filter log entries
pf_log = dev.status("eventlog", "50", "FILTER|IN=.*OUT=")
for line in pf_log.strip().split("\n"):
    if line:
        print(line)
```

#### Log Line Format

Each logged packet produces a kernel syslog line in standard iptables LOG format. The log prefix is `{ruleset_name}.{rule_description}`:

**ICMP example** (echo request):

```
Feb 19 19:19:30 IRF3851-AX20291598 kernel: [13460.442264] LOG_ALL.LOG_ALL
  IN=ETH7 OUT=ETH2
  MAC=3e:18:92:08:1c:79:2a:18:92:07:d2:fb:08:00
  SRC=192.168.12.254 DST=192.168.0.190
  LEN=84 TOS=0x00 PREC=0x00 TTL=63 ID=50556
  PROTO=ICMP TYPE=0 CODE=0 ID=5 SEQ=452
```

**TCP example** (SYN — connection initiation to port 80):

```
Feb 19 19:23:20 IRF3851-AX20291598 kernel: [13689.627510] LOG_ALL.LOG_ALL
  IN=ETH2 OUT=ETH7
  MAC=2a:18:92:08:1c:79:cc:96:e5:40:d0:52:08:00
  SRC=192.168.0.190 DST=192.168.12.254
  LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=46464 DF
  PROTO=TCP SPT=34440 DPT=80 WINDOW=64240 RES=0x00 SYN URGP=0
```

| Field | Description |
|---|---|
| `LOG_ALL.LOG_ALL` | Log prefix: `{services.name}.{serv_Protocols.description}` |
| `IN=ETH7` | Ingress interface (uses UI alias name, see [interface aliases](packet-filter/index.md#interface-name-aliases)) |
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

Protocol-specific fields follow `PROTO=`:

| Protocol | Additional Fields |
|---|---|
| **ICMP** | `TYPE=` (e.g., `8`=echo request, `0`=echo reply), `CODE=`, `ID=`, `SEQ=` |
| **TCP** | `SPT=` (source port), `DPT=` (dest port), `WINDOW=` (TCP window size), `RES=` (reserved bits), flags (`SYN`, `ACK`, `FIN`, `RST`, `PSH`, `URG`), `URGP=` (urgent pointer) |
| **UDP** | `SPT=` (source port), `DPT=` (dest port), `LEN=` (UDP payload length) |

!!! tip "Troubleshooting: move a LOG rule through the ruleset order"
    Create a dedicated LOG ruleset (e.g., `log_active="1"`, action ACCEPT, matching all traffic) and change its `selected_services.position` to insert it **before** or **after** specific rulesets. This lets you observe which packets reach a given point in the filter chain — if a packet appears in the log at position 2 but not at position 4, it was consumed by a ruleset in between. Move the LOG ruleset up and down to isolate exactly where traffic is being accepted, dropped, or redirected.

!!! tip "Combine with datacollection counters"
    Use the [packet filter counters](packet-filter/examples.md#monitoring-packet-filter-counters) from the `datacollection` API for real-time byte/packet counts. Use the event log for detailed per-packet inspection when `log_active` is enabled on a rule.

### Audit Events

The Linux audit subsystem (`audispd`) logs security-relevant events such as login attempts, configuration changes, and process executions. Filter for `audispd` to retrieve these:

```python
# Get the last 100 audit events
audit_log = dev.status("eventlog", "100", "audispd")
for line in audit_log.strip().split("\n"):
    if line:
        print(line)
```

---

## Downloading Diagnostic Archive

The diagnostic archive (`diag.tar.gz`) contains system information including CPU, memory, network, and temperature data.

```python
from datetime import datetime

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Trigger diagnostic generation
dev.config_set_commit({"generate_diag_now": "1"})

# Build a descriptive filename
system_name = dev.status("system_name")
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
output_filename = f"diag_{system_name}_{timestamp}.tar.gz"

# Download
dev.download_file("diag.tar.gz", output_filename)
print(f"Downloaded: {output_filename}")

dev.logout()
```

!!! tip
    The diagnostic archive is generated on-demand. Always call `config_set_commit({"generate_diag_now": "1"})` before downloading to ensure you get current data.
