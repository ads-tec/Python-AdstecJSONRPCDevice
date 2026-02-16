# Status Properties (Firewalls)

!!! info "Firewall models only"
    The status properties on this page apply to **IRF1000, IRF2000, and IRF3000** firewalls only. For properties available on all devices, see [Status Properties](../status-properties.md).

---

## OpenVPN

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `vpnconnstat` | `tap0` - `tap9` | `"up"` / `"down"` | VPN connection status for a specific interface |
| `vpnclients` | `tap0` - `tap9` | number | Number of connected clients on a VPN interface |

---

## CUT & ALARM

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `alarm` | — | `"off"` / `"on"` | ALARM signal state |
| `intcut` | — | `"off"` / `"on"` | Internal CUT signal state |
| `extcut` | — | `"off"` / `"on"` | External CUT signal state |

---

## 3G/4G (UMTS/LTE)

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `umts_multistat` | — | multiline string | Full detailed UMTS/LTE module status |
| `umts_iccid` | — | string | SIM card ICCID; `"Error"` if no card |
| `umts_pinstate` | — | string | `"READY"` if PIN correct; `"bad pin"` if incorrect |
| `umts_signal` | — | dBm value | Reception strength in dBm |
| `umts_regstate` | — | `"0"` - `"5"` | Registration state: `0` = not registered; `1` = home network; `2` = searching; `3` = denied; `4` = unknown; `5` = roaming |
| `umts_localip` | — | IP address | Device IP if connected |
| `umts_remoteip` | — | IP address | Remote station IP |
| `umts_operator` | — | string | Operator name (e.g., `"vodafone.de"`); `"0"` on error |
| `umts_stat` | — | string | Connection status: `"connected"` / `"standby - connect on demand"` / `"not connected"` / `"connecting..."` |
| `umts_serving_system` | — | JSON object | Contains: `registration`, `plmn_mcc`, `plmn_mnc`, `plmn_description`, `roaming` |
| `umts_supported_bands_json` | — | JSON object | Nested object with `"2G"` / `"3G"` / `"4G"` keys, each containing band-name:value pairs. Band names are valid values for `umts_bands_*` config variables |

---

## GNSS / GPS

| Property | Parameters | Returns | Description |
|---|---|---|---|
| `gnss_devices` | — | string | List of GNSS modems |
| `gnss_tpv` | — | JSON object | Position data: `time` (ISO8601), `lat`, `lon`, `alt` (meters), `track` (m/s) |
| `gnss_sky` | — | JSON array | Received satellites. Each entry has `PRN` (satellite ID) |
