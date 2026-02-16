# Configuration Variables

Configuration variables are read with `config.get()` and written with `config.set()` within a configuration session.

## Reading Configuration

```python
result = dev.config_get(["lan_ipaddr", "timezone", "ntp_service"])
```

## Writing Configuration

```python
dev.config_set_commit({"timezone": "Europe/Berlin", "ntp_service": "enabled"})
```

---

## Operation Mode

| Variable | Values | Description |
|---|---|---|
| `opmode` | `"transbridge"` / `"iprouter"` / `"iprouter5port"` | Device operation mode. `transbridge` = Layer 2 managed switch; `iprouter` = Layer 3 LAN/WAN; `iprouter5port` = Layer 3 all ports with independent IPs |

!!! warning
    Changing `opmode` has side effects on filter rules and static routes.

---

## Network

### Interface Configuration

Interface variables use a prefix pattern: `(wan|lan|lan_port1|lan_port2|lan_port3|lan_port4)_<variable>`.

| Variable | Values | Description |
|---|---|---|
| `(wan\|lan\|lan_port[1-4])_proto` | `"static"` / `"dhcp"` / `"dhcpstatic"` / `"dhcpovpn"` / `"pppoedyn"` | Interface protocol. `static` = manual config; `dhcp` = dynamic; `dhcpstatic` = DHCP with static fallback; `dhcpovpn` = IP via OpenVPN tunnel; `pppoedyn` = PPPoE for DSL |
| `(wan\|lan\|lan_port[1-4])_ipaddr` | IP address | Interface IP address (e.g., `"192.168.0.254"`) |
| `(wan\|lan\|lan_port[1-4])_netmask` | Netmask | Interface subnet mask (e.g., `"255.255.255.0"`) |
| `lan_gateway` | IP address | Default gateway (applies to all interfaces despite the `lan_` prefix) |
| `splitbridge_port[1-4]` | `"enabled"` / `"disabled"` | In `iprouter5port` mode: whether LAN-out port forms a bridge with LAN-in |

!!! warning "IP Address Changes"
    When changing `lan_ipaddr`, use `config_set_commit_with_ip_change()` in the Python reference implementation. The device becomes unreachable at the old IP after the change. See [Networking Guide](../guides/networking.md).

### DNS

| Variable | Values | Description |
|---|---|---|
| `dns1` | IP address | Primary DNS server |
| `dns2` | IP address | Secondary DNS server |
| `dns3` | IP address | Tertiary DNS server |
| `dns_domain` | string | Local network subdomain (e.g., `"intranet.company.de"`). Auto-appended to bare hostname DNS queries |
| `dns_request_all` | `"enabled"` / `"disabled"` | Query all DNS servers simultaneously (otherwise sequential with timeout fallover) |
| `dns_proxy` | `"enabled"` / `"disabled"` | Activate DNS relay service on device |
| `gw_dhcp_interface` | interface name or `""` | Which DHCP interface provides the default gateway |
| `dns_dhcp_interface` | interface name or `""` | Which DHCP interface provides DNS settings |

### PPPoE (DSL)

| Variable | Values | Description |
|---|---|---|
| `wan_pppoe_userid` | string | DSL user ID |
| `wan_pppoe_password` | string | DSL password |

---

## Date & Time

| Variable | Values | Description |
|---|---|---|
| `timezone` | string | Timezone (e.g., `"Europe/Berlin"`). Query `timezone_list` status for available values |
| `ntp_service` | `"enabled"` / `"disabled"` | Enable NTP time synchronization |
| `ntp_relay` | `"enabled"` / `"disabled"` | Enable NTP relay (device acts as NTP server) |
| `ntp_server` | string | Primary NTP server |
| `ntp_server2` | string | Secondary NTP server |
| `ntp_server3` | string | Tertiary NTP server |
| `day` | string | Day of month, zero-padded (e.g., `"01"`) — only when NTP is disabled |
| `month` | string | Month, zero-padded (e.g., `"01"`) |
| `year` | string | Year (e.g., `"2026"`) |
| `hour` | string | Hour, zero-padded (e.g., `"00"`) |
| `minute` | string | Minute, zero-padded (e.g., `"00"`) |
| `second` | string | Second, zero-padded (e.g., `"00"`) |

---

## Password & Authentication

| Variable | Values | Description |
|---|---|---|
| `webpwd_user` | string | Username for the password change operation |
| `webpwd_user_old` | string | Current password (required when changing own password) |
| `webpwd_user_new` | string | New password |
| `webpwd_user_checked` | string | New password confirmation (must match `webpwd_user_new`) |
| `password_mode` | string | Password hashing mode (e.g., `"argon2"`) |
| `password_policy` | `"enabled"` / `"disabled"` | Enable password policy enforcement |

---

## Firewall-Only Variables

OpenVPN, CUT & ALARM, GPIO Automatic Control, and 3G/4G UMTS/LTE variables are available on firewall models only. See [Configuration Variables (Firewalls)](firewall/config-variables.md).

---

## Big-LinX

### Connection Configuration

| Variable | Values | Description |
|---|---|---|
| `vpn_list_10` | slash-separated string | Big-LinX VPN connection. Last field: `"active"` (permanent) or `"switched"` (triggered remotely) |
| `vpn_ida_proxy` | `"enabled"` / `"disabled"` | HTTP proxy for Big-LinX |
| `vpn_ida_proxyip` | IP or hostname | Proxy address |
| `vpn_ida_proxyport` | TCP port | Proxy port |
| `vpn_ida_proxyauth` | `"ntlm"` / `"basic"` / `"none"` | Proxy auth method |
| `vpn_ida_proxyuser` | string | Proxy username |
| `vpn_ida_proxypass` | string | Proxy password |

### Smart Card

| Variable | Values | Description |
|---|---|---|
| `sc_autopin` | `"enabled"` / `"disabled"` | Autopin for smart cards |
| `sc_savepin` | `"enabled"` / `"disabled"` | Must be `"enabled"` for cards without autopin |
| `sc_pin` | string | Big-LinX smart card PIN. **Legacy only** — older cards required a manually configured PIN. Current cards use auto-PIN and do not need this variable |

### Approval Mode (4-Eyes Principle)

| Variable | Values | Description |
|---|---|---|
| `vpn_approval_mode` | `"disabled"` / `"vpnswitch"` / `"api"` | `"vpnswitch"` = physical key switch required; `"api"` = remote acknowledgement via API |
| `vpn_approve_now` | any | Trigger: approve a pending VPN connection |

---

## SCEP (Certificate Enrollment)

| Variable | Values | Description |
|---|---|---|
| `scep_service` | `"enabled"` / `"disabled"` | Activate SCEP service |
| `scep_url` | URL | SCEP server API URL |
| `scep_sncn` | `"enabled"` / `"disabled"` | Include device serial number in certificate CN |
| `scep_subject` | formatted string | Format: `"dns:NAME/C=DE, O=ads-tec"` |
| `scep_autocrl` | `"enabled"` / `"disabled"` | Automatic CRL retrieval from SCEP server |
| `scep_autorenew` | number of days | Auto-renew certificate N days before expiry |
| `scep_keybits` | `"1024"` / `"2048"` / `"3072"` / `"4096"` | Key length for certificate |
| `scep_challenge` | string | One-time challenge password for SCEP server |

---

## Certificates

| Variable | Values | Description |
|---|---|---|
| `to_be_deleted` | string | Path of certificate to delete (e.g., `"ca/cert.pem"`) |
| `cert_delete` | `"1"` | Trigger certificate deletion |
| `upload_cert_file_now` | any | Trigger: process an uploaded certificate file |
| `upload_cert_file_sha256` | SHA256 hex string | SHA256 checksum of the uploaded certificate file |
| `filename_password` | string | Passphrase for password-protected p12/pem files |

---

## Web Terminal Variables

Web Panel configuration variables are available on web terminals only. See [Configuration Variables (Web Terminals)](terminal/config-variables.md).

---

## Remote Capture (rpcap)

| Variable | Values | Description |
|---|---|---|
| `rpcap_status` | `"enabled"` / `"disabled"` | Enable remote packet capture |
| `rpcap_hostlist` | string | Comma-separated list of allowed capture hosts |
| `rpcap_access` | string | Space-separated native interface names to block from capture |

---

## Web Server

| Variable | Values | Description |
|---|---|---|
| `service_https` | `"enabled"` / `"disabled"` | HTTPS access on port 443 |
| `service_http` | `"enabled"` / `"disabled"` | If disabled, both HTTPS (443) and HTTP (80) are disabled |
| `service_http_port` | TCP port | HTTP port (default: `"80"`). HTTPS 443 is unaffected |

---

## System

### General

| Variable | Values | Description |
|---|---|---|
| `system_name` | string | Device system name (default: product name) |
| `system_contact` | string | Contact information |
| `systemname_sndyn` | `"enabled"` / `"disabled"` | Use serial number as system name |
| `hostname` | string | Network hostname (default: product name) |
| `hostname_sndyn` | `"enabled"` / `"disabled"` | Use serial number as hostname |
| `nvram_mode` | `"save"` / `"commit"` | `"save"` = changes saved persistently, applied after reboot; `"commit"` = changes applied immediately, saved only after `save_now` |

### Firmware Update from Server

| Variable | Values | Description |
|---|---|---|
| `update_proto` | `"http"` / `"ftp"` / `"tftp"` | Protocol for firmware download |
| `update_server` | IP address | Server providing the firmware |
| `update_restoredefaults` | `"enabled"` / `"disabled"` | Reset to factory defaults after firmware install |
| `fw_update_now` | any | Trigger: start firmware update |

### Reboot & Watchdog

| Variable | Values | Description |
|---|---|---|
| `reboot_now` | any | Trigger: system reboot (immediately, or after `reboot_wait` minutes) |
| `reboot_wait` | minutes | Wait time before reboot. Set to `"0"` to cancel a running timer |
| `firmware_switch_now` | any | Trigger: activate switchover to alternative firmware on next reboot |

### Settings Backup & Restore

| Variable | Values | Description |
|---|---|---|
| `save_now` | any | Trigger: save running config to NVRAM |
| `save_settings_now` | any | Trigger: prepare settings.cf2 for download |
| `restore_settings_now` | any | Trigger: parse an uploaded .cf2 settings file |
| `restore_settings_sha256` | SHA256 hex string | SHA256 checksum of the uploaded .cf2 file |

### Diagnostics

| Variable | Values | Description |
|---|---|---|
| `generate_diag_now` | `"1"` | Trigger: generate diagnostic archive for download |
