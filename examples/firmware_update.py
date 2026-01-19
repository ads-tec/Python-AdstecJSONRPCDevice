import time
import requests
import jsonrpcdevice

def check_host(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        return True, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)


def wait_for_reboot(host, username, password, check_interval=3):
    previous_state = None
    url = "https://" + host + "/"
    while True:
        is_online, info = check_host(url)
        if previous_state is None:
            status = "ONLINE" if is_online else "OFFLINE"
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Initial state: {status}")
            if is_online:
                print(f"  Status code: {info}")
            else:
                print(f"  Error: {info}")
        elif previous_state != is_online:
            if is_online:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✓ Host came ONLINE")
                while True:
                    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, password)
                    boot_finished = dev.status("boot_finished")
                    if boot_finished == "yes":
                        return dev
                    else:
                        print("Boot in progress, waiting for boot_finished")
                        time.sleep(1)
            else:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✗ Host went OFFLINE")

        previous_state = is_online
        time.sleep(check_interval)


if __name__ == "__main__":
    host = "192.168.0.254"
    username = "admin"
    password = "admin"

    # login to device
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, password)

    firmware_filename = "Ads-tec-IRF3xxx-2.2.6-SVN-R63743.B-181926.bin"

    initial_firmware_version = dev.status("imageversion")
    print(f"initial_firmware_version: {initial_firmware_version}")
    initial_uptime = dev.status("uptimesec")

    upload_result = dev.upload_file("firmware", firmware_filename)
    print(f"upload_result: {upload_result}")

    dev = wait_for_reboot(host, username, password, check_interval=3)

    current_firmware_version = dev.status("imageversion")

    print(f"Device rebooted with firmware: {current_firmware_version}")