"""Smoke test: tasks load, scoring works on toy values."""
import os
import tempfile
import textwrap

from vlmprobe.tasks import load, score_one, aggregate


def test_load_and_score(tmp_path):
    yaml_path = tmp_path / "t.yaml"
    yaml_path.write_text(textwrap.dedent("""
    name: count_objects
    items:
      - image: x.jpg
        prompt: how many?
        answer: "3"
    """))
    task = load(str(yaml_path))
    assert task["name"] == "count_objects"
    assert score_one(task, "3", "3")
    assert score_one(task, "There are 3 cats.", "3")
    assert not score_one(task, "There are five cats.", "3")


def test_aggregate():
    recs = [
        {"task": "count_objects", "correct": True},
        {"task": "count_objects", "correct": False},
        {"task": "spatial_rel",   "correct": True},
    ]
    out = aggregate(recs)
    assert abs(out["count_objects"] - 0.5) < 1e-9
    assert out["spatial_rel"] == 1.0


def test_score_letter():
    task = {"name": "spatial_rel"}
    assert score_one(task, "b. no", "B")
    assert score_one(task, "Yes, it is.", "Y")
    assert not score_one(task, "No.", "Y")


def test_aggregate_empty_safe():
    assert aggregate([]) == {}
