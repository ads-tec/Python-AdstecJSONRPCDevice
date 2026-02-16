# ads-tec Industrial IT JSON-RPC API

JSON-RPC 2.0 API for **ads-tec Industrial IT** devices over HTTPS. This documentation covers the full device API and provides a Python reference implementation.

## Supported Devices

| Device Family | Models | Firmware Version |
|---|---|---|
| **Firewalls** | IRF1000, IRF2000, IRF3000 | IRF 2.2.7 |
| **Web Terminals** | All ads-tec Web terminals | AWT 14.2.7 |

## API Capabilities

- **Authentication** — Session-based login with SID management
- **Configuration** — Read and write device configuration variables with transactional sessions
- **Status Monitoring** — Query device status properties (firmware version, CPU stats, network state, etc.)
- **Table Operations** — CRUD operations on device tables (users, routing, etc.)
- **File Transfer** — Upload firmware, certificates, settings; download diagnostics and backups
- **GPIO Control** — Read digital inputs and control LEDs (firewall models)
- **Password Strength** — Validate passwords using the built-in zxcvbn algorithm

## Quick Example (Python Reference Implementation)

```python
import jsonrpcdevice

# Connect to device
dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Query status
version = dev.status("imageversion")
print(f"Firmware: {version}")

# Change configuration
dev.config_set_commit({"ntp_service": "enabled", "ntp_server": "pool.ntp.org"})

# Clean up
dev.logout()
```

## Documentation Structure

The documentation is organized into three sections by device category:

- **All Devices** — API reference and guides that apply to every ads-tec Industrial IT device
- **Firewalls** (IRF1000 / IRF2000 / IRF3000) — GPIO, IPsec, OpenVPN, CUT & ALARM, 3G/4G, GNSS
- **Web Terminals** — Web Panel display and browser configuration

## Next Steps

- [Getting Started](getting-started.md) — Installation and first connection
- [JSON-RPC Methods](api-reference/jsonrpc-methods.md) — Core API method reference (all devices)
- [JSON Schemas](api-reference/schemas.md) — Machine-readable request/response schemas
- [Python Reference Implementation](api-reference/python-client.md) — Python client documentation
- [Firewall Methods](api-reference/firewall/jsonrpc-methods.md) — GPIO and IPsec (firewalls only)
- [Web Terminal Config](api-reference/terminal/config-variables.md) — Web Panel (terminals only)
