# User Management

## Creating a New User

User creation requires two steps within a single configuration session:

1. Insert a row into the `users` table
2. Set the password for the new user

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

new_username = "testuser"
new_password = "SecurePassword123!"

# Both operations must happen in the same session
cfg_session_id = dev.sess_start()

# 1. Create the user entry
dev.table_insert("users", cfg_session_id,
    [new_username, "", "", "1", "", "1970-01-01", "1970-01-01"])

# 2. Set the password
dev.config_set(cfg_session_id, {
    "webpwd_user": new_username,
    "webpwd_user_new": new_password,
    "webpwd_user_checked": new_password
})

# Apply
dev.sess_commit(cfg_session_id)
dev.logout()
```

### User Row Format

| Index | Field | Example | Description |
|---|---|---|---|
| 0 | username | `"testuser"` | Login username |
| 1 | (reserved) | `""` | |
| 2 | (reserved) | `""` | |
| 3 | enabled | `"1"` | `"1"` = enabled, `"0"` = disabled |
| 4 | (reserved) | `""` | |
| 5 | created | `"1970-01-01"` | Account creation date |
| 6 | expires | `"1970-01-01"` | Account expiration date |

## Verify the New Account

```python
# Log in as the new user
dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", new_username, new_password)
version = dev.status("imageversion")
print(f"Logged in as {new_username}, firmware: {version}")
dev.logout()
```
