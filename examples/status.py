import jsonrpcdevice

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    # simple status
    imageversion = dev.status("imageversion")
    print(f"imageversion: {imageversion}")

    # status with parameters
    ping = dev.status("ping4", "127.0.0.1", "3")
    print(f"ping: {ping}")

    dev.logout()