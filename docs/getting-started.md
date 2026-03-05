# Getting Started

## Prerequisites

- Python 3.6+
- Network access to an ads-tec device
- Valid device credentials (username and password)

## Installation

Clone the repository:

```bash
git clone https://github.com/ads-tec/Python-AdstecJSONRPCDevice.git
cd Python-AdstecJSONRPCDevice
```

Install the required dependency:

```bash
pip install requests
```

## First Connection

```python
import jsonrpcdevice

# Create a device instance
dev = jsonrpcdevice.AdstecJSONRPCDevice(
    target="192.168.0.254",   # Device IP address
    user="admin",             # Username
    pw="admin",               # Password
    timeout=120.0,            # Request timeout in seconds (optional)
    verify=False              # SSL certificate verification (optional)
)

# Query the firmware version
version = dev.status("imageversion")
print(f"Firmware version: {version}")

# Always log out when done
dev.logout()
```

!!! note "SSL Verification"
    By default, SSL certificate verification is disabled (`verify=False`) because ads-tec devices typically use self-signed certificates. Set `verify=True` if your device has a trusted certificate installed.

!!! note "Automatic Authentication"
    You do not need to call `get_sid()` manually. The library automatically authenticates on the first API call.

## Understanding Configuration Sessions

Changing device configuration requires a **configuration session**. This ensures that multiple changes are applied atomically.

### Manual Session Management

```python
# 1. Start a session
cfg_session_id = dev.sess_start()

# 2. Set values within the session
dev.config_set(cfg_session_id, {
    "ntp_service": "enabled",
    "ntp_server": "pool.ntp.org"
})

# 3. Commit the session to apply changes
dev.sess_commit(cfg_session_id)
```

### Convenience Method

For simple changes, use `config_set_commit()` which handles session management automatically:

```python
dev.config_set_commit({
    "ntp_service": "enabled",
    "ntp_server": "pool.ntp.org"
})
```

## Persisting Changes with `save_now`

By default (`nvram_mode = "commit"`), `config_set_commit()` applies changes **immediately** but does **not** save them to persistent storage (NVRAM). Changes that are only committed will be lost on the next power cycle.

To save committed changes permanently, set the `save_now` trigger variable:

```python
dev.config_set_commit({"save_now": "1"})
```

!!! warning "Test before you save"
    It is strongly recommended to **verify** that the device is still reachable after applying changes — especially for network settings on remote devices — **before** persisting with `save_now`. If a misconfiguration makes the device unreachable, an on-site power cycle will restore the previous working configuration.

```python
# 1. Apply new settings (not yet persistent)
dev.config_set_commit({"lan_gateway": "10.0.0.1"})

# 2. Verify the device is still reachable
online, _ = jsonrpcdevice.check_host("192.168.0.254", timeout=5)
if online:
    # 3. Only now persist to NVRAM
    dev.config_set_commit({"save_now": "1"})
    print("Settings saved permanently")
else:
    print("Device unreachable — power cycle to restore previous config")
```

## Error Handling

```python
try:
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "wrong_password")
    dev.get_sid()
except Exception as e:
    print(f"Login failed: {e}")
```

## Next Steps

- [JSON-RPC Methods](api-reference/jsonrpc-methods.md) — Full API method reference
- [Python Reference Implementation](api-reference/python-client.md) — All methods and parameters
- [Configuration Variables](api-reference/config-variables.md) — Available configuration keys
- [Status Properties](api-reference/status-properties.md) — Available status queries
