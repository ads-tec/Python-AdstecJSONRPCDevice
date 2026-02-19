# Python-AdstecJSONRPCDevice

Python reference implementation for the JSON-RPC 2.0 API of ads-tec Industrial IT devices: **IRF1000**, **IRF2000**, **IRF3000** firewalls and all ads-tec Web terminals.

## Documentation

**[ads-tec Industrial IT JSON-RPC API Documentation](https://ads-tec.github.io/Python-AdstecJSONRPCDevice/)**

The documentation covers:

- **[Getting Started](https://ads-tec.github.io/Python-AdstecJSONRPCDevice/latest/getting-started/)** — Installation and first connection
- **[JSON-RPC Methods](https://ads-tec.github.io/Python-AdstecJSONRPCDevice/latest/api-reference/jsonrpc-methods/)** — Core API method reference
- **[Configuration Variables](https://ads-tec.github.io/Python-AdstecJSONRPCDevice/latest/api-reference/config-variables/)** — Full variable catalog
- **[Status Properties](https://ads-tec.github.io/Python-AdstecJSONRPCDevice/latest/api-reference/status-properties/)** — Device status queries
- **[JSON Schemas](https://ads-tec.github.io/Python-AdstecJSONRPCDevice/latest/api-reference/schemas/)** — Machine-readable request/response schemas
- **Guides** — Firmware update, networking, certificates, password management, and more

## Quick Example

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

version = dev.status("imageversion")
print(f"Firmware: {version}")

dev.config_set_commit({"ntp_service": "enabled", "ntp_server": "pool.ntp.org"})

dev.logout()
```

## Requirements

```
pip install requests
```

Optional, for the traffic monitor example:

```
pip install matplotlib
```

## Examples

The `examples/` directory contains ready-to-run scripts. Each script can be run directly from any directory:

```
python3 examples/status.py 192.168.0.254 admin admin
```

| Script | Description |
|---|---|
| `status.py` | Query device status (firmware version, uptime, etc.) |
| `diagnostics.py` | Collect diagnostic information |
| `create_user.py` | Create a new user account |
| `change_password.py` | Change a user's password |
| `zxcvbn.py` | Check password strength |
| `datetime_settings.py` | Configure date/time and NTP |
| `web_panel.py` | Configure web panel IP and settings |
| `settings_backup.py` | Export and import device settings |
| `cert_upload.py` | Upload TLS/VPN certificates |
| `firmware_update.py` | Upload and install firmware |
| `vpn_approve.py` | Approve Big-LinX VPN connection |
| `gpio.py` | Read/write GPIOs, LEDs, buttons (firewalls only) |
| `remote_capture.py` | Start a remote packet capture |
| `packet_filter_crud.py` | Create, read, update, delete filter rules (firewalls only) |
| `packet_filter_export.py` | Export packet filter configuration (firewalls only) |
| `packet_filter_import.py` | Import packet filter configuration (firewalls only) |
| `filter_monitor.py` | Monitor packet filter byte counters in real time (firewalls only) |
| `traffic_monitor.py` | Live matplotlib chart of network traffic |

## License

BSD 2-Clause — see [LICENSE](LICENSE).
