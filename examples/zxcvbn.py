import jsonrpcdevice

def check_password_strength(dev, password):
    result = dev.call("zxcvbn", "get", password=password)
    entropy = result["entropy"]
    if entropy> 75.0:
        print(f"password: \"{password}\" has entropy of: {entropy} and is strong")
    else:
        print(f"password: \"{password}\" has entropy of: {entropy} and is not strong enough")

if __name__ == "__main__":
    dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

    check_password_strength(dev, "weak123")
    check_password_strength(dev, "1H_$X%rIjg(EIu+ecw9VCZ+T")

    dev.logout()