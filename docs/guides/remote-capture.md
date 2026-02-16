# Remote Capture

## Overview

ads-tec devices support remote packet capture (rpcap) which allows tools like Wireshark to capture traffic directly from device interfaces.

## Setting Up Remote Capture

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Get available interfaces
ifaces = dev.status("symbolic_ifnames_with_umts_with_ipsec").split(" ")
print(f"Available interfaces: {ifaces}")
# e.g., ['lan', 'wan', 'docker', 'vpn10']

# Block all interfaces except 'lan' from capture
ifaces.remove("lan")
native_block_list = dev.convert_to_ifname(ifaces)

# Enable remote capture
dev.config_set_commit({
    "rpcap_status": "enabled",
    "rpcap_hostlist": "192.168.0.190",        # Allowed capture host
    "rpcap_access": native_block_list          # Interfaces to block
})

dev.logout()
```

## Interface Name Conversion

Device interfaces have two names:

- **Symbolic names**: Human-readable (`lan`, `wan`, `docker`, `vpn10`)
- **Native names**: System-level (`br0`, `br1`, `lxcbr0`, `l3tap10`)

The `rpcap_access` configuration requires native names. Use `convert_to_ifname()` to convert:

```python
symbolic = ["wan", "docker", "vpn10"]
native = dev.convert_to_ifname(symbolic)
# Returns: "br1 lxcbr0 l3tap10"
```

## Configuration Variables

| Variable | Description |
|---|---|
| `rpcap_status` | `"enabled"` / `"disabled"` — Enable remote capture service |
| `rpcap_hostlist` | Comma-separated list of IPs allowed to capture |
| `rpcap_access` | Space-separated native interface names to **block** from capture |
