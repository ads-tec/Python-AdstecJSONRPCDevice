import jsonrpcdevice
from datetime import datetime

if __name__ == "__main__":
    # login to device
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # prepare settings
    print(f"start prepare settings")
    dev.config_set_commit({"save_settings_now": "1"})
    print(f"prepare settings done")

    # get info for local filename
    serial = dev.status("redbootserial")
    now = datetime.now()
    format_datetime = now.strftime("%Y_%m_%d_%H_%M")
    product = dev.status("product_alias")
    output_filename = f"settings_{product}_{serial}_{format_datetime}.cf2"

    # download file
    dev.download_file("settings.cf2", output_filename)
    print(f"Settings download complete: {output_filename}")

    dev.logout()