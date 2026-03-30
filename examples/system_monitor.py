# Copyright (c) 2026 ads-tec Industrial IT GmbH, Germany
# Licensed under the BSD 2-Clause License. See LICENSE file for details.

"""Real-time system resource monitor using the datacollection API.

Polls CPU usage (aggregate and per core), memory, load averages, and
uptime every 10 seconds.  Press Ctrl+C to stop.

Requires firmware 2.2.8 or later (system-datacollectd).

Usage:
    python system_monitor.py <host> <user> <password>

Examples:
    python system_monitor.py 192.168.0.254 admin admin
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jsonrpcdevice

POLL_INTERVAL = 10  # seconds (data arrives every ~10s)


def discover_system_metrics(dev):
    """Return sorted list of all system.* metric names."""
    raw = dev.call("datacollection", "get_metrics")
    return sorted(m for m in raw.get("result", []) if m.startswith("system."))


def latest_value(data, metric):
    """Return the most recent non-null value for a metric, or None."""
    points = data.get(metric, [])
    for p in reversed(points):
        if p["val"] is not None:
            return p["val"]
    return None


def format_uptime(seconds):
    """Format uptime seconds as 'Xd Yh Zm'."""
    if seconds is None:
        return "n/a"
    seconds = int(seconds)
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    if days > 0:
        return f"{days}d {hours}h{minutes:02d}m"
    return f"{hours}h{minutes:02d}m"


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    host, user, password = sys.argv[1], sys.argv[2], sys.argv[3]
    dev = jsonrpcdevice.AdstecJSONRPCDevice(host, user, password)

    # discover available system metrics
    system_metrics = discover_system_metrics(dev)
    if not system_metrics:
        print("No system.* metrics found. Is the firmware >= 2.2.8?")
        dev.logout()
        sys.exit(1)

    cpu_cores = sorted(
        m for m in system_metrics
        if m.startswith("system.cpu.") and m != "system.cpu"
    )

    print(f"Device: {host}")
    print(f"System metrics: {len(system_metrics)} ({len(cpu_cores)} CPU cores)")
    print(f"Polling every {POLL_INTERVAL}s. Press Ctrl+C to stop.\n")

    # header
    core_hdrs = "  ".join(f"C{m.split('.')[-1]:>2s}" for m in cpu_cores)
    print(f"{'Time':>8s}  {'CPU':>5s}  {core_hdrs}  "
          f"{'MEM%':>5s}  {'MEM_MB':>8s}  "
          f"{'LD1':>5s}  {'LD5':>5s}  {'LD15':>5s}  {'Uptime':>10s}")
    print("-" * (50 + len(cpu_cores) * 5))

    try:
        while True:
            now = int(time.time())
            try:
                raw = dev.call("datacollection", "get_values_as_table",
                               metrics=system_metrics,
                               **{"from": now - 30, "to": now,
                                  "resolution": 1})
            except Exception as e:
                print(f"Query error: {e}")
                time.sleep(POLL_INTERVAL)
                continue

            data = raw.get("result", {})
            ts = time.strftime("%H:%M:%S")

            cpu = latest_value(data, "system.cpu")
            mem_used = latest_value(data, "system.memory.used")
            mem_total = latest_value(data, "system.memory.total")
            load1 = latest_value(data, "system.load.1")
            load5 = latest_value(data, "system.load.5")
            load15 = latest_value(data, "system.load.15")
            uptime = latest_value(data, "system.uptime")

            # per-core CPU
            core_vals = []
            for m in cpu_cores:
                val = latest_value(data, m)
                core_vals.append(f"{val:4.0f}" if val is not None else "   -")

            # memory percentage
            mem_pct = ""
            mem_mb = ""
            if mem_used is not None and mem_total is not None and mem_total > 0:
                mem_pct = f"{mem_used / mem_total * 100:5.1f}"
                mem_mb = f"{mem_used / 1048576:.0f}/{mem_total / 1048576:.0f}"

            print(
                f"{ts:>8s}  "
                f"{cpu:5.1f}  " if cpu is not None else f"{'-':>5s}  ",
                end="",
            )
            print("  ".join(core_vals), end="  ")
            print(
                f"{mem_pct:>5s}  {mem_mb:>8s}  "
                f"{load1:5.2f}  " if load1 is not None else f"{'-':>5s}  ",
                end="",
            )
            print(
                f"{load5:5.2f}  " if load5 is not None else f"{'-':>5s}  ",
                end="",
            )
            print(
                f"{load15:5.2f}  " if load15 is not None else f"{'-':>5s}  ",
                end="",
            )
            print(f"{format_uptime(uptime):>10s}")

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        dev.logout()
        print("Disconnected.")


if __name__ == "__main__":
    main()
