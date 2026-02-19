# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

"""Real-time traffic monitor using the datacollection API.

Displays a live matplotlib chart of rx/tx bytes for one or more
network interfaces.  Press Ctrl+C or close the window to stop.

Usage:
    python traffic_monitor.py <host> <user> <password> [interface ...]

Examples:
    python traffic_monitor.py 192.168.0.254 admin admin ETH1 ETH2
    python traffic_monitor.py 192.168.0.254 admin admin          # auto-detect
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict, deque

WINDOW = 600          # seconds of data visible on the chart
POLL_INTERVAL = 10000  # milliseconds between updates (data arrives every ~10s)


def discover_interfaces(dev):
    """Return sorted list of interface names from available metrics."""
    raw = dev.call("datacollection", "get_metrics")
    metrics = raw.get("result", [])
    interfaces = set()
    for m in metrics:
        if m.endswith(".rx_bytes"):
            interfaces.add(m.rsplit(".", 2)[0])
    return sorted(interfaces)


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    host, user, password = sys.argv[1], sys.argv[2], sys.argv[3]
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, user, password)

    interfaces = sys.argv[4:] if len(sys.argv) > 4 else discover_interfaces(dev)
    if not interfaces:
        print("No interfaces found.")
        dev.logout()
        sys.exit(1)

    print(f"Monitoring: {', '.join(interfaces)}")

    # metrics to query
    rx_metrics = [f"{iface}.rx_bytes" for iface in interfaces]
    tx_metrics = [f"{iface}.tx_bytes" for iface in interfaces]
    all_metrics = rx_metrics + tx_metrics

    # rolling data store: {metric: deque of (timestamp, value)}
    history = defaultdict(lambda: deque(maxlen=WINDOW))

    # set up the plot
    fig, (ax_rx, ax_tx) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle(f"Traffic Monitor — {host}")
    ax_rx.set_ylabel("RX (bytes/s)")
    ax_tx.set_ylabel("TX (bytes/s)")
    ax_tx.set_xlabel("Time (s ago)")

    colors = plt.cm.tab10.colors
    lines_rx = {}
    lines_tx = {}
    for i, iface in enumerate(interfaces):
        c = colors[i % len(colors)]
        lines_rx[iface], = ax_rx.plot([], [], label=iface, color=c)
        lines_tx[iface], = ax_tx.plot([], [], label=iface, color=c)

    ax_rx.legend(loc="upper left", fontsize="small")
    ax_tx.legend(loc="upper left", fontsize="small")
    ax_rx.grid(True, alpha=0.3)
    ax_tx.grid(True, alpha=0.3)
    fig.tight_layout()

    def update(_frame):
        now = int(time.time())
        try:
            result = dev.call("datacollection", "get_values_as_table",
                              metrics=all_metrics,
                              **{"from": now - WINDOW, "to": now,
                                 "resolution": 1})
        except Exception as e:
            print(f"Query error: {e}")
            return

        data = result.get("result", result)
        for metric, points in data.items():
            history[metric].clear()
            for p in points:
                if p["val"] is not None:
                    history[metric].append((p["ts"], p["val"]))

        for iface in interfaces:
            rx_key = f"{iface}.rx_bytes"
            tx_key = f"{iface}.tx_bytes"

            if history[rx_key]:
                ts, vals = zip(*history[rx_key])
                x = [t - now for t in ts]
                lines_rx[iface].set_data(x, vals)

            if history[tx_key]:
                ts, vals = zip(*history[tx_key])
                x = [t - now for t in ts]
                lines_tx[iface].set_data(x, vals)

        for ax in (ax_rx, ax_tx):
            ax.set_xlim(-WINDOW, 0)
            ax.relim()
            ax.autoscale_view(scalex=False, scaley=True)

    ani = animation.FuncAnimation(fig, update, interval=POLL_INTERVAL,
                                  cache_frame_data=False)
    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        dev.logout()
        print("Disconnected.")


if __name__ == "__main__":
    main()
