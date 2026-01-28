import jsonrpcdevice
from datetime import datetime

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    system_name = dev.status("system_name")
    print(f"system_name: {system_name}")

    imageversion = dev.status("imageversion")
    print(f"imageversion: {imageversion}")

    cpustat = dev.status("cpustat")
    print(f"cpustat: {cpustat}")

    # download diag which contains system information like cpu, memory, network, temperature
    dev.config_set_commit({"generate_diag_now": "1"})
    now = datetime.now()
    format_datetime = now.strftime("%Y_%m_%d_%H_%M")
    output_filename = "diag_" + system_name + "_" + format_datetime + ".tar.gz"
    dev.download_file("diag.tar.gz", output_filename)
    print(f"Diag download complete: {output_filename}")

    redbootserial = dev.status("redbootserial")
    print(f"serial: {redbootserial}")

    redbootproduct = dev.status("redbootproduct")
    print(f"hardware revision: {redbootproduct}")

    dev.logout()