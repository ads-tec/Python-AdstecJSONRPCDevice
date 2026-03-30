# Port Forwarding

!!! note "Firewall models only"
    Port forwarding is available on IRF1000, IRF2000, and IRF3000 firewalls in IP-Router mode.

Port forwarding (DNAT) allows incoming connections on an external interface to be redirected to devices on an internal network. From the external sender's perspective, the service appears to be provided directly by the router.

## Concepts

Two NAT mechanisms are involved:

- **DNAT (Destination NAT)** — rewrites the destination address and optionally the port of incoming packets so the connection reaches an internal host. This is the standard method for making services behind a NAT router accessible from the outside.

- **SNAT (Source NAT)** — additionally masks the source address behind the router's local IP. Required when the internal target host has no return route to the original sender (e.g., a PLC without a default gateway).

## The `forwarding` Table

Port forwarding rules are stored in the `forwarding` table (see e.g. [IRF3821 Configuration Database](../api-reference/configdb/IRF3821.md#packet-filter-nat)). Each row defines one forwarding rule. Changes take effect immediately on commit — no trigger variable is needed.

### Interface Names

The `fwifname` column uses **Linux interface names** (e.g., `br1`, `wwan1`, `ppp0`), not the symbolic aliases shown in the web UI. Use the `_ifname` config variables to resolve them:

```python
# Resolve WAN interface name for use in forwarding rules
wan_ifname = dev.config_get(["wan_ifname"])["result"][0]["wan_ifname"]
print(wan_ifname)  # e.g. "br1"
```

See [Networking — Interface Names](networking.md#interface-names) for the full mapping.

### Port Ranges

Both `fwlocalport` and `fwtargetport` support ranges using a hyphen (e.g., `"8080-8090"`). When using port ranges, the number of ports must match between local and target.

### Protocol Wildcard

Setting `fwproto` to `"*"` forwards both protocols (TCP and UDP) to the target IP. When using the wildcard protocol, port numbers are ignored — all traffic matching the interface and destination IP is forwarded.

## Rule Order — First Match Wins

Forwarding rules are translated to iptables DNAT rules in the PREROUTING chain. Rules are appended in table row order, and **the first matching rule wins** — once a packet matches a DNAT rule, no further forwarding rules are evaluated for that packet.

This means rule order matters. You can use it to cherry-pick specific ports to dedicated hosts, then place a wildcard (`*`) rule at the end to catch all remaining traffic and forward it to a default host.

### Example: Cherry-Pick Ports with a Catch-All Default

In this scenario, three specific services are forwarded to their respective hosts, while all other incoming traffic on the WAN interface is sent to a default server at 192.168.10.1:

```python
cfg = dev.sess_start()

# Rule 1: RDP to Windows host
dev.table_insert("forwarding", cfg, [
    wan_ifname, "tcp", "", "3389",
    "192.168.10.200", "3389",
    "disabled", "", "RDP", "enabled", "1", "disabled",
])

# Rule 2: HTTPS to web server
dev.table_insert("forwarding", cfg, [
    wan_ifname, "tcp", "", "443",
    "192.168.10.100", "443",
    "disabled", "", "HTTPS", "enabled", "2", "disabled",
])

# Rule 3: SSH to management host
dev.table_insert("forwarding", cfg, [
    wan_ifname, "tcp", "", "22",
    "192.168.10.50", "22",
    "disabled", "", "SSH", "enabled", "3", "disabled",
])

# Rule 4: Catch-all — forward everything else to default host
dev.table_insert("forwarding", cfg, [
    wan_ifname, "*", "", "",
    "192.168.10.1", "",
    "disabled", "", "Default host", "enabled", "99", "disabled",
])

dev.sess_commit(cfg)
```

An incoming TCP connection to port 443 matches rule 2 and is forwarded to 192.168.10.100. A UDP packet on port 5000 does not match any of the specific rules, falls through to rule 4, and is forwarded to 192.168.10.1.

!!! warning "Place specific rules before wildcard rules"
    A wildcard rule (`fwproto` = `"*"`) matches **all** traffic on the interface. If it appears before a port-specific rule, the specific rule will never be reached. Always insert specific port forwards with a lower `fwposition` than catch-all rules.

## When to Use SNAT

| Scenario | SNAT needed? |
|---|---|
| Target host has default gateway pointing to the router | No |
| PLC / controller without default gateway | **Yes** |
| Docker container (rootless namespace) | **Yes** |
| Target on isolated subnet with no route to external network | **Yes** |

!!! warning "SNAT hides the original source IP"
    With SNAT enabled, the target host sees only the router's local IP address as the sender. If the application requires the original source IP (e.g., for access logging), SNAT should not be used. Instead, configure a default gateway on the target host.

## Example: Forward RDP to Internal Host

Forward TCP port 3389 from the WAN interface to an internal host at 192.168.10.200:

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Resolve WAN interface name
wan_ifname = dev.config_get(["wan_ifname"])["result"][0]["wan_ifname"]

cfg = dev.sess_start()
dev.table_insert("forwarding", cfg, [
    wan_ifname,       # fwifname: WAN interface
    "tcp",            # fwproto
    "",               # fwlocalip (any router IP on this interface)
    "3389",           # fwlocalport
    "192.168.10.200", # fwtargetip
    "3389",           # fwtargetport
    "disabled",       # fwsnat
    "",               # fwsrcnet (no restriction)
    "RDP access",     # fwcomment
    "enabled",        # fwenabled
    "1",              # fwposition
    "disabled",       # fwrsnat
])
dev.sess_commit(cfg)

dev.logout()
```

## Example: Forward with SNAT and Source Restriction

Forward TCP port 443 from the WAN interface to a PLC at 192.168.10.100, restricted to the source network 10.0.0.0/24:

```python
cfg = dev.sess_start()
dev.table_insert("forwarding", cfg, [
    wan_ifname,       # fwifname
    "tcp",            # fwproto
    "",               # fwlocalip
    "443",            # fwlocalport
    "192.168.10.100", # fwtargetip
    "443",            # fwtargetport
    "enabled",        # fwsnat (PLC has no default gateway)
    "10.0.0.0/24",    # fwsrcnet (restrict to this network)
    "PLC HTTPS",      # fwcomment
    "enabled",        # fwenabled
    "1",              # fwposition
    "disabled",       # fwrsnat
])
dev.sess_commit(cfg)
```

## Example: Port Remapping (PAT)

Redirect external port 50022 to internal SSH port 22 — useful for avoiding standard ports or making multiple hosts accessible via different external ports:

```python
cfg = dev.sess_start()
dev.table_insert("forwarding", cfg, [
    wan_ifname,       # fwifname
    "tcp",            # fwproto
    "",               # fwlocalip
    "50022",          # fwlocalport (external port)
    "192.168.10.50",  # fwtargetip
    "22",             # fwtargetport (internal port)
    "disabled",       # fwsnat
    "",               # fwsrcnet
    "SSH remapped",   # fwcomment
    "enabled",        # fwenabled
    "1",              # fwposition
    "disabled",       # fwrsnat
])
dev.sess_commit(cfg)
```

## Managing Existing Rules

### List All Rules

```python
rules = dev.call("config", "export_pages", pages=["FORWARDCONF"])
print(json.dumps(rules, indent=2))
```

### Disable a Rule Without Deleting

```python
cfg = dev.sess_start()
dev.table_up("forwarding", cfg,
    condition={"fwcomment": "RDP access"},
    values={"fwenabled": "disabled"}
)
dev.sess_commit(cfg)
```

### Delete a Rule

```python
cfg = dev.sess_start()
dev.table_del("forwarding", cfg,
    condition={"fwcomment": "RDP access"}
)
dev.sess_commit(cfg)
```

## Docker Container Forwarding

On IRF1000 and IRF3000 devices with Docker, the Docker environment runs in a rootless network namespace behind the `DOCKER` interface (`lxcbr0`, default IP 10.0.3.1/24).

### Bridge Mode with `-p` (Recommended)

Publishing ports with `docker run -p 8080:80` binds to `0.0.0.0` in the main namespace — the service is directly accessible on **all** interfaces. No forwarding rule is needed, but use firewall rules to restrict access.

### Forwarding to Docker-Bound Services

If a container binds to the Docker interface only (`-p 10.0.3.1:8080:80`), or uses host networking, create a forwarding rule with SNAT:

```python
cfg = dev.sess_start()
dev.table_insert("forwarding", cfg, [
    wan_ifname,       # fwifname
    "tcp",            # fwproto
    "",               # fwlocalip
    "8080",           # fwlocalport
    "10.0.3.1",       # fwtargetip (Docker bridge)
    "8080",           # fwtargetport
    "enabled",        # fwsnat (required for Docker namespace)
    "",               # fwsrcnet
    "Docker web",     # fwcomment
    "enabled",        # fwenabled
    "1",              # fwposition
    "disabled",       # fwrsnat
])
dev.sess_commit(cfg)
```

!!! tip "SNAT is required for Docker forwarding"
    The Docker rootless namespace has no direct route back to external networks. Without SNAT, return packets will not reach the original sender.

## Interaction with the Packet Filter

Port forwarding rules operate at the NAT level (PREROUTING chain) and take effect **before** the packet filter. The forwarded traffic then passes through the firewall's FORWARD chain. Ensure that [packet filter rules](packet-filter/index.md) allow the forwarded traffic to pass.

## Security Considerations

- Only forward the ports that are actually needed
- Use `fwsrcnet` to restrict access to known IP ranges
- Select the specific protocol (`"tcp"` or `"udp"`) instead of `"*"` where possible
- Set `fwenabled` to `"disabled"` for rules that are no longer needed instead of leaving them active
- Port forwarding does not encrypt traffic — use VPN tunnels for sensitive services
