# JSON-RPC Methods (Firewalls)

!!! info "Firewall models only"
    The methods on this page are available on **IRF1000, IRF2000, and IRF3000** firewalls only. For methods available on all devices, see [JSON-RPC Methods](../jsonrpc-methods.md).

---

## `gpio` — GPIO Control

| Method | Parameters | Description |
|---|---|---|
| `list` | — | List all available GPIO signals |
| `get` | `signal` | Get the current value of a signal |
| `get_bool` | `signal` | Get the boolean state of a signal |
| `get_pulses` | `signal` | Get pulse count (counts rising + falling edges; one button press = 2) |
| `on` | `signal` | Turn a signal on |
| `off` | `signal` | Turn a signal off |

### IRF2000 Signals

**Output signals** (on/off):

| Signal | Alias | Description |
|---|---|---|
| `alarm` | `x1out` | Alarm output |
| `vpnup` | `x2out` | VPN status output |
| `vpnled` | | VPN LED |
| `cutled` | | CUT LED |
| `statusled` | | Status LED |

**Input signals** (get/get_bool):

| Signal | Alias | Description |
|---|---|---|
| `cut` | `x1in` | CUT input |
| `vpnkey` | `x2in` | VPN key input |
| `button` | | Front reset button |

### IRF3000 Signals

| Signal | Description |
|---|---|
| `DI1`, `DI2`, ... | Digital inputs |
| `LED2_RED`, ... | LEDs |

Use `gpio.list` to discover all signals on your device.

**Python:**

```python
signals = dev.call("gpio", "list")
state = dev.call("gpio", "get_bool", signal="DI2")
dev.call("gpio", "on", signal="LED2_RED")
dev.call("gpio", "off", signal="LED2_RED")
pulses = dev.call("gpio", "get_pulses", signal="button")
```

---

## `network.ipsec.control` — IPsec VPN

Control IPsec VPN policies configured as "Active (Switched)" in the web interface.

| Method | Parameters | Description |
|---|---|---|
| `up` | policy identifier | Activate an IPsec policy |
| `down` | policy identifier | Deactivate an IPsec policy |

!!! note
    The IPsec policy must be configured as "Active (Switched)" before it can be controlled via API.
