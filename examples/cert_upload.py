# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

def delete_cert(dev, filename):
    cfg_session_id = dev.sess_start()
    dev.config_set(cfg_session_id, {"to_be_deleted": "ca/"+filename, "cert_delete" : "1" })
    dev.sess_commit(cfg_session_id)

def upload_cert(dev, cert_type, filename, overwrite_existing_cert=False):
    certs_before = dev.status(cert_type)
    if filename in certs_before:
        print(f"cert already uploaded: {certs_before}")
        if overwrite_existing_cert:
            delete_cert(dev, filename)
        else:
            return
    upload_result = dev.upload_file("cert", filename)
    print(f"upload_result: {upload_result}")
    certs_after = dev.status(cert_type)
    if filename in certs_after:
        print(f"cert succefully uploaded")

if __name__ == "__main__":
    # login to device
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # upload a ca cert
    ca_cert_filename = "ca-cert.pem"
    upload_cert(dev, "cacerts", ca_cert_filename)
    ca_cert = dev.status("print_cacert", ca_cert_filename)
    print(f"cacert: {ca_cert}")

    # upload a server or client cert
    server_cert_filename = "server-cert.pem"
    upload_cert(dev, "clcerts", server_cert_filename)
    server_cert = dev.status("print_cert", server_cert_filename)
    print(f"server_cert: {server_cert}")

    dev.logout()