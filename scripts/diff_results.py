"""Show per-task accuracy delta between two result JSONs."""
import json
import sys


def main():
    a = json.load(open(sys.argv[1]))
    b = json.load(open(sys.argv[2]))
    keys = sorted(set(a["summary"]) | set(b["summary"]))
    print(f"{'task':<20s}  {a['model']:<25s}  {b['model']:<25s}  delta")
    for k in keys:
        va = a["summary"].get(k, float("nan"))
        vb = b["summary"].get(k, float("nan"))
        print(f"{k:<20s}  {va:<25.3f}  {vb:<25.3f}  {vb - va:+.3f}")


if __name__ == "__main__":
    main()
