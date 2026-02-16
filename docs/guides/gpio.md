# GPIO

!!! note "Firewall models only"
    GPIO functionality is available on IRF1000, IRF2000, and IRF3000 firewalls.

## Listing Available Signals

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

signals = dev.call("gpio", "list")
for signal in signals["signals"]:
    print(signal)

dev.logout()
```

## Reading Digital Inputs

```python
# Get boolean state of digital input 2
di2_state = dev.call("gpio", "get_bool", signal="DI2")
print(f"DI2: {di2_state}")
```

## Controlling LEDs

```python
import time

# Turn on the red LED on LED2
dev.call("gpio", "on", signal="LED2_RED")

# Check the state
state = dev.call("gpio", "get", signal="LED2_RED")
print(f"LED2_RED: {state}")

# Wait, then turn off
time.sleep(1)
dev.call("gpio", "off", signal="LED2_RED")
```

## GPIO Methods

| Method | Parameters | Description |
|---|---|---|
| `gpio.list` | — | List all available GPIO signals |
| `gpio.get` | `signal` | Get current value of a signal |
| `gpio.get_bool` | `signal` | Get boolean state of a signal |
| `gpio.on` | `signal` | Turn a signal on |
| `gpio.off` | `signal` | Turn a signal off |

## Signal Naming

| Type | Pattern | Example |
|---|---|---|
| Digital Inputs | `DI<n>` | `DI1`, `DI2` |
| LEDs | `LED<n>_<color>` | `LED2_RED` |
