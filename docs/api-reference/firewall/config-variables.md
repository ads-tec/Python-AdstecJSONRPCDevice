# Configuration Variables (Firewalls)

!!! info "Firewall models only"
    The configuration variables on this page apply to **IRF1000, IRF2000, and IRF3000** firewalls only. For variables available on all devices, see [Configuration Variables](../config-variables.md).

---

## OpenVPN

### General Connection Configuration

| Variable | Values | Description |
|---|---|---|
| `vpn_list_n` (n: 0-10) | slash-separated string | VPN connection definition. Format: `"OpenVPN/Client\|Master/TCP\|UDP/DestIP:Port:Proto/ListenPort/CertName/tapN/active\|deactive\|switched"`. Index 10 is reserved for Big-LinX |
| `vpn_proxy` | `"enabled"` / `"disabled"` | Use HTTP proxy for OpenVPN client connections |
| `vpn_proxyip` | IP or hostname | Proxy address |
| `vpn_proxyport` | TCP port | Proxy port |
| `vpn_proxyauthmeth` | `"ntlm"` / `"basic"` / `"none"` | Proxy authentication method |
| `vpn_proxyuser` | string | Proxy username |
| `vpn_proxypass` | string | Proxy password |

### Client-Specific OpenVPN

| Variable | Values | Description |
|---|---|---|
| `vpn_clientpull_status` | `"enabled"` / `"disabled"` | Activate DHCP on VPN client interface |
| `vpn_clientpull_routes` | `"enabled"` / `"disabled"` | Retrieve routing info from VPN master |
| `vpn_clientpull_dev` | `"tap0"` - `"tap9"` | Interface for clientpull options |

### Master-Specific OpenVPN

| Variable | Values | Description |
|---|---|---|
| `vpn_ippool_status` | `"enabled"` / `"disabled"` | Activate IP assignment to clients |
| `vpn_ippool_startip` | IP address | Start of client IP range |
| `vpn_ippool_endip` | IP address | End of client IP range |
| `vpn_ippool_masterdev` | `"tap0"` - `"tap9"` | Interface for IP pool |
| `vpn_ippool_pushgw` | `"enabled"` / `"disabled"` | Push master IP as default gateway to clients |
| `vpn_ippool_pushsubnet` | `"enabled"` / `"disabled"` | Push static routes to clients |

### Manual VPN Switching

Requires VPN connection configured in `"switched"` state.

| Variable | Values | Description |
|---|---|---|
| `vpn_switch_on` | `"0"` - `"10"` | VPN connection index to activate |
| `vpn_switch_off` | `"0"` - `"10"` | VPN connection index to deactivate |
| `vpn_switch_now` | any | Trigger: execute the switch. Clears `vpn_switch_on`/`vpn_switch_off` afterwards |

---

## CUT & ALARM

| Variable | Values | Description |
|---|---|---|
| `cutsignal_mode` | `"manual"` / `"auto"` | Manual or automatic CUT signal confirmation |
| `alarmsignal_mode` | `"manual"` / `"auto"` | Manual or automatic ALARM signal confirmation |
| `cutsignal_timeout` | seconds | Auto-confirm timeout for CUT signal |
| `alarmsignal_timeout` | seconds | Auto-confirm timeout for ALARM signal |
| `cutsignal_ack_now` | any | Trigger: immediately cancel CUT signal |
| `alarmsignal_ack_now` | any | Trigger: immediately cancel ALARM signal |
| `cutsignal_cut_now` | any | Trigger: activate CUT signal |
| `alarm_signal_alarm_now` | any | Trigger: activate ALARM signal |
| `cutandalrm_reset` | `"true"` / `"false"` | Auto-acknowledge CUT/ALARM if triggered by client monitoring |
| `vpn_ovpn_enable_on_cut` | `"true"` / `"false"` | Activate/deactivate "switched" OpenVPN connections when CUT signal changes |
| `vpn_ovpn_enb_on_cut_type` | `"enabled"` / `"disabled"` | `"enabled"` = connect on CUT activation; `"disabled"` = connect on CUT deactivation |

---

## GPIO Automatic Control

| Variable | Values | Description |
|---|---|---|
| `gpio_cut_auto` | `"enabled"` / `"disabled"` | Automatic CUT LED/signal control |
| `gpio_alarm_auto` | `"enabled"` / `"disabled"` | Automatic ALARM signal control |
| `gpio_vpn_auto` | `"enabled"` / `"disabled"` | Automatic VPN LED/signal control |

---

## Packet Filter

| Variable | Values | Description |
|---|---|---|
| `l3_forward` | any | Trigger: reload Layer 3 (iptables) packet filter rules from database. Any value change triggers the reload; using `str(int(time.time()))` is a convenient way to ensure a unique value |
| `l2_forward` | any | Trigger: reload Layer 2 (ebtables) packet filter rules from database. Same behavior as `l3_forward` |

!!! warning "Required after table changes"
    Modifying the packet filter tables (`services`, `serv_Protocols`, `selected_services`) does **not** automatically reload the running filter. You must write to `l3_forward` (for L3 rules) or `l2_forward` (for L2 rules) to apply changes. See the [Packet Filter guide](../../guides/packet-filter/index.md#applying-changes) for details.

---

## 3G/4G (UMTS/LTE)

!!! note
    Despite the `umts_` prefix, all variables apply to LTE as well.

| Variable | Values | Description |
|---|---|---|
| `umts_service` | `"enabled"` / `"disabled"` | Activate 3G/4G service |
| `umts_apn` | string | Provider APN (e.g., `"web.vodafone.de"`) |
| `umts_user` | string | Provider username |
| `umts_pass` | string | Provider password |
| `umts_apn2` | string | Fallback APN |
| `umts_user2` | string | Fallback username |
| `umts_pass2` | string | Fallback password |
| `umts_dns` | `"enabled"` / `"disabled"` | Obtain DNS server via 3G/4G |
| `umts_pin` | string | SIM card PIN |
| `umts_puk` | string | SIM card PUK (for unblocking) |
| `umts_permalink` | `"enabled"` / `"disabled"` | Maintain permanent connection |
| `umts_ondemand` | `"enabled"` / `"disabled"` | On-demand dialling (`umts_permalink` must be disabled) |
| `umts_connect_now` | any | Trigger: manually connect (only with `ondemand`) |
| `umts_disconnect_now` | any | Trigger: manually disconnect (only with `ondemand`) |
| `umts_bands_2G` | space-separated list or `"any"` | 2G band selection (use band names from `umts_supported_bands_json` status) |
| `umts_bands_3G` | space-separated list or `"any"` | 3G band selection |
| `umts_bands_4G` | space-separated list or `"any"` | 4G band selection |
