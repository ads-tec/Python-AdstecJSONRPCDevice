# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

if __name__ == "__main__":
    host = "192.168.0.254"
    username = "admin"
    password = "admin"
    allowed_capture_hosts = "192.168.0.190"
    # login to device
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, password)

    # get a list of all available interfaces
    ifaces_array = dev.status("symbolic_ifnames_with_umts_with_ipsec").split(' ')

    # remove the "lan" interface from available ifaces_array to create a block list
    ifaces_array.remove("lan")

    native_block_access_list =  dev.convert_to_ifname(ifaces_array)

    dev.config_set_commit({"rpcap_status": "enabled",
              "rpcap_hostlist": allowed_capture_hosts,
              "rpcap_access": native_block_access_list
              })

    dev.logout()
