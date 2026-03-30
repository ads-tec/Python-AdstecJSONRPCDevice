# System Monitoring

The [`datacollection`](../api-reference/jsonrpc-methods.md#datacollection-traffic-system-statistics) API exposes real-time system resource metrics collected by the `system-datacollectd` service. These metrics cover CPU usage (aggregate and per core), memory usage, load averages, and system uptime.

!!! info "Firmware requirement"
    System metrics are available from firmware **IRF 2.2.8 / AWT 14.2.8** onwards.

## Discovering System Metrics

List all `system.*` metrics available on the device:

```python
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

raw = dev.call("datacollection", "get_metrics")
system_metrics = sorted(
    m for m in raw["result"] if m.startswith("system.")
)
for m in system_metrics:
    print(m)

dev.logout()
```

Example output on a 4-core device:

```
system.cpu
system.cpu.0
system.cpu.1
system.cpu.2
system.cpu.3
system.memory.free
system.memory.total
system.memory.used
system.load.1
system.load.5
system.load.15
system.uptime
```

## Querying CPU and Memory

Query the last 5 minutes of CPU and memory data:

```python
import time
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

now = int(time.time())
metrics = ["system.cpu", "system.memory.used", "system.memory.total"]

raw = dev.call("datacollection", "get_values_as_table",
    metrics=metrics,
    **{"from": now - 300, "to": now, "resolution": 1})
data = raw["result"]

# Latest CPU usage
cpu_points = data.get("system.cpu", [])
latest_cpu = next(
    (p["val"] for p in reversed(cpu_points) if p["val"] is not None), None
)
if latest_cpu is not None:
    print(f"CPU usage: {latest_cpu:.1f}%")

# Latest memory usage
mem_used = data.get("system.memory.used", [])
mem_total = data.get("system.memory.total", [])
latest_used = next(
    (p["val"] for p in reversed(mem_used) if p["val"] is not None), None
)
latest_total = next(
    (p["val"] for p in reversed(mem_total) if p["val"] is not None), None
)
if latest_used is not None and latest_total is not None and latest_total > 0:
    pct = latest_used / latest_total * 100
    print(f"Memory: {latest_used / 1048576:.1f} / {latest_total / 1048576:.1f} MB ({pct:.1f}%)")

dev.logout()
```

## Monitoring Load Averages

```python
import time
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

now = int(time.time())
raw = dev.call("datacollection", "get_values_as_table",
    metrics=["system.load.1", "system.load.5", "system.load.15"],
    **{"from": now - 60, "to": now, "resolution": 1})
data = raw["result"]

for key in ["system.load.1", "system.load.5", "system.load.15"]:
    points = data.get(key, [])
    latest = next(
        (p["val"] for p in reversed(points) if p["val"] is not None), None
    )
    label = key.replace("system.load.", "") + "min"
    print(f"Load {label}: {latest:.2f}" if latest is not None else f"Load {label}: n/a")

dev.logout()
```

## Continuous System Monitoring

Poll all system metrics every 10 seconds and print a status line:

```python
import time
import jsonrpcdevice

dev = jsonrpcdevice.AdstecJSONRPCDevice("192.168.0.254", "admin", "admin")

# Discover per-core CPU metrics
raw = dev.call("datacollection", "get_metrics")
cpu_cores = sorted(
    m for m in raw["result"]
    if m.startswith("system.cpu.") and m != "system.cpu"
)

all_metrics = (
    ["system.cpu"] + cpu_cores +
    ["system.memory.used", "system.memory.free", "system.memory.total",
     "system.load.1", "system.load.5", "system.load.15",
     "system.uptime"]
)

print(f"Monitoring {len(cpu_cores)} CPU cores. Press Ctrl+C to stop.\n")

try:
    while True:
        now = int(time.time())
        raw = dev.call("datacollection", "get_values_as_table",
            metrics=all_metrics,
            **{"from": now - 30, "to": now, "resolution": 1})
        data = raw["result"]

        def latest(metric):
            points = data.get(metric, [])
            for p in reversed(points):
                if p["val"] is not None:
                    return p["val"]
            return None

        ts = time.strftime("%H:%M:%S")
        cpu = latest("system.cpu")
        mem_used = latest("system.memory.used")
        mem_total = latest("system.memory.total")
        load1 = latest("system.load.1")
        uptime = latest("system.uptime")

        parts = [f"[{ts}]"]
        if cpu is not None:
            parts.append(f"CPU: {cpu:5.1f}%")
        for core in cpu_cores:
            val = latest(core)
            if val is not None:
                parts.append(f"{core.split('.')[-1]}:{val:.0f}%")
        if mem_used is not None and mem_total is not None and mem_total > 0:
            pct = mem_used / mem_total * 100
            parts.append(f"MEM: {pct:5.1f}%")
        if load1 is not None:
            parts.append(f"LOAD: {load1:.2f}")
        if uptime is not None:
            h, rem = divmod(int(uptime), 3600)
            m, s = divmod(rem, 60)
            parts.append(f"UP: {h}h{m:02d}m")

        print("  ".join(parts))
        time.sleep(10)

except KeyboardInterrupt:
    print("\nStopped.")
finally:
    dev.logout()
```

Example output:

```
Monitoring 4 CPU cores. Press Ctrl+C to stop.

[14:20:30]  CPU:  12.3%  0:18%  1:8%  2:14%  3:9%  MEM:  43.2%  LOAD: 0.45  UP: 72h14m
[14:20:40]  CPU:  15.1%  0:22%  1:10%  2:17%  3:11%  MEM:  43.3%  LOAD: 0.48  UP: 72h14m
[14:20:50]  CPU:   9.8%  0:12%  1:7%  2:11%  3:9%  MEM:  43.2%  LOAD: 0.44  UP: 72h14m
```

!!! info "Data collection interval"
    The device collects system metrics every **10 seconds**. Polling faster than this interval will not produce additional data points. Unlike network traffic metrics (which are deltas), system metrics are **point-in-time gauge values** — they represent the instantaneous reading at each collection interval.

!!! tip "Combine with status properties"
    For a one-off snapshot, the `cpustat` [status property](../api-reference/status-properties.md) returns CPU information without time-series history. Use `datacollection` when you need historical data or continuous monitoring.

See also the [`examples/system_monitor.py`](https://github.com/ads-tec/Python-AdstecJSONRPCDevice/tree/main/examples/system_monitor.py) script for a ready-to-run version.
