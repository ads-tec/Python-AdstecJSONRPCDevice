# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # Get the LAN interface name from config
    lan_ifname = dev.config_get(["lan_ifname"])["result"][0]["lan_ifname"]
    print(f"LAN interface: {lan_ifname}")

    # Query IP and MAC address
    lan_ip = dev.status("if_ip", lan_ifname)
    lan_mac = dev.status("if_mac", lan_ifname)
    print(f"LAN IP:  {lan_ip}")
    print(f"LAN MAC: {lan_mac}")

    dev.logout()
