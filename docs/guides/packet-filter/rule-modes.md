# Rule Modes

The columns referenced below (`state_type_id`, `revert`, `states`, `statevalue`) are part of the [`serv_Protocols`](../../api-reference/firewall/tables.md#serv_protocols-packet-filter-rules) table. See the [Table Reference](tables.md#serv_protocols) for full column schemas.

## L3 Rule Modes: Easy, Stateful, and Stateless

Layer 3 (iptables) rulesets support three distinct modes for handling connection state and return traffic. Each mode represents a different trade-off between simplicity, flexibility, and performance.

!!! warning "Do not mix modes within a ruleset"
    All rules within a single ruleset should use the same mode. Mixing modes (e.g., a stateful rule and a stateless rule in the same ruleset) leads to unpredictable behavior because the return-traffic handling assumptions conflict. Create separate rulesets if you need different modes.

### Easy Mode (Default)

**Fields**: `revert="1"`, `state_type_id=""`, `states=""`

This is the default mode in the device web UI. The user defines a rule for one direction only, and the system automatically generates a hidden reverse rule using conntrack to allow the return traffic. The user never has to think about connection states or return packets.

**How it works**: When a rule has `revert="1"`, the device automatically creates a second iptables rule in a reverse chain that uses conntrack (`-m conntrack --ctstate RELATED,ESTABLISHED`) to match return traffic for connections allowed by the forward rule.

**Pros**:

- Simplest to configure — define one direction, return traffic is handled automatically
- Lowest risk of misconfiguration — no state or flag parameters to get wrong
- Default in the web UI, suitable for most use cases

**Cons**:

- Uses conntrack, which has a finite connection table (can overflow under very high connection rates)
- Less control — you cannot fine-tune which return traffic is allowed
- The hidden reverse rule is not visible in the table, which can be confusing when debugging via API

**Example rule values**:
```
revert="1", state_type_id="", states=""
```

### Stateful Mode

**Fields**: `revert="0"`, `state_type_id="1"` or `"3"`, `states="NEW,RELATED,ESTABLISHED"`

Classic iptables stateful filtering using the conntrack module. The user explicitly specifies which connection states to match (e.g., `NEW`, `ESTABLISHED`, `RELATED`, `INVALID`). The user is responsible for creating matching rules for both directions or using appropriate state combinations.

**How it works**: The rule translates directly to `-m conntrack --ctstate <states>` in iptables. `state_type_id="1"` and `"3"` both use conntrack; `"3"` additionally applies to auto-generated reverse chains for directional rulesets.

**Pros**:

- Full control over which connection states are matched
- Well-understood iptables paradigm — extensive documentation and tooling available
- Can create precise rules like "allow only established return traffic" or "block invalid packets"

**Cons**:

- More complex to configure correctly — the user must understand conntrack states
- Requires explicit rules for return traffic (or careful use of `ESTABLISHED,RELATED`)
- Still uses conntrack, so the same connection table limits apply as easy mode

**Example rule values**:
```
revert="0", state_type_id="1", states="NEW,RELATED,ESTABLISHED"
```

### Stateless Mode

**Fields**: `revert="0"`, `state_type_id="2"`, `states=<tcp-flags>`

Low-level stateless filtering using TCP flags only, bypassing the conntrack module entirely. Rules match individual packets based on their TCP flag combination (SYN, ACK, FIN, RST, etc.) without any connection tracking.

**How it works**: The rule translates to `--tcp-flags <flags-to-check> <expected-flags>` in iptables. The `states` field contains the flag specification (e.g., `SYN,ACK,FIN,RST SYN` to match SYN-only packets). On L2 (ebtables), the `statevalue` field encodes flags as a 12-bit integer instead.

**Pros**:

- Highest performance — no conntrack overhead, no connection table, no per-connection memory
- Ideal for high-throughput scenarios or DDoS mitigation where conntrack would be a bottleneck
- Deterministic — each packet is evaluated independently, no state table to overflow

**Cons**:

- Most complex to configure — requires deep understanding of TCP flag combinations
- The user must create explicit rules for every traffic direction and packet type (SYN, SYN+ACK, ACK, FIN, etc.)
- No automatic handling of related traffic (e.g., ICMP error messages for TCP connections)
- Easy to misconfigure — a missing flag combination silently drops legitimate traffic

**Example rule values**:
```
revert="0", state_type_id="2", states="SYN,ACK,FIN,RST SYN"
```

### Mode Comparison

| | Easy | Stateful | Stateless |
|---|---|---|---|
| **Complexity** | Low | Medium | High |
| **Performance** | Good | Good | Best |
| **Conntrack** | Yes (hidden) | Yes (explicit) | No |
| **Return traffic** | Automatic | Manual (via states) | Manual (via TCP flags) |
| **`revert`** | `"1"` | `"0"` | `"0"` |
| **`state_type_id`** | `""` | `"1"` or `"3"` | `"2"` |
| **`states`** | `""` | `NEW,RELATED,...` | TCP flag spec |
| **Web UI default** | Yes | Selectable | Selectable |
| **Recommended for** | General use | Fine-grained control | High-throughput, DDoS |

---

## L2 Filtering (ebtables)

Layer 2 rulesets (`layer_id="1"`) use ebtables instead of iptables and operate on Ethernet frames. L2 filtering has fundamental differences from L3 that affect how rules are constructed and how state is handled.

### No Native Conntrack

Ebtables has no conntrack module. The three L3 modes (easy, stateful, stateless) do not apply to L2 in the same way. On L2:

- **Easy mode** (`revert="1"`) still works for directional rulesets — the reverse rule is placed in a separate chain. However, this is a simple directional reversal, not conntrack-based return traffic matching.
- **Stateful mode** (`state_type_id="1"`) is **not available** on L2 — ebtables has no conntrack.
- **TCP flag matching** is supported on L2 via the `states` and `statevalue` fields. Set `states` to the human-readable flag specification (e.g., `"SYN,ACK,FIN,RST SYN"`) and `statevalue` to the corresponding numeric encoding. The system handles the translation internally.

### Protocol Handling

L2 rules use the `protocol` field differently from L3:

| `protocol` | `prot_transport` | `prot_hex` | Meaning |
|---|---|---|---|
| `"ARP"` | — | opcode (e.g. `"10"` = any) | ARP frames; `prot_hex` is the ARP opcode |
| `"IPV4"` | `"6"` | — | IPv4 + TCP (`--ip-protocol 6`) |
| `"IPV4"` | `"17"` | — | IPv4 + UDP (`--ip-protocol 17`) |
| `"IPV4"` | `"1"` | — | IPv4 + ICMP (`--ip-protocol 1`) |
| `"IPV4"` | `"*"` | — | IPv4 any transport |
| `"802_1Q"` | — | — | VLAN-tagged frames (uses `vlan_data` table for VLAN ID/priority) |
| (other) | — | hex value | Raw Ethernet protocol by hex; `"0000"` = LENGTH (legacy Ethernet II) |

### MAC and IP Groups on L2

Group handling differs from L3:

- **MAC groups** (`@groupname` in `src_mac_add`/`des_mac_add`): resolved from the `macgroups` table and applied using ebtables `--among-src`/`--among-dst` (comma-separated MAC list in a single rule).
- **IP groups** (`@groupname` in `src_ip_add`/`des_ip_add`): since ebtables has no `ipset` support, each IP/network entry from the `ipgroups` table is expanded into a **separate ebtables rule**. Large IP groups generate many rules, which can impact performance.

!!! tip "Prefer MAC groups over IP groups on L2"
    MAC groups are efficient on L2 because ebtables handles them in a single rule with `--among`. IP groups are expanded into individual rules, so large groups significantly increase the rule count and evaluation time.
