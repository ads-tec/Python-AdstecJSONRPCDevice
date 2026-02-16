# Password Management

## Password Strength Check

ads-tec devices include a built-in password strength checker based on the [zxcvbn](https://github.com/dropbox/zxcvbn) algorithm. Always validate a password **before** setting it — if the device has `password_policy` enabled, weak passwords will be rejected.

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

result = dev.call("zxcvbn", "get", password="weak123")
print(f"Entropy: {result['entropy']}")
# Entropy: ~25.0 (weak)

result = dev.call("zxcvbn", "get", password="1H_$X%rIjg(EIu+ecw9VCZ+T")
print(f"Entropy: {result['entropy']}")
# Entropy: >75.0 (strong)
```

### Strength Threshold

| Entropy | Strength |
|---|---|
| < 75.0 | Not strong enough |
| >= 75.0 | Strong |

### Helper Function

```python
def check_password_strength(dev, password):
    result = dev.call("zxcvbn", "get", password=password)
    entropy = result["entropy"]
    if entropy > 75.0:
        print(f'"{password}" — entropy {entropy:.1f} — STRONG')
        return True
    else:
        print(f'"{password}" — entropy {entropy:.1f} — TOO WEAK')
        return False
```

---

## Changing a User Password

```python
import jsonrpcdevice

host = "192.168.0.254"
username = "admin"
old_password = "admin"
new_password = "NewSecurePassword!"

dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, old_password)

# Check strength before changing
result = dev.call("zxcvbn", "get", password=new_password)
if result["entropy"] < 75.0:
    print("Password too weak, choose a stronger one")
    dev.logout()
    exit(1)

# Change password
cfg_session_id = dev.sess_start()
dev.config_set(cfg_session_id, {
    "webpwd_user": username,
    "webpwd_user_old": old_password,
    "webpwd_user_new": new_password,
    "webpwd_user_checked": new_password
})
dev.sess_commit(cfg_session_id)
dev.logout()

# Verify: log in with the new password
dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, new_password)
dev.logout()
print("Password changed successfully")
```

!!! important
    All four password fields must be set in a single `config_set` call within one session:

    - `webpwd_user` — the username
    - `webpwd_user_old` — the current password
    - `webpwd_user_new` — the new password
    - `webpwd_user_checked` — confirmation (must match `webpwd_user_new`)

---

## Migrating to Argon2 Password Mode

!!! note
    This is only needed on IRF devices that were updated from firmware versions older than 2.0.0. Devices shipped with firmware >= 2.0.0 already use Argon2.

To upgrade password hashing to Argon2, the password mode, policy, and admin password must be changed **atomically** in one session:

```python
dev = jsonrpcdevice.AdstecJSONRPCDevice(host, "admin", old_password)

cfg_session_id = dev.sess_start()
dev.config_set(cfg_session_id, {
    "password_mode": "argon2",
    "password_policy": "enabled",
    "webpwd_user": "admin",
    "webpwd_user_new": new_password,
    "webpwd_user_checked": new_password
})
dev.sess_commit(cfg_session_id)
```

!!! warning
    Changing `password_mode` is irreversible. Ensure you have the new password noted before committing.
