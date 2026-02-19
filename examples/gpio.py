# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice
import time

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # get a list of all available GPIO signals
    list = dev.call("gpio", "list")
    for f in list['signals']:
        print(f)

    # get state of DI2 digital input 2
    di2_state = dev.call("gpio", "get_bool", signal="DI2")
    print(f"di2_state: {di2_state}")

    # turn on the red light on LED2
    dev.call("gpio", "on", signal="LED2_RED")

    # get state of LED2
    led2_state = dev.call("gpio", "get", signal="LED2_RED")
    print(f"led2_state: {led2_state}")

    # wait a sec to make LED visible
    time.sleep(1)
    dev.call("gpio", "off", signal="LED2_RED")

    # LED2 should be off now
    led2_state = dev.call("gpio", "get", signal="LED2_RED")
    print(f"led2_state: {led2_state}")

    dev.logout()