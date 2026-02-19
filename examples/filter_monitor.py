# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

"""Monitor packet filter byte counters in real time (firewalls only).

Lists all available filter metrics from the datacollection API and then
polls a selected ruleset, printing byte-count deltas every interval.
By default monitors the "Allow_L3" ruleset which is present on every
IRF device.

Usage:
    python filter_monitor.py <host> <user> <password> [ruleset]

Examples:
    python filter_monitor.py 192.168.0.254 admin admin            # Allow_L3
    python filter_monitor.py 192.168.0.254 admin admin MyRuleset
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

POLL_INTERVAL = 10  # seconds (data arrives every ~10s)


def get_filter_metrics(dev):
    """Return sorted list of all filter.* metric names."""
    raw = dev.call("datacollection", "get_metrics")
    return sorted(m for m in raw.get("result", []) if m.startswith("filter."))


def get_ruleset_metrics(all_metrics, ruleset):
    """Return metrics belonging to a specific ruleset chain."""
    chain = f"_{ruleset}"
    matches = []
    for m in all_metrics:
        parts = m.split(".")
        # filter.rule.<chain>.<target>.<index>.bcnt
        # Match both the ruleset chain and the jump-to-ruleset in FORWARD
        if chain in parts:
            matches.append(m)
    return sorted(matches)


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    host, user, password = sys.argv[1], sys.argv[2], sys.argv[3]
    ruleset = sys.argv[4] if len(sys.argv) > 4 else "Allow_L3"

    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, user, password)

    # discover all filter metrics
    all_filter = get_filter_metrics(dev)
    if not all_filter:
        print("No filter metrics found. Is this a firewall device?")
        dev.logout()
        sys.exit(1)

    print(f"Available filter metrics ({len(all_filter)}):\n")
    for m in all_filter:
        print(f"  {m}")

    # find metrics for the selected ruleset
    ruleset_metrics = get_ruleset_metrics(all_filter, ruleset)
    if not ruleset_metrics:
        print(f"\nNo metrics found for ruleset '{ruleset}'.")
        print("Available rulesets:",
              sorted(set(m.split(".")[2] for m in all_filter
                         if m.startswith("filter.rule."))))
        dev.logout()
        sys.exit(1)

    print(f"\n--- Monitoring ruleset '{ruleset}' ({len(ruleset_metrics)} metrics) ---")
    print(f"Polling every {POLL_INTERVAL}s. Press Ctrl+C to stop.\n")

    prev_values = {}

    try:
        while True:
            now = int(time.time())
            try:
                raw = dev.call("datacollection", "get_values_as_table",
                               metrics=ruleset_metrics,
                               **{"from": now - 30, "to": now,
                                  "resolution": 1})
            except Exception as e:
                print(f"Query error: {e}")
                time.sleep(POLL_INTERVAL)
                continue

            data = raw.get("result", {})
            ts_str = time.strftime("%H:%M:%S")

            for metric in ruleset_metrics:
                points = data.get(metric, [])
                # use the latest non-null value
                current = None
                for p in reversed(points):
                    if p["val"] is not None:
                        current = p["val"]
                        break

                if current is None:
                    continue

                prev = prev_values.get(metric)
                delta = current - prev if prev is not None else 0.0
                prev_values[metric] = current

                if delta != 0.0 or prev is None:
                    label = metric.replace("filter.rule.", "").replace(".bcnt", "")
                    print(f"[{ts_str}] {label:40s}  "
                          f"bytes={current:>10.0f}  delta={delta:>+10.0f}")

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        dev.logout()
        print("Disconnected.")


if __name__ == "__main__":
    main()
