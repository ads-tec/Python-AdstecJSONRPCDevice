# Certificates

## Uploading a CA Certificate

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Upload
dev.upload_file("cert", "ca-cert.pem")

# Verify it's installed
ca_certs = dev.status("cacerts")
print(f"Installed CA certs: {ca_certs}")

# Print certificate details
details = dev.status("print_cacert", "ca-cert.pem")
print(details)

dev.logout()
```

## Uploading a Server/Client Certificate

```python
dev.upload_file("cert", "server-cert.pem")

# Verify
client_certs = dev.status("clcerts")
print(f"Installed certs: {client_certs}")

# Print details
details = dev.status("print_cert", "server-cert.pem")
print(details)
```

## Upload with Overwrite

If a certificate with the same filename already exists, delete it first:

```python
def upload_cert(dev, cert_type, filename, overwrite=False):
    certs_before = dev.status(cert_type)
    if filename in certs_before:
        if overwrite:
            # Delete existing cert
            cfg_session_id = dev.sess_start()
            dev.config_set(cfg_session_id, {
                "to_be_deleted": "ca/" + filename,
                "cert_delete": "1"
            })
            dev.sess_commit(cfg_session_id)
        else:
            print(f"Certificate already exists: {filename}")
            return

    dev.upload_file("cert", filename)
    certs_after = dev.status(cert_type)
    if filename in certs_after:
        print(f"Certificate uploaded: {filename}")

# Usage
upload_cert(dev, "cacerts", "ca-cert.pem", overwrite=True)
upload_cert(dev, "clcerts", "server-cert.pem")
```

## Deleting a Certificate

```python
cfg_session_id = dev.sess_start()
dev.config_set(cfg_session_id, {
    "to_be_deleted": "ca/ca-cert.pem",
    "cert_delete": "1"
})
dev.sess_commit(cfg_session_id)
```

## Certificate Status Properties

| Property | Description |
|---|---|
| `cacerts` | List of installed CA certificates |
| `clcerts` | List of installed client/server certificates |
| `print_cacert` | Print CA certificate details (param: filename) |
| `print_cert` | Print client/server certificate details (param: filename) |
