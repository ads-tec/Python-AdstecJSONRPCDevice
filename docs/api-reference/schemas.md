# JSON Schemas

Machine-readable JSON Schema files are available in the [`schemas/`](https://github.com/ads-tec/Python-AdstecJSONRPCDevice/tree/main/schemas) directory of the repository. These can be used for request validation, code generation, or integration with other tools.

## Available Schemas

| File | Description |
|---|---|
| [`jsonrpc-envelope.schema.json`](#request-envelope) | Base JSON-RPC 2.0 request/response/error envelope |
| [`session.schema.json`](#session-authentication) | `session.create`, `session.list`, `session.destroy` |
| [`config.schema.json`](#config-configuration) | `config.get`, `config.get_values`, `config.get_default`, `config.set`, `config.export_pages`, `config.import_config`, session management, table operations |
| [`status.schema.json`](#status-device-status) | `status.get` with all known property names |
| [`gpio.schema.json`](#gpio-gpio-control-firewalls-only) | `gpio.list`, `gpio.get`, `gpio.get_bool`, `gpio.get_pulses`, `gpio.on`, `gpio.off` **(firewalls only)** |
| [`ipsec.schema.json`](#ipsec-vpn-firewalls-only) | `network.ipsec.control.up`, `network.ipsec.control.down` **(firewalls only)** |
| [`statusd.schema.json`](#big-linx-vpn-control) | `statusd.blx_status`, `statusd.blx_vpn_up`, `statusd.vpn_down` |
| [`blxpush.schema.json`](#big-linx-iiot-data-push) | `blxpush.status`, `blxpush.push` |
| [`file-rpc.schema.json`](#base64-file-transfer-json-rpc) | `file.write`, `file.read`, `file.delete` |
| [`zxcvbn.schema.json`](#zxcvbn-password-strength) | `zxcvbn.get` |
| [`file-transfer.schema.json`](#file-transfer-http) | HTTP upload/download endpoints (not JSON-RPC) |

---

## Request Envelope

All JSON-RPC calls use the same envelope. The top-level `method` is always `"call"` (or `"list"` to discover methods on an object), with `params` as a 4-element array:

```json
{
  "id": "req-1",
  "jsonrpc": "2.0",
  "method": "call",
  "params": [
    "<session_id>",
    "<object>",
    "<method>",
    { <method_parameters> }
  ]
}
```

Available objects: `session`, `config`, `status`, `gpio`, `network.ipsec.control`, `statusd`, `blxpush`, `file`, `zxcvbn`.

Successful responses return `result` as `[0, {data}]`. Non-zero first element indicates an error.

=== "Success"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "result": [0, {"imageversion": "2.2.6"}]
    }
    ```

=== "Error"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "error": {"code": -32000, "message": "error description"}
    }
    ```

---

## session — Authentication

### session.create

Authenticate and obtain a session ID. This is the **only** call that may use the null SID.

=== "Request"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "method": "call",
      "params": [
        "00000000000000000000000000000000",
        "session", "create",
        {"user": "admin", "password": "admin", "timeout": 600}
      ]
    }
    ```

=== "Response"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "result": [0, {"sid": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4", "acls": {}}]
    }
    ```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `user` | string | yes | Login username |
| `password` | string | yes | Login password |
| `timeout` | integer | no | Session timeout in seconds (default: 600) |

Returns `sid` (32-char hex) and `acls` (access rights for this user).

### session.list

List all active sessions on the device.

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "session", "list", {}]}
```

### session.destroy

Invalidate the current session (logout).

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "session", "destroy", {}]}
```

---

## config — Configuration

### config.sess_start

Start a configuration session. Returns `cfg_session_id`.

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "config", "sess_start", {}]}
```

### config.sess_commit

Commit all changes in the session atomically. On conflict, the entire config set is discarded.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cfg_session_id` | string | yes | Session ID from `sess_start` |

### config.sess_abort

Cancel a configuration session and discard all pending changes.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cfg_session_id` | string | yes | Session ID from `sess_start` |

### config.get

Read configuration variables. Non-existing variables return empty string.

=== "Request"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "method": "call",
      "params": ["<sid>", "config", "get",
        {"keys": ["lan_ipaddr", "timezone"]}]
    }
    ```

=== "Response"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "result": [0, {"result": [
        {"lan_ipaddr": "192.168.0.254"},
        {"timezone": "Europe/Berlin"}
      ]}]
    }
    ```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `keys` | string[] | yes | Configuration variable names |

### config.get_values

Extended read: returns default value, permissions, JSON-interpreted value, and raw string for each variable.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `keys` | string[] | yes | Configuration variable names |

### config.get_default

Get the firmware/product-specific default value for each variable.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `keys` | string[] | yes | Configuration variable names |

### config.export_pages

Export all settings for given page IDs. Output can be fed to `import_config`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pages` | string[] | yes | Page IDs to export |

### config.set

Write configuration variables (requires active session). Values are regex-validated; on failure the entire call is aborted.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cfg_session_id` | string | yes | Active session ID |
| `values` | object | yes | Key-value pairs to set |
| `verbose` | boolean | no | Return all validation errors instead of just the first (default: `true`) |

### config.import_config

Bulk import configuration. Does **not** require a config session. All-or-nothing — aborts on any error.

```json
{
  "id": "req-1",
  "jsonrpc": "2.0",
  "method": "call",
  "params": ["<sid>", "config", "import_config", {
    "jsondata": {
      "configdata": {"timezone": "Europe/Berlin"},
      "tableinsert": {},
      "tableupdate": {},
      "tabledelete": {}
    }
  }]
}
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `jsondata` | object | yes | Import payload with `configdata`, `tableinsert`, `tableupdate`, `tabledelete` |

### config.table_get

Read table rows matching a condition (max 2 keys, AND logic).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tablename` | string | yes | Table name (e.g. `"users"`, `"ipgroups"`, `"macgroups"`, `"permissions"`) |
| `condition` | object | yes | Match condition (max 2 keys) |

### config.table_set

Insert a new row (requires active session). All columns required.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tablename` | string | yes | Table name |
| `cfg_session_id` | string | yes | Active session ID |
| `row` | string[] | yes | Ordered array of field values |

### config.table_up

Update matching rows (requires active session).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tablename` | string | yes | Table name |
| `cfg_session_id` | string | yes | Active session ID |
| `condition` | object | yes | Match condition (max 2 keys) |
| `values` | object | yes | Fields to update |

### config.table_del

Delete matching rows (requires active session).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `tablename` | string | yes | Table name |
| `cfg_session_id` | string | yes | Active session ID |
| `condition` | object | yes | Match condition (max 2 keys) |

---

## status — Device Status

### status.get

Query a status property.

=== "Simple (no params)"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "method": "call",
      "params": ["<sid>", "status", "get",
        {"function": "imageversion", "parameters": ["", ""]}]
    }
    ```

=== "With parameters"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "method": "call",
      "params": ["<sid>", "status", "get",
        {"function": "ping4", "parameters": ["127.0.0.1", "3"]}]
    }
    ```

=== "Interface query"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "method": "call",
      "params": ["<sid>", "status", "get",
        {"function": "if_status", "parameters": ["eth0", ""]}]
    }
    ```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `function` | string | yes | Status property name |
| `parameters` | string[] | no | Up to 2 optional parameters (default: `["", ""]`) |

---

## gpio — GPIO Control (Firewalls Only)

!!! note
    Available on firewall models (IRF1000, IRF2000, IRF3000) only. See [JSON-RPC Methods (Firewalls)](firewall/jsonrpc-methods.md).

All GPIO methods use `dev.call("gpio", "<method>", signal="<name>")`.

| Method | Parameters | Description |
|---|---|---|
| `list` | — | List all GPIO signals |
| `get` | `signal` | Get signal value |
| `get_bool` | `signal` | Get boolean state |
| `get_pulses` | `signal` | Get pulse count (rising + falling edges; 1 button press = 2) |
| `on` | `signal` | Activate signal |
| `off` | `signal` | Deactivate signal |

---

## IPsec VPN (Firewalls Only)

!!! note
    Available on firewall models (IRF1000, IRF2000, IRF3000) only. The IPsec policy must be configured as "Active (Switched)" before it can be controlled via API. See [JSON-RPC Methods (Firewalls)](firewall/jsonrpc-methods.md).

| Method | Parameters | Description |
|---|---|---|
| `up` | policy identifier | Activate an IPsec policy |
| `down` | policy identifier | Deactivate an IPsec policy |

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "network.ipsec.control", "up", {}]}
```

---

## Big-LinX VPN Control

### statusd.blx_status

Full Big-LinX diagnostic status.

=== "Request"
    ```json
    {"id": "req-1", "jsonrpc": "2.0", "method": "call",
     "params": ["<sid>", "statusd", "blx_status", {}]}
    ```

=== "Response"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "result": [0, {
        "cardstate": "VPNSC_CS_READY",
        "tokenlabel": "device-001.biglinx.cloud",
        "vpn_state_name": "CONNECTED",
        "vpn_ip": "10.8.0.5",
        "vpn_server_ip": "203.0.113.1:1194",
        "vpn_ctrl_state": 1
      }]
    }
    ```

| Field | Type | Description |
|---|---|---|
| `cardstate` | string | Smart card state. `"VPNSC_CS_READY"` = VPN can be activated |
| `tokenlabel` | string | Common Name of Big-LinX X.509 certificate |
| `vpn_state_name` | string | Current OpenVPN state |
| `vpn_ip` | string | VPN interface IP (empty if down) |
| `vpn_server_ip` | string | VPN server public IP and port |
| `vpn_ctrl_state` | integer | Target state: `1` = should be up, `0` = should be down |

### statusd.blx_vpn_up / statusd.vpn_down

Start or stop the Big-LinX VPN connection.

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "statusd", "blx_vpn_up", {}]}
```

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "statusd", "vpn_down", {}]}
```

---

## Big-LinX IIoT Data Push

!!! note
    Requires Big-LinX connection configured and Big-LinX IoT feature enabled.

### blxpush.status

Get connection state and buffer status.

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "blxpush", "status", {}]}
```

### blxpush.push

Push measurement data to the Big-LinX database.

=== "Request"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "method": "call",
      "params": ["<sid>", "blxpush", "push", {
        "measurement": "temperature",
        "tags": ["sensor1"],
        "values": [{"ts": 1708099200000, "temp_celsius": 23.5}]
      }]
    }
    ```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `measurement` | string | yes | Measurement name in the Big-LinX database |
| `tags` | string[] | yes | Additional tags for the data |
| `values` | object[] | yes | Data points. Each must include `ts` (millisecond timestamp) plus key-value pairs of integer/float data |

---

## Base64 File Transfer (JSON-RPC)

Upload and download files via JSON-RPC using Base64 encoding. Alternative to the HTTP file transfer endpoints.

### file.write

Upload a Base64-encoded file.

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "file", "write",
   {"path": "/tmp/upcerts", "data": "<base64-encoded-content>"}]}
```

### file.read

Download a file as Base64.

=== "Request"
    ```json
    {"id": "req-1", "jsonrpc": "2.0", "method": "call",
     "params": ["<sid>", "file", "read",
       {"path": "/tmp/root/settings.cf2"}]}
    ```

=== "Response"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "result": [0, {"data": "<base64-encoded-content>"}]
    }
    ```

### file.delete

Delete a file to free RAM.

```json
{"id": "req-1", "jsonrpc": "2.0", "method": "call",
 "params": ["<sid>", "file", "delete",
   {"path": "/tmp/root/settings.cf2"}]}
```

### Allowed Paths

| Path | Operations | Purpose |
|---|---|---|
| `/tmp/upsettigs` | write | Settings (.cf2) upload |
| `/tmp/upcerts` | write | Certificate upload |
| `/tmp/root/settings.cf2` | read, delete | Settings download |

---

## zxcvbn — Password Strength

### zxcvbn.get

=== "Request"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "method": "call",
      "params": ["<sid>", "zxcvbn", "get",
        {"password": "1H_$X%rIjg(EIu+ecw9VCZ+T"}]
    }
    ```

=== "Response"
    ```json
    {
      "id": "req-1",
      "jsonrpc": "2.0",
      "result": [0, {"entropy": 132.7}]
    }
    ```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `password` | string | yes | Password to evaluate |

**Threshold:** entropy >= 75.0 = strong password.

---

## File Transfer (HTTP)

File upload and download use **HTTP endpoints**, not JSON-RPC. Authentication is via the `ads_sid` cookie (session ID from `session.create`).

### Upload

`POST https://<device-ip>/priv/script/php_rpc/upload.php`

- Content-Type: `multipart/form-data`
- Cookie: `ads_sid=<session_id>`
- Form field name = file type, value = file binary

| File Type | Description |
|---|---|
| `firmware` | Firmware binary — triggers reboot |
| `bootlogo` | Custom boot logo |
| `settings` | Settings backup (.cf2) |
| `customer_settings` | Customer-specific settings |
| `cert` | Certificate (CA, server, client PEM) |
| `wwan_update` | WWAN modem firmware |

### Download

`GET https://<device-ip>/priv/script/php_rpc/download.php?file=<filename>`

- Cookie: `ads_sid=<session_id>`

| Filename | Prerequisite | Description |
|---|---|---|
| `diag.tar.gz` | Set `generate_diag_now` = `"1"` first | Diagnostic archive |
| `settings.cf2` | Set `save_settings_now` = `"1"` first | Settings backup |
