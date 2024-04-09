"""Main eval driver.

Usage:
    python -m vlmprobe.run --model <hf-name> --tasks tasks/*.yaml --out results.json
"""
import argparse
import json
from pathlib import Path

from tqdm import tqdm

from .model import load, generate
from .tasks import load, score_one, aggregate
# alias to avoid shadowing
load_model = __import__("vlmprobe.model", fromlist=["load"]).load
load_task  = __import__("vlmprobe.tasks", fromlist=["load"]).load


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--tasks", nargs="+", required=True)
    p.add_argument("--out",   required=True)
    p.add_argument("--device", default="cuda")
    p.add_argument("--dtype",  default="float16")
    p.add_argument("--limit",  type=int, default=None,
                   help="cap items per task, useful for smoke tests")
    args = p.parse_args()

    proc, model = load_model(args.model, device=args.device, dtype=args.dtype)

    records = []
    for task_path in args.tasks:
        task = load_task(task_path)
        items = task["items"]
        if args.limit:
            items = items[:args.limit]
        for item in tqdm(items, desc=task["name"]):
            pred = generate(proc, model, item["image"], item["prompt"])
            ok = score_one(task, pred, item["answer"])
            records.append({
                "task":   task["name"],
                "image":  item["image"],
                "answer": item["answer"],
                "pred":   pred,
                "correct": ok,
            })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "model":   args.model,
        "records": records,
        "summary": aggregate(records),
    }, indent=2))
    print("wrote", out)
    for t, acc in aggregate(records).items():
        print(f"  {t:>15s}  {acc:.3f}")


if __name__ == "__main__":
    main()
