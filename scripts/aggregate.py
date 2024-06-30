"""Aggregate a directory of result JSONs into a CSV."""
import argparse
import csv
import glob
import json
import os


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results_dir", required=True)
    p.add_argument("--out",         required=True)
    args = p.parse_args()

    rows = []
    tasks = set()
    for path in glob.glob(os.path.join(args.results_dir, "*.json")):
        d = json.load(open(path))
        rows.append({"model": d.get("model", os.path.basename(path)), **d["summary"]})
        tasks.update(d["summary"].keys())

    fieldnames = ["model"] + sorted(tasks)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})
    print("wrote", args.out)


if __name__ == "__main__":
    main()
