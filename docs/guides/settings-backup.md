# Settings Backup

## Downloading Device Settings

```python
import jsonrpcdevice
from datetime import datetime

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# 1. Trigger settings preparation
dev.config_set_commit({"save_settings_now": "1"})

# 2. Build a descriptive filename
serial = dev.status("redbootserial")
product = dev.status("product_alias")
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
output_filename = f"settings_{product}_{serial}_{timestamp}.cf2"

# 3. Download
dev.download_file("settings.cf2", output_filename)
print(f"Settings saved to: {output_filename}")

dev.logout()
```

## Restoring Settings

Upload a previously saved `.cf2` file:

```python
dev.upload_file("settings", "settings_IRF3000_ABC123_2026_01_15_14_30.cf2")
```

!!! tip
    Always trigger `save_settings_now` before downloading. This ensures the settings file reflects the current device configuration.

## Downloadable Files

| Filename | Description |
|---|---|
| `settings.cf2` | Device configuration backup |
| `diag.tar.gz` | Diagnostic archive (see [Diagnostics](diagnostics.md)) |
