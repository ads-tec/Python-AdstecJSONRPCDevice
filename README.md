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

## License

BSD 2-Clause — see [LICENSE](LICENSE).
