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

## Table Reference

For a complete list of all tables with column definitions, validation rules, and factory defaults, see the per-product Configuration Database reference:

| Product | Reference |
|---|---|
| AWT1000 (Web Terminal) | [AWT1000 Configuration Database](configdb/AWT1000.md) |
| IRF1401 | [IRF1401 Configuration Database](configdb/IRF1401.md) |
| IRF1421 | [IRF1421 Configuration Database](configdb/IRF1421.md) |
| IRF3401 | [IRF3401 Configuration Database](configdb/IRF3401.md) |
| IRF3421 | [IRF3421 Configuration Database](configdb/IRF3421.md) |
| IRF3801 | [IRF3801 Configuration Database](configdb/IRF3801.md) |
| IRF3821 | [IRF3821 Configuration Database](configdb/IRF3821.md) |

See also the [Configuration Database Overview](configdb/index.md) for a comparison across products.
