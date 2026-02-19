# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

if __name__ == "__main__":
    host = "192.168.0.254"
    username = "admin"
    old_password = "admin"
    new_password = "ads-tecNuertingen"

    # login to device
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, old_password)

    # create config session
    cfg_session_id = dev.sess_start()

    # set password
    dev.config_set(cfg_session_id, {"webpwd_user": username, "webpwd_user_old": old_password, "webpwd_user_new": new_password, "webpwd_user_checked": new_password })

    # submit config session
    dev.sess_commit(cfg_session_id)

    dev.logout()

    # try to login with new password
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, new_password)

    dev.logout()
