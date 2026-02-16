# Date & Time / NTP

## Setting the Timezone

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# List available timezones
available = dev.status("timezone_list")
timezones = available.split(" ")
print(f"Available: {timezones[:5]}...")  # e.g., ['Europe/Berlin', 'UTC', ...]

# Set timezone
dev.config_set_commit({"timezone": "Europe/Berlin"})

dev.logout()
```

## Configuring NTP (Automatic Time Sync)

```python
import time

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

dev.config_set_commit({
    "ntp_service": "enabled",
    "ntp_server": "ptbtime1.ptb.de",
    "ntp_server2": "ptbtime2.ptb.de"
})

# Wait for NTP synchronization
for i in range(10):
    time.sleep(2)
    ntpstat = dev.status("ntpstat_sources")
    for line in ntpstat.split("\n"):
        fields = line.split(",")
        if fields[1] == "*":
            print(f"Synced to: {fields[2]}")
            break
    else:
        continue
    break

dev.logout()
```

## Setting Time Manually

When NTP is not available, set the date and time directly:

```python
dev.config_set_commit({
    "ntp_service": "disabled",
    "day": "15",
    "month": "03",
    "year": "2026",
    "hour": "14",
    "minute": "30",
    "second": "00"
})
```

!!! note
    Date and time fields are strings. Day, month, hour, minute, and second should be zero-padded (e.g., `"01"`, not `"1"`).
