"""Main eval driver."""
import argparse
import json
from pathlib import Path

from .model import load_llava, generate
from .tasks import load_task, score_exact


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True)
    args = p.parse_args()

    proc, model = load_llava()
    cfg = load_task(args.task)
    n_correct = 0
    for item in cfg["items"]:
        pred = generate(proc, model, item["image"], item["prompt"])
        ok = score_exact(pred, item["answer"])
        n_correct += int(ok)
    print(n_correct, "/", len(cfg["items"]))


if __name__ == "__main__":
    main()
