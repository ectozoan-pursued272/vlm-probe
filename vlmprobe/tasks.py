"""Read task YAMLs, run, score."""
import json
import yaml
from pathlib import Path


def load_task(path):
    cfg = yaml.safe_load(open(path))
    return cfg


def score_exact(pred, ref):
    return pred.strip().lower() == ref.strip().lower()
