# JSON-RPC Methods

This page documents the JSON-RPC 2.0 methods available on ads-tec Industrial IT devices. The Python reference implementation wraps these methods for convenience, but any HTTP client that can send JSON-RPC requests can use this API.

## Protocol

All requests are sent as `POST https://<device-ip>/rpc` with `Content-Type: application/json`.

### Request Format

```json
{
    "id": "req-1",
    "jsonrpc": "2.0",
    "method": "call",
    "params": ["<session_id>", "<object>", "<method>", {<parameters>}]
}
```

Use `"method": "list"` instead of `"call"` to get a description of an object and its available methods.

### Response Format

```json
{
    "id": "req-1",
    "jsonrpc": "2.0",
    "result": [0, {<result_data>}]
}
```

The first element of `result` is the return code (`0` = success). The second element contains the response data.

### Error Response

```json
{
    "id": "req-1",
    "jsonrpc": "2.0",
    "error": {"code": -32000, "message": "error description"}
}
```

---

## Available Objects

| Object | Description |
|---|---|
| `session` | Authentication and session management |
| `config` | Configuration read/write and table operations |
| `status` | Device status queries |
| `gpio` | LEDs, buttons, digital I/O — **[firewalls only](firewall/jsonrpc-methods.md#gpio-gpio-control)** |
| `network.ipsec.control` | IPsec VPN tunnel control — **[firewalls only](firewall/jsonrpc-methods.md#networkipseccontrol-ipsec-vpn)** |
| `statusd` | Big-LinX VPN control |
| `blxpush` | Big-LinX IIoT dashboard data push |
| `file` | Base64 file upload/download via JSON-RPC |
| `zxcvbn` | Password strength checking |

---

## `session` — Authentication

| Method | Parameters | Description |
|---|---|---|
| `create` | `user`, `password`, `timeout` (optional) | Authenticate and get a session ID |
| `list` | — | List all active sessions |
| `destroy` | `sid` | Destroy a session (logout) |

`session.create` is the **only** call that may use the null SID `00000000000000000000000000000000`.

**Parameters for `create`:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `user` | string | yes | Username |
| `password` | string | yes | Password |
| `timeout` | integer | no | Session timeout in seconds (default: 600) |

**Response:** Returns `sid` (32-char hex string) and `acls` (access rights for this user).

**Python:**

```python
dev.get_sid()    # session.create
dev.logout()     # session.destroy
```

---

## `config` — Configuration

### Session Management

| Method | Parameters | Description |
|---|---|---|
| `sess_start` | — | Start a configuration session. Returns `cfg_session_id` |
| `sess_commit` | `cfg_session_id` | Commit and apply changes atomically |
| `sess_abort` | `cfg_session_id` | Cancel all changes in the session |

!!! note "All-or-Nothing"
    On conflict (e.g., invalid combination of settings), `sess_commit` discards the **entire** config set and returns an error.

### Read Operations

| Method | Parameters | Description |
|---|---|---|
| `get` | `keys` (list) | Read configuration variable values. Non-existing variables return empty string |
| `get_values` | `keys` (list) | Extended read: returns default value, permissions, JSON-interpreted value, and raw string |
| `get_default` | `keys` (list) | Get default value for each variable (firmware/product-specific) |
| `export_pages` | `pages` (list) | Export all settings for given page IDs. Output can be fed to `import_config` |

### Write Operations

| Method | Parameters | Description |
|---|---|---|
| `set` | `cfg_session_id`, `values` (dict), `verbose` (bool, optional) | Write configuration variables. Values are regex-validated; on failure the entire call is aborted. With `verbose=true`, returns all errors instead of just the first |
| `import_config` | `jsondata` (complex) | Bulk import: does NOT need a config session. All-or-nothing — aborts on any error |

**`import_config` structure:**

```json
{
    "jsondata": {
        "configdata": {"var1": "val1", "var2": "val2"},
        "tableinsert": { ... },
        "tableupdate": { ... },
        "tabledelete": { ... }
    }
}
```

### Table Operations

| Method | Parameters | Description |
|---|---|---|
| `table_get` | `tablename`, `condition` (dict, max 2 keys) | Read matching rows |
| `table_set` | `tablename`, `cfg_session_id`, `row` (array) | Insert a new row (all columns required) |
| `table_up` | `tablename`, `cfg_session_id`, `condition` (dict), `values` (dict) | Update matching rows |
| `table_del` | `tablename`, `cfg_session_id`, `condition` (dict) | Delete matching rows |

See [Tables](tables.md) for known table schemas.

**Python:**

```python
dev.sess_start()                          # config.sess_start
dev.sess_commit(cfg_session_id)           # config.sess_commit
dev.config_get(["lan_ipaddr", "timezone"])  # config.get
dev.config_set(cfg_session_id, values)    # config.set
dev.config_set_commit(values)             # sess_start + set + sess_commit
```

---

## `status` — Device Status

| Method | Parameters | Description |
|---|---|---|
| `get` | `function`, `parameters` (list, optional) | Query a status property |

**Python:**

```python
dev.status("imageversion")              # No parameters
dev.status("ping4", "127.0.0.1", "3")  # With parameters
```

See [Status Properties](status-properties.md) for the full list.

---

## Firewall-Only Methods

The `gpio` and `network.ipsec.control` objects are available on **firewall models** (IRF1000, IRF2000, IRF3000) only. See [JSON-RPC Methods (Firewalls)](firewall/jsonrpc-methods.md).

---

## `statusd` — Big-LinX VPN Control

| Method | Parameters | Description |
|---|---|---|
| `blx_status` | — | Full Big-LinX diagnostic status |
| `blx_vpn_up` | — | Start Big-LinX VPN connection |
| `vpn_down` | — | Stop Big-LinX VPN connection |

### `blx_status` Response Fields

| Field | Type | Description |
|---|---|---|
| `cardstate` | string | Smart card state. `"VPNSC_CS_READY"` = VPN can be activated |
| `tokenlabel` | string | Common Name of Big-LinX X.509 certificate |
| `vpn_state_name` | string | Current OpenVPN state (see [Big-LinX status values](status-properties.md#blxstat_vpnstate-values)) |
| `vpn_ip` | string | VPN interface IP (empty if down) |
| `vpn_server_ip` | string | VPN server public IP and port |
| `vpn_ctrl_state` | integer | Target state: `1` = should be up, `0` = should be down |

**Python:**

```python
blx = dev.call("statusd", "blx_status")
dev.call("statusd", "blx_vpn_up")
dev.call("statusd", "vpn_down")
```

---

## `blxpush` — Big-LinX IIoT Data Push

Push measurement data to the Big-LinX IIoT dashboard.

!!! note
    Requires Big-LinX connection configured and Big-LinX IoT feature enabled.

| Method | Parameters | Description |
|---|---|---|
| `status` | — | Connection state and buffer status |
| `push` | `measurement`, `tags`, `values` | Push data to Big-LinX database |

### `push` Parameters

| Parameter | Type | Description |
|---|---|---|
| `measurement` | string | Measurement name in the Big-LinX database |
| `tags` | array | Additional tags for the data |
| `values` | array of objects | Key-value pairs of integer/float data. Must include `"ts"` key with millisecond-resolution timestamp |

**Python:**

```python
status = dev.call("blxpush", "status")
dev.call("blxpush", "push",
    measurement="temperature",
    tags=["sensor1"],
    values=[{"ts": 1708099200000, "temp_celsius": 23.5}]
)
```

---

## `file` — Base64 File Transfer

Upload and download files via JSON-RPC using Base64 encoding. Alternative to the HTTP upload/download endpoints.

| Method | Parameters | Description |
|---|---|---|
| `write` | `path`, `data` | Upload a Base64-encoded file |
| `read` | `path` | Download a file as Base64 |
| `delete` | `path` | Delete a file to free RAM |

### Allowed Paths

| Path | Purpose |
|---|---|
| `/tmp/upsettigs` | Settings (.cf2) upload |
| `/tmp/upcerts` | Certificate upload |
| `/tmp/root/settings.cf2` | Settings download (read/delete only) |

**Python:**

```python
import base64

# Upload a certificate via JSON-RPC
with open("cert.pem", "rb") as f:
    data = base64.b64encode(f.read()).decode()
dev.call("file", "write", path="/tmp/upcerts", data=data)

# Download settings via JSON-RPC
result = dev.call("file", "read", path="/tmp/root/settings.cf2")
# result["data"] contains Base64-encoded content
```

---

## `zxcvbn` — Password Strength

| Method | Parameters | Description |
|---|---|---|
| `get` | `password` | Check password strength, returns `entropy` score |

**Threshold:** entropy >= 75.0 = strong password.

**Python:**

```python
result = dev.call("zxcvbn", "get", password="mypassword")
entropy = result["entropy"]
```

---

## Raw Call Example

For any method, use `dev.call()` directly:

```python
# dev.call(object, method, **params)
result = dev.call("gpio", "get_bool", signal="DI2")
```

This sends:

```json
{
    "id": "req-1",
    "jsonrpc": "2.0",
    "method": "call",
    "params": ["<sid>", "gpio", "get_bool", {"signal": "DI2"}]
}
```
