# Configuration Variables (Firewalls)

!!! info "Firewall models only"
    The configuration variables described here apply to **IRF1000, IRF2000, and IRF3000** firewalls only. For the API usage patterns (reading/writing variables), see [Configuration Variables](../config-variables.md).

## Variable Reference

For the complete list of all firewall configuration variables with defaults, allowed values, and validation rules, see the per-product Configuration Database:

- [IRF1401](../configdb/IRF1401.md) / [IRF1421](../configdb/IRF1421.md)
- [IRF3401](../configdb/IRF3401.md) / [IRF3421](../configdb/IRF3421.md)
- [IRF3801](../configdb/IRF3801.md) / [IRF3821](../configdb/IRF3821.md)

Key firewall-specific sections in those references:

- **VPN** — OpenVPN connections, IPsec tunnels, Big-LinX configuration
- **Packet Filter & NAT** — filter rules, 1:1 NAT, port forwarding, network/hardware groups
- **I/O & Signals** — CUT & ALARM signals, GPIO automatic control
- **Mobile & Cellular** — 3G/4G UMTS/LTE, SMS Service (IRF1421, IRF3421, IRF3821)
