import argparse
import csv
import json
import subprocess
import time
from datetime import datetime


parser = argparse.ArgumentParser()

parser.add_argument("--output", required=True)
parser.add_argument("--duration", type=int, default=120)
parser.add_argument("--interval", type=int, default=5)
parser.add_argument("containers", nargs="+")

args = parser.parse_args()


def collect(container):
    result = subprocess.run(
        [
            "docker",
            "stats",
            "--no-stream",
            "--format",
            "{{json .}}",
            container,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(result.stdout.strip())


with open(args.output, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "elapsed_seconds",
        "container",
        "cpu_percent",
        "memory_usage",
        "memory_percent",
    ])

    start = time.monotonic()
    next_sample = start

    while True:
        now = time.monotonic()
        elapsed = now - start

        if elapsed >= args.duration:
            break

        for container in args.containers:
            stats = collect(container)

            writer.writerow([
                datetime.now().isoformat(),
                round(elapsed, 2),
                container,
                stats["CPUPerc"],
                stats["MemUsage"],
                stats["MemPerc"],
            ])

            file.flush()

        next_sample += args.interval

        sleep_time = next_sample - time.monotonic()

        if sleep_time > 0:
            time.sleep(sleep_time)