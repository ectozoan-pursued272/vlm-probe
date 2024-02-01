"""Read task YAMLs, run, score."""
import json
import yaml
from pathlib import Path


def load_task(path):
    cfg = yaml.safe_load(open(path))
    return cfg


def score_exact(pred, ref):
    return pred.strip().lower() == ref.strip().lower()


import re


def parse_number(text):
    m = re.search(r"-?\d+", text)
    return m.group(0) if m else text.strip()


def score_count(pred, ref):
    return parse_number(pred) == ref.strip()


def score_exact_word(pred, ref):
    # NOTE: don't strip leading articles. "the cat" must NOT match "the dog".
    return pred.strip().lower() == ref.strip().lower()
