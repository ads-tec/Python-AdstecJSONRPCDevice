# Configuration Variables (Web Terminals)

!!! info "Web terminals only"
    The configuration variables on this page apply to **ads-tec Web terminals** only. For variables available on all devices, see [Configuration Variables](../config-variables.md).

---

## Web Panel

| Variable | Values | Description |
|---|---|---|
| `browser_url` | URL string | URL displayed on the web terminal |
| `browser_activate_url_now` | `"1"` | Trigger immediate navigation to `browser_url` |
| `browser_switch_gesture` | `"enabled"` / `"disabled"` | Allow gesture to switch between browser and config UI |
| `browser_context_menu` | `"enabled"` / `"disabled"` | Enable browser right-click context menu |
| `browser_persistent_cache` | `"enabled"` / `"disabled"` | Persist browser cache across reboots |
| `browser_keyboard` | `"enabled"` / `"disabled"` | Show on-screen keyboard |
| `browser_keyboard_scale` | string | Keyboard scale factor (e.g., `"1.0"`) |
| `keyboard_layout` | string | Keyboard layout (e.g., `"en"`, `"de"`) |
| `display_orientation` | `"0"` / `"90"` / `"180"` / `"270"` | Display rotation in degrees |
| `display_brightness` | `"0"` - `"100"` | Display brightness percentage |
| `terminal_gui_locale` | string | GUI language (e.g., `"en"`, `"de"`) |
