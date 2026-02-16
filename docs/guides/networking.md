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
