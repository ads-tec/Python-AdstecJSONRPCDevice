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

## Variable Reference

For a complete list of all configuration variables with defaults, allowed values, and validation rules, see the per-product Configuration Database reference:

| Product | Reference |
|---|---|
| AWT1000 (Web Terminal) | [AWT1000 Configuration Database](configdb/AWT1000.md) |
| IRF1401 | [IRF1401 Configuration Database](configdb/IRF1401.md) |
| IRF1421 | [IRF1421 Configuration Database](configdb/IRF1421.md) |
| IRF3401 | [IRF3401 Configuration Database](configdb/IRF3401.md) |
| IRF3421 | [IRF3421 Configuration Database](configdb/IRF3421.md) |
| IRF3801 | [IRF3801 Configuration Database](configdb/IRF3801.md) |
| IRF3821 | [IRF3821 Configuration Database](configdb/IRF3821.md) |

See also the [Configuration Database Overview](configdb/index.md) for a comparison of features across products.
