"""Per-task confusion histogram on a results JSON. Text only — no plot deps."""
import argparse
import collections
import json


def main():
    p = argparse.ArgumentParser()
    p.add_argument("results_json")
    p.add_argument("--task", default=None)
    args = p.parse_args()

    d = json.load(open(args.results_json))
    rows = d["records"]
    if args.task:
        rows = [r for r in rows if r["task"] == args.task]
    by_ref = collections.defaultdict(collections.Counter)
    for r in rows:
        by_ref[r["answer"]][r["pred"].strip().lower()[:20]] += 1
    for ref, counts in sorted(by_ref.items()):
        total = sum(counts.values())
        print(f"\n=== answer = {ref!r}  (n={total}) ===")
        for pred, c in counts.most_common(5):
            bar = "#" * int(40 * c / total)
            print(f"  {c:>3d}  {bar:<40s}  {pred!r}")


if __name__ == "__main__":
    main()
