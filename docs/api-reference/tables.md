# Tables

Some device data is stored in tables rather than flat configuration variables. Use the table operations to read, insert, update, and delete rows.

## Table Operations

### Read a Row

```python
row = dev.table_get("users", "username", "admin")
```

### Insert a Row

```python
cfg_session_id = dev.sess_start()
dev.table_insert("users", cfg_session_id, ["newuser", "", "", "1", "", "1970-01-01", "1970-01-01"])
dev.sess_commit(cfg_session_id)
```

### Update a Row

```python
cfg_session_id = dev.sess_start()
dev.table_up("users", cfg_session_id,
    condition={"username": "testuser"},
    values={"enabled": "1"}
)
dev.sess_commit(cfg_session_id)
```

### Delete a Row

```python
cfg_session_id = dev.sess_start()
dev.table_del("users", cfg_session_id,
    condition={"username": "testuser"}
)
dev.sess_commit(cfg_session_id)
```

### Query Semantics

- `condition` supports up to **2 key-value pairs** (AND logic)
- Example: `{"username": "guest", "enabled": "0"}` matches rows where both conditions are true
- Non-existing variables return empty string, not an error

---

## Known Tables

### `users` — User Accounts

Row format for `table_insert` (all columns required):

| Index | Field | Example | Description |
|---|---|---|---|
| 0 | username | `"testuser"` | Login username |
| 1 | (reserved) | `""` | |
| 2 | (reserved) | `""` | |
| 3 | enabled | `"1"` | `"1"` = enabled, `"0"` = disabled |
| 4 | (reserved) | `""` | |
| 5 | created | `"1970-01-01"` | Account creation date |
| 6 | expires | `"1970-01-01"` | Account expiration date |

!!! note "Setting the password"
    After inserting a user row, set the password in the **same** configuration session:

    ```python
    cfg_session_id = dev.sess_start()
    dev.table_insert("users", cfg_session_id,
        ["testuser", "", "", "1", "", "1970-01-01", "1970-01-01"])
    dev.config_set(cfg_session_id, {
        "webpwd_user": "testuser",
        "webpwd_user_new": "SecurePassword123!",
        "webpwd_user_checked": "SecurePassword123!"
    })
    dev.sess_commit(cfg_session_id)
    ```

---

### `ipgroups` — Network Groups

Used for grouping IP subnets (e.g., for firewall rules).

| Column | Type | Constraint | Description |
|---|---|---|---|
| `name` | string (max 14 chars) | unique with `network` | Name of the network group |
| `network` | IP/mask | unique with `name` | Subnet (e.g., `"192.168.1.0/24"`) |

```python
cfg_session_id = dev.sess_start()
dev.table_insert("ipgroups", cfg_session_id, ["office", "192.168.1.0/24"])
dev.table_insert("ipgroups", cfg_session_id, ["office", "10.0.0.0/8"])
dev.sess_commit(cfg_session_id)
```

---

### `macgroups` — Hardware Groups

Used for grouping devices by MAC address.

| Column | Type | Constraint | Description |
|---|---|---|---|
| `name` | string (max 14 chars) | unique with `hwaddr` | Name of the hardware group |
| `hwaddr` | MAC address | unique with `name` | Hardware address (e.g., `"00:10:20:45:67:89"`) |

```python
cfg_session_id = dev.sess_start()
dev.table_insert("macgroups", cfg_session_id, ["printers", "00:10:20:45:67:89"])
dev.sess_commit(cfg_session_id)
```

---

### `permissions` — User Rights

Controls per-user read/write access to configuration variables and tables.

| Column | Type | Constraint | Description |
|---|---|---|---|
| `username` | string (max 14 chars) | unique with `configid` | Username |
| `configid` | `"0"` / `"1"-"9999"` / table name | unique with `username` | `0` = default permissions; `1-9999` = config variable ID; table name (e.g., `"macgroups"`) = table access |
| `permission` | `"r"` / `"w"` | | `r` = read; `w` = read + write |

```python
cfg_session_id = dev.sess_start()
# Give user "operator" write access to config variable #42
dev.table_insert("permissions", cfg_session_id, ["operator", "42", "w"])
dev.sess_commit(cfg_session_id)
```
