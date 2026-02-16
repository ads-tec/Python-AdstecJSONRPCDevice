# Web Panel (Terminals)

!!! note "Web terminals only"
    These settings apply to ads-tec Web terminals, not firewall models.

## Configuring the Web Panel

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

dev.config_set_commit({
    "browser_url": "http://192.168.0.190",
    "browser_activate_url_now": "1",
    "browser_switch_gesture": "enabled",
    "browser_context_menu": "enabled",
    "browser_persistent_cache": "enabled",
    "display_orientation": "0",
    "display_brightness": "80",
    "browser_keyboard": "enabled",
    "browser_keyboard_scale": "1.0",
    "keyboard_layout": "en",
    "terminal_gui_locale": "en",
})
print("Web panel settings applied")

dev.logout()
```

## Showing the Config UI Again

To switch the terminal back to the built-in configuration interface:

```python
dev.config_set_commit({
    "browser_url": "http://localhost",
    "browser_activate_url_now": "1",
})
```

## Available Settings

| Variable | Values | Description |
|---|---|---|
| `browser_url` | URL string | URL to display on the terminal |
| `browser_activate_url_now` | `"1"` | Navigate to the URL immediately |
| `browser_switch_gesture` | `"enabled"` / `"disabled"` | Allow gesture to switch between browser and config UI |
| `browser_context_menu` | `"enabled"` / `"disabled"` | Enable right-click context menu |
| `browser_persistent_cache` | `"enabled"` / `"disabled"` | Persist browser cache across reboots |
| `browser_keyboard` | `"enabled"` / `"disabled"` | Show on-screen keyboard |
| `browser_keyboard_scale` | `"0.5"` to `"2.0"` | Keyboard size scale factor |
| `keyboard_layout` | `"en"`, `"de"`, etc. | Keyboard layout |
| `display_orientation` | `"0"`, `"90"`, `"180"`, `"270"` | Display rotation in degrees |
| `display_brightness` | `"0"` to `"100"` | Display brightness percentage |
| `terminal_gui_locale` | `"en"`, `"de"`, etc. | GUI language |

## Changing IP with Web Panel Setup

When setting up a new terminal, you often need to change the IP address first:

```python
host_new = "192.168.0.253"

# Use short timeout for IP change
dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin", timeout=5)

# Change IP first
dev.config_set_commit_with_ip_change(
    {"lan_ipaddr": host_new, "lan_netmask": "255.255.255.0", "lan_gateway": "192.168.0.1"},
    host_new
)

# Then configure the web panel
dev.config_set_commit({"browser_url": "http://my-app.local", "browser_activate_url_now": "1"})

dev.logout()
```
