import csv
import glob
import os
import re
import statistics
from collections import defaultdict


def memory_to_mib(value):
    used = value.split("/")[0].strip()

    if used.endswith("GiB"):
        return float(used.replace("GiB", "")) * 1024

    if used.endswith("MiB"):
        return float(used.replace("MiB", ""))

    if used.endswith("KiB"):
        return float(used.replace("KiB", "")) / 1024

    if used.endswith("B"):
        return float(used.replace("B", "")) / (1024 * 1024)

    raise ValueError(f"Unidade de memória desconhecida: {value}")


files = glob.glob("results/final/*_resources.csv")

pattern = re.compile(
    r"(monolith|microservices)_(10|50|100)u_run([123])_resources\.csv"
)

run_results = []

for file in files:
    filename = os.path.basename(file)
    match = pattern.fullmatch(filename)

    if not match:
        continue

    architecture = match.group(1)
    users = int(match.group(2))
    run = int(match.group(3))

    samples = defaultdict(
        lambda: {
            "cpu": 0.0,
            "memory": 0.0
        }
    )

    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            elapsed = float(row["elapsed_seconds"])

            cpu = float(
                row["cpu_percent"]
                .replace("%", "")
                .strip()
            )

            memory = memory_to_mib(
                row["memory_usage"]
            )

            # Soma todos os containers naquele instante
            samples[elapsed]["cpu"] += cpu
            samples[elapsed]["memory"] += memory

    cpu_values = [
        sample["cpu"]
        for sample in samples.values()
    ]

    memory_values = [
        sample["memory"]
        for sample in samples.values()
    ]

    run_results.append({
        "architecture": architecture,
        "users": users,
        "run": run,
        "cpu_mean": statistics.mean(cpu_values),
        "cpu_peak": max(cpu_values),
        "memory_mean_mib": statistics.mean(memory_values),
        "memory_peak_mib": max(memory_values),
    })


run_results.sort(
    key=lambda x: (
        x["architecture"],
        x["users"],
        x["run"]
    )
)


# CSV por execução
with open(
    "results/final/resources_by_run.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    fields = [
        "architecture",
        "users",
        "run",
        "cpu_mean",
        "cpu_peak",
        "memory_mean_mib",
        "memory_peak_mib"
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fields
    )

    writer.writeheader()

    for row in run_results:
        writer.writerow({
            key: round(value, 2)
            if isinstance(value, float)
            else value
            for key, value in row.items()
        })


# Agrupa os 3 runs
groups = defaultdict(list)

for row in run_results:
    groups[
        (
            row["architecture"],
            row["users"]
        )
    ].append(row)


summary = []

for (architecture, users), rows in groups.items():

    cpu_means = [
        r["cpu_mean"] for r in rows
    ]

    memory_means = [
        r["memory_mean_mib"] for r in rows
    ]

    summary.append({
        "architecture": architecture,
        "users": users,

        "cpu_mean":
            statistics.mean(cpu_means),

        "cpu_std":
            statistics.stdev(cpu_means)
            if len(cpu_means) > 1
            else 0,

        "cpu_peak":
            max(r["cpu_peak"] for r in rows),

        "memory_mean_mib":
            statistics.mean(memory_means),

        "memory_std_mib":
            statistics.stdev(memory_means)
            if len(memory_means) > 1
            else 0,

        "memory_peak_mib":
            max(
                r["memory_peak_mib"]
                for r in rows
            ),
    })


summary.sort(
    key=lambda x: (
        x["architecture"],
        x["users"]
    )
)


# CSV consolidado
with open(
    "results/final/resources_summary.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    fields = [
        "architecture",
        "users",
        "cpu_mean",
        "cpu_std",
        "cpu_peak",
        "memory_mean_mib",
        "memory_std_mib",
        "memory_peak_mib"
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fields
    )

    writer.writeheader()

    for row in summary:
        writer.writerow({
            key: round(value, 2)
            if isinstance(value, float)
            else value
            for key, value in row.items()
        })


print("\n=== RESULTADOS POR RUN ===\n")

for row in run_results:
    print(
        f"{row['architecture']:14} "
        f"{row['users']:3} usuários "
        f"run {row['run']} | "
        f"CPU média={row['cpu_mean']:.2f}% | "
        f"CPU pico={row['cpu_peak']:.2f}% | "
        f"Mem média={row['memory_mean_mib']:.2f} MiB | "
        f"Mem pico={row['memory_peak_mib']:.2f} MiB"
    )


print("\n=== TABELA CONSOLIDADA ===\n")

print(
    f"{'Arquitetura':15} "
    f"{'Usuários':8} "
    f"{'CPU média':10} "
    f"{'CPU std':9} "
    f"{'CPU pico':10} "
    f"{'Mem média':12} "
    f"{'Mem std':10} "
    f"{'Mem pico':10}"
)

print("-" * 95)

for row in summary:
    print(
        f"{row['architecture']:15} "
        f"{row['users']:8} "
        f"{row['cpu_mean']:10.2f} "
        f"{row['cpu_std']:9.2f} "
        f"{row['cpu_peak']:10.2f} "
        f"{row['memory_mean_mib']:12.2f} "
        f"{row['memory_std_mib']:10.2f} "
        f"{row['memory_peak_mib']:10.2f}"
    )