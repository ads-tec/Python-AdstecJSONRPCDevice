# Networking & IP Change

## Changing the Device IP Address

Changing the device IP requires special handling because the device becomes unreachable at the old address after the change.

Use `config_set_commit_with_ip_change()` which:

1. Applies the configuration change
2. Expects and handles the resulting timeout
3. Waits for the device to become reachable at the new IP
4. Updates the internal target address

```python
import jsonrpcdevice

host = "192.168.0.254"
host_new = "192.168.0.253"

# Use a short timeout so the expected timeout doesn't block too long
dev = jsonrpcdevice.AdstecJSONRPCDevice(host, "admin", "admin", timeout=5)

values = {
    "lan_ipaddr": host_new,
    "lan_netmask": "255.255.255.0",
    "lan_gateway": "192.168.0.1"
}

dev.config_set_commit_with_ip_change(values, host_new)
# dev.target is now host_new

dev.logout()
```

!!! warning
    Set a **short timeout** (e.g., 5 seconds) when you expect an IP change. The default 120-second timeout would cause a long wait before the library detects the expected disconnect.

### Persisting the IP Change

After `config_set_commit_with_ip_change()`, the new IP is active but **not yet saved to NVRAM**. If the device is power-cycled, it will revert to the old IP. To persist the change, set the `save_now` trigger:

```python
dev.config_set_commit_with_ip_change(values, host_new)

# Verify the device is reachable at the new IP
online, _ = jsonrpcdevice.check_host(host_new, timeout=5)
if online:
    dev.config_set_commit({"save_now": "1"})
    print("New IP saved permanently")
else:
    print("Device unreachable — power cycle to restore previous IP")
```

!!! tip "Safe remote reconfiguration"
    Always verify connectivity **before** calling `save_now`. If a misconfigured network setting makes the device unreachable, an on-site power cycle will restore the previous working configuration. This is especially important when configuring devices remotely.

## Interface Names

Each network interface has a **symbolic name** (used in the UI and config variables) and an underlying **Linux interface name** (used for status queries like `if_ip`, `if_mac`). The config variable `{symbolic_name}_ifname` maps between them.

| Symbolic Name | Config Variable | Linux Name (example) |
|---|---|---|
| `lan` | `lan_ifname` | `br0` |
| `wan` | `wan_ifname` | `br1` |
| `lan_port1` | `lan_port1_ifname` | `ETH2` |
| `vpn10` | `vpn10_ifname` | `l3tap10` |
| `docker` | `docker_ifname` | `lxcbr0` |
| `umts` | `umts_ifname` | `wwan1` |

!!! note
    The actual Linux names vary by device model and configuration. Always read the `_ifname` variable rather than hardcoding interface names.

You can also retrieve the full mapping via two status properties that return space-separated lists in matching order:

- `interfaces` — Linux interface names (e.g., `"br0 lxcbr0 l3tap10"`)
- `symbolic_ifnames_with_umts_with_ipsec` — symbolic names (e.g., `"lan docker vpn10"`)

## Querying Interface IP and MAC Address

Use the `_ifname` config variable to resolve the Linux interface name, then query `if_ip` and `if_mac`:

```python
# Get the LAN interface name dynamically
lan_ifname = dev.config_get(["lan_ifname"])["result"][0]["lan_ifname"]

lan_ip = dev.status("if_ip", lan_ifname)
lan_mac = dev.status("if_mac", lan_ifname)
print(f"LAN IP: {lan_ip}, MAC: {lan_mac}")
```

This works for any interface — replace `lan_ifname` with e.g. `wan_ifname` or `vpn10_ifname` to query other interfaces.

See [`examples/lan_ip_mac_status.py`](https://github.com/ads-tec/Python-AdstecJSONRPCDevice/blob/main/examples/lan_ip_mac_status.py) for the complete example.

## Checking Host Availability

```python
is_online, info = jsonrpcdevice.check_host("192.168.0.254", timeout=5)
if is_online:
    print(f"Device online, status code: {info}")
else:
    print(f"Device offline: {info}")
```

## Waiting for a Host to Come Online

```python
# Blocks until the host responds or times out (default: 300 seconds)
jsonrpcdevice.wait_for_host_is_online("192.168.0.254", timeout=300, interval=5)
```
