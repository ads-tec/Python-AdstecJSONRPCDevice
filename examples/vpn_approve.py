import time
import jsonrpcdevice

if __name__ == "__main__":
    host = "192.168.0.254"
    username = "admin"
    password = "admin"

    # login to device
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, password)

    # create config session
    cfg_session_id = dev.sess_start()

    # set approval mode to API, only needed once
    dev.config_set(cfg_session_id, {"vpn_approval_mode": "api"})

    # submit config session
    dev.sess_commit(cfg_session_id)

    #wait for approval
    blxstat_vpnstate = ""
    while blxstat_vpnstate != "WAITINGFORAPPROVAL":
        blxstat_vpnstate = dev.status('blxstat_vpnstate')
        print(f"blxstat_vpnstate: {blxstat_vpnstate}")
        time.sleep(3)

    # in WAITINGFORAPPROVAL state now
    cfg_session_id = dev.sess_start()
    dev.config_set(cfg_session_id, {"vpn_approve_now": "1"})
    dev.sess_commit(cfg_session_id)

    # connection approved, wait until vpn is up
    while blxstat_vpnstate != "CONNECTED":
        blxstat_vpnstate = dev.status('blxstat_vpnstate')
        print(f"blxstat_vpnstate: {blxstat_vpnstate}")
        time.sleep(1)

    print(f"vpn online")

    dev.logout()