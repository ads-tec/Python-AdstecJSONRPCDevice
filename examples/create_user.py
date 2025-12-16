import jsonrpcdevice

if __name__ == "__main__":
    new_username = "testuser"
    new_password = "ads-tecNuertingen"

    # login to device
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # create config session
    cfg_session_id = dev.sess_start()

    # add user
    dev.table_insert("users", cfg_session_id, [new_username, "", "", "1", "", "1970-01-01", "1970-01-01"])

    # set password
    dev.config_set(cfg_session_id, {"webpwd_user": new_username, "webpwd_user_new": new_password, "webpwd_user_checked": new_password})

    # submit config session
    dev.sess_commit(cfg_session_id)

    dev.logout()