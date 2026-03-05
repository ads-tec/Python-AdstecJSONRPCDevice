# Remote Syslog

ads-tec devices use syslog-ng internally. By default, remote syslog forwarding is **disabled**. When enabled, the device forwards log messages to a remote syslog server via UDP or TCP on port 514.

## Configuration Variables

| Variable | Values | Default | Description |
|---|---|---|---|
| `syslog_service` | `"enabled"` / `"disabled"` | `"disabled"` | Enable remote syslog forwarding |
| `syslog_server` | hostname or IP | — | Remote syslog server address |
| `syslog_service_tcp` | `"enabled"` / `"disabled"` | `"disabled"` | Use TCP instead of UDP |
| `syslog_remote_event` | `"enabled"` / `"disabled"` | `"enabled"` | Forward event log messages to remote server |
| `syslog_remote_audit` | `"enabled"` / `"disabled"` | `"enabled"` | Forward audit log messages to remote server |
| `syslog_local_audit` | `"enabled"` / `"disabled"` | `"disabled"` | Show audit log entries in local event log |

## Enabling Remote Syslog

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

dev.config_set_commit({
    "syslog_service": "enabled",
    "syslog_server": "10.0.0.100",
    "syslog_remote_event": "enabled",
    "syslog_remote_audit": "enabled",
})

# Verify the device is still reachable before persisting
online, _ = jsonrpcdevice.check_host("192.168.0.254", timeout=5)
if online:
    dev.config_set_commit({"save_now": "1"})
    print("Remote syslog enabled and saved")

dev.logout()
```

!!! tip
    Test the configuration before persisting with `save_now`. The syslog-ng service reloads automatically after a config commit — check that messages appear on your syslog server before saving.

## Using TCP Instead of UDP

UDP is the default transport. To use TCP (more reliable, but blocks if the server is unreachable):

```python
dev.config_set_commit({
    "syslog_service": "enabled",
    "syslog_server": "10.0.0.100",
    "syslog_service_tcp": "enabled",
})
```

## Filtering What Gets Forwarded

You can independently control which log categories are forwarded to the remote server:

| `syslog_remote_event` | `syslog_remote_audit` | Result |
|---|---|---|
| `"enabled"` | `"enabled"` | Forward both event and audit logs |
| `"enabled"` | `"disabled"` | Forward event log only |
| `"disabled"` | `"enabled"` | Forward audit log only |
| `"disabled"` | `"disabled"` | Forward nothing (effectively disables remote syslog) |

## Disabling Remote Syslog

```python
dev.config_set_commit({"syslog_service": "disabled"})
dev.config_set_commit({"save_now": "1"})
```

## See Also

- [Event Log](../api-reference/status-properties.md#event-log) — reading the device's event log via the API
- [Diagnostics](diagnostics.md) — generating a full diagnostic archive
