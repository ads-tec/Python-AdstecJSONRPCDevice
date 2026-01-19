import time
import requests
import re
from typing import Tuple, Optional
import jsonrpcdevice


def extract_firmware_info(filename: str) -> Optional[Tuple[str, str, str]]:
    name = filename.replace('.bin', '')
    pattern = r'^Ads-tec-([^-]+)-(\d+\.\d+\.\d+)-(SVN-R\d+\.B-\d+)$'
    match = re.match(pattern, name)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None


def extract_device_status(status: str) -> Optional[Tuple[str, str, str]]:
    status_clean = status.split(' -- ')[0]
    pattern = r'^Ads-tec/([^/]+)/(\d+\.\d+\.\d+)/(SVN-R\d+\.B-\d+)$'
    match = re.match(pattern, status_clean)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None


def compare_firmware_versions(filename: str, device_status: str) -> bool:
    file_info = extract_firmware_info(filename)
    device_info = extract_device_status(device_status)
    if file_info is None or device_info is None:
        return False
    return file_info == device_info


def check_host(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        return True, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)


def wait_for_reboot(host, check_interval=3):
    """Monitor host and report state changes"""
    previous_state = None
    url = "https://" + host + "/"
    while True:
        is_online, info = check_host(url)

        # Detect state change
        if previous_state is None:
            status = "ONLINE" if is_online else "OFFLINE"
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Initial state: {status}")
            if is_online:
                print(f"  Status code: {info}")
            else:
                print(f"  Error: {info}")
        elif previous_state != is_online:
            # State changed
            if is_online:
                print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✓ Host came ONLINE")
                return True
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

    wait_for_reboot(host, check_interval=3)

    # after reboot a new session is needed
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, username, password)
    current_firmware_version = dev.status("imageversion")

    if compare_firmware_versions(firmware_filename, current_firmware_version):
        print(f"Firmware update from {initial_firmware_version} to {current_firmware_version} successful")
    else:
        print(f"Firmware update failed")