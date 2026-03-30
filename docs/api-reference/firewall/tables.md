# Tables (Firewall)

!!! note "Firewall models only"
    The tables described here are available on IRF1000, IRF2000, and IRF3000 firewalls. For the table API operations (read, insert, update, delete), see [Tables](../tables.md).

## Table Reference

For the complete list of all firewall tables with column definitions, validation rules, and factory defaults, see the per-product Configuration Database:

- [IRF1401](../configdb/IRF1401.md) / [IRF1421](../configdb/IRF1421.md)
- [IRF3401](../configdb/IRF3401.md) / [IRF3421](../configdb/IRF3421.md)
- [IRF3801](../configdb/IRF3801.md) / [IRF3821](../configdb/IRF3821.md)

Key firewall-specific tables documented there:

- **`services`** — Packet filter rulesets (Packet Filter & NAT section)
- **`serv_Protocols`** — Packet filter rules within rulesets
- **`selected_services`** — Active packet filter rulesets with time-based scheduling
- **`ipgroups`** / **`macgroups`** — Network and hardware address groups
- **`forwarding`** — Port forwarding (DNAT) rules
- **`vpnconfig`** / **`vpnclientconfig`** / **`vpnclientroutes`** — OpenVPN configuration
- **`din_mapping`** / **`dout_mapping`** — Digital I/O signal mapping

See the [Packet Filter guide](../../guides/packet-filter/index.md) for detailed usage examples.
