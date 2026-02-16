# VPN Approval

## Overview

ads-tec firewalls support a VPN approval workflow where VPN connections must be explicitly approved before they are established. When set to `"api"` mode, this approval can be automated via the JSON-RPC API.

## VPN States

| State | Description |
|---|---|
| `WAITINGFORAPPROVAL` | VPN connection is pending approval |
| `CONNECTED` | VPN tunnel is established |

## Automated Approval Workflow

```python
import time
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# 1. Enable API-based approval (one-time setup)
dev.config_set_commit({"vpn_approval_mode": "api"})

# 2. Wait for a VPN connection request
vpn_state = ""
while vpn_state != "WAITINGFORAPPROVAL":
    vpn_state = dev.status("blxstat_vpnstate")
    print(f"VPN state: {vpn_state}")
    time.sleep(3)

# 3. Approve the connection
dev.config_set_commit({"vpn_approve_now": "1"})

# 4. Wait for connection to establish
while vpn_state != "CONNECTED":
    vpn_state = dev.status("blxstat_vpnstate")
    print(f"VPN state: {vpn_state}")
    time.sleep(1)

print("VPN connected")
dev.logout()
```

!!! tip
    Set `vpn_approval_mode` to `"api"` only once. It persists across reboots.
