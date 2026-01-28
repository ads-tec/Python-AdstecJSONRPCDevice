import jsonrpcdevice
import time

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")
    external_timesync = True
    available_timezones = dev.status("timezone_list")
    timezone_list = available_timezones.split(" ")
    print(f"available_timezones: {available_timezones}")
    print("set timezone to:" + timezone_list[0])
    dev.config_set_commit({"timezone": timezone_list[0]})

    if external_timesync:

        dev.config_set_commit({"ntp_service": "enabled",
                               "ntp_server": "ptbtime1.ptb.de",
                               "ntp_server2": "ptbtime2.ptb.de"})
        ntp_synced = False
        for i in range(10):
            time.sleep(2)
            ntpstat_sources = dev.status("ntpstat_sources")
            ntpstat_sources_list = ntpstat_sources.split("\n")
            for ntp_server in ntpstat_sources_list:
                ntp_server_status_list = ntp_server.split(",")
                if ntp_server_status_list[1] == "*":
                    print(f"ntp_server {ntp_server_status_list[2]} is used for time sync")
                    ntp_synced = True
                    break
            if ntp_synced:
                break
        if not ntp_synced:
            print("ntp sync failed")

    else:
        dev.config_set_commit({"ntp_service": "disabled",
                               "day": "01",
                               "month": "01",
                               "year": "2026",
                               "hour": "00",
                               "minute": "00",
                               "second": "00"})
    dev.logout()