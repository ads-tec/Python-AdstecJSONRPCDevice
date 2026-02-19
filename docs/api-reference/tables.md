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

!!! warning "Integer `id` columns require explicit values"
    Tables with an integer `id` primary key (e.g. `services`, `serv_Protocols`, `selected_services`) do **not** support auto-increment. Passing `""` or `"0"` for the `id` field causes a `"datatype mismatch"` error at commit. Always provide a unique non-zero integer.

    **Custom entries must use IDs starting at `1000` or higher.** IDs below 1000 are reserved for factory defaults. Rules inserted with lower IDs may not appear in the device web UI and can conflict with firmware updates that add new factory defaults.

    Alternatively, use `config.import_config` with `tableinsert` which uses the same dict format as `export_pages` output — but the same `id` rule applies.

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
