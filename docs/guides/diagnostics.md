# Status & Diagnostics

## Querying Device Information

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

system_name = dev.status("system_name")
print(f"System name: {system_name}")

imageversion = dev.status("imageversion")
print(f"Firmware version: {imageversion}")

cpustat = dev.status("cpustat")
print(f"CPU stats: {cpustat}")

serial = dev.status("redbootserial")
print(f"Serial number: {serial}")

hardware = dev.status("redbootproduct")
print(f"Hardware revision: {hardware}")

dev.logout()
```

## Status with Parameters

Some status properties accept parameters:

```python
# Ping a host 3 times
ping_result = dev.status("ping4", "127.0.0.1", "3")
print(f"Ping result: {ping_result}")
```

## Downloading Diagnostic Archive

The diagnostic archive (`diag.tar.gz`) contains system information including CPU, memory, network, and temperature data.

```python
from datetime import datetime

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Trigger diagnostic generation
dev.config_set_commit({"generate_diag_now": "1"})

# Build a descriptive filename
system_name = dev.status("system_name")
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
output_filename = f"diag_{system_name}_{timestamp}.tar.gz"

# Download
dev.download_file("diag.tar.gz", output_filename)
print(f"Downloaded: {output_filename}")

dev.logout()
```

!!! tip
    The diagnostic archive is generated on-demand. Always call `config_set_commit({"generate_diag_now": "1"})` before downloading to ensure you get current data.
