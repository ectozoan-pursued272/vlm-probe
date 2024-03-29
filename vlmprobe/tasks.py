"""Task loader + scorer.

Tasks are YAML, e.g.:

    name: count_objects
    items:
      - image: data/images/IMG_0001.jpg
        prompt: "How many cats are in the image? Answer with a number."
        answer: "3"
"""
import json
import re
import yaml
from pathlib import Path


def load(path):
    cfg = yaml.safe_load(open(path))
    cfg["__path__"] = str(path)
    return cfg


def parse_number(text):
    m = re.search(r"-?\d+", text)
    return m.group(0) if m else text.strip()


def score_one(task, pred, ref):
    name = task["name"]
    if name == "count_objects":
        return parse_number(pred) == ref.strip()
    # multiple-choice tasks: accept either the letter or the full word answer
    letter = re.match(r"^\s*([a-d])\b", pred.lower())
    if letter:
        return letter.group(1) == ref.strip().lower()[:1]
    return pred.strip().lower().startswith(ref.strip().lower())


def aggregate(records):
    by_task = {}
    for r in records:
        by_task.setdefault(r["task"], []).append(r["correct"])
    return {t: sum(v) / len(v) for t, v in by_task.items()}
