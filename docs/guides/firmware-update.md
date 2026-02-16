# Firmware Update

## Overview

ads-tec devices support two firmware update methods:

| Method | Trigger | Reboot | Use Case |
|---|---|---|---|
| [HTTP POST Upload](#method-1-http-post-upload) | Python `upload_file()` | Automatic | Simple, direct upload from a connected machine |
| [Server Pull (JSON-RPC)](#method-2-server-pull-via-json-rpc) | Config variable `fw_update_now` | Automatic | Device pulls from FTP/TFTP/HTTP server |

All methods flash to the secondary partition. The bootloader switches to the new firmware on reboot. Avoid power loss during flashing.

---

## Method 1: HTTP POST Upload

Upload a firmware binary directly to the device. The device reboots automatically after flashing completes. This is the method used by the ads-tec web interface.

```python
import jsonrpcdevice

host = "192.168.0.254"
username = "admin"
password = "admin"
firmware_filename = "Ads-tec-IRF3xxx-2.2.6-SVN-R63743.B-181926.bin"

dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, password)

# Check current version
initial_version = dev.status("imageversion")
print(f"Current firmware: {initial_version}")

# Upload firmware — device will reboot automatically
upload_result = dev.upload_file("firmware", firmware_filename)
print(f"Upload result: {upload_result}")

# Wait for device to reboot and finish booting
dev = jsonrpcdevice.wait_for_reboot(host, username, password, check_interval=3)

# Verify new version
new_version = dev.status("imageversion")
print(f"New firmware: {new_version}")

dev.logout()
```

### How `wait_for_reboot` Works

1. Monitors the device going **offline** (reboot started)
2. Waits for the device to come back **online** (HTTPS reachable)
3. Polls `boot_finished` status until it returns `"yes"`
4. Returns a new authenticated `AdstecJSONRPCDevice` instance

---

## Method 2: Server Pull via JSON-RPC

The device pulls a firmware image from an FTP, TFTP, or HTTP server that you control. Available on all IRF1000, IRF3000, and IRF2000 (firmware >= 2.5.0).

The device reboots automatically after flashing. Secondary services with high RAM usage may be shut down during download to free memory. There is no retry on network interruption.

!!! warning "Security"
    Firmware files are always encrypted and signed by ads-tec, so an unprotected transport link (plain HTTP, FTP, TFTP) does not expose firmware contents. However, this does **not** prevent a man-in-the-middle from serving an older, authentic ads-tec firmware that may have known security vulnerabilities (downgrade attack). Use a trusted network or authenticated transport where possible.

### Configuration Variables

| Variable | Values | Description |
|---|---|---|
| `update_proto` | `"http"` / `"ftp"` / `"tftp"` | Protocol for firmware download |
| `update_server` | IP or hostname | Server providing the firmware file |
| `update_restoredefaults` | `"enabled"` / `"disabled"` | Reset to factory defaults after update (default: disabled) |
| `fw_update_now` | any | Trigger: start firmware download and flash |

### Example

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Configure and trigger server-based update
dev.config_set_commit({
    "update_proto": "http",
    "update_server": "192.168.0.100",
    "fw_update_now": "1"
})

# Device will download firmware, flash it, and reboot automatically
dev = jsonrpcdevice.wait_for_reboot("192.168.0.254", "admin", "admin")

print(f"New firmware: {dev.status('imageversion')}")
dev.logout()
```

!!! note "Permissions"
    Which user accounts are allowed to trigger this method can be configured via the Permissions feature.

---

## Legacy: HTTP POST to netflash

!!! note
    This endpoint only exists on IRF firmware versions < 2.0.0 that do not yet have the newer `upload.php`. Firmware versions >= 2.0.0 no longer provide this endpoint — use [Method 1](#method-1-http-post-upload) instead.

For devices running firmware < 2.0.0, the firmware can be sent as an HTTP POST directly to the device's `netflash` CGI endpoint.

- Only the `admin` user account is allowed
- HTTP Digest authentication only

```bash
curl -v --digest -u admin:$password \
    https://$ip//cgi-bin/netflash?cgi://file, \
    -F file="@$filename"
```
