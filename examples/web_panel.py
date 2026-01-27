import jsonrpcdevice

if __name__ == "__main__":
    username = "admin"
    password = "admin"
    host = "192.168.0.254"
    host_new = "192.168.0.253"

    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, password, 5, False)

    values = {"lan_ipaddr": host_new,
               "lan_netmask": "255.255.255.0",
               "lan_gateway": "192.168.0.1"
              }
    print("Set new IP address:" + host_new + " and wait for device to come online")
    dev.config_set_commit_with_ip_change(values, host_new)

    dev.config_set_commit({"browser_url": "http://192.168.0.190",
                           "browser_activate_url_now": "1",
                           "browser_switch_gesture": "enabled",
                           "browser_context_menu": "enabled",
                           "browser_persistent_cache": "enabled",
                           "display_orientation": "0",
                           "display_brightness": "80",
                           "browser_keyboard": "enabled",
                           "terminal_gui_locale": "en",
                           "browser_keyboard_scale": "1.0",
                           "keyboard_layout": "en",
              })
    print("Web panel settings applied")

    # to show config on web panel again. set the url to localhost
    # dev.config_set_commit({"browser_url": "http://localhost",
    #                       "browser_activate_url_now": "1",})

    dev.logout()
