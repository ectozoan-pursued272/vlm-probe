"""Render results.csv -> a tiny static HTML table for the writeup."""
import argparse
import csv
import html


HEAD = """<!doctype html><meta charset=utf-8>
<title>vlm-probe results</title>
<style>
  body { font: 14px/1.4 system-ui, sans-serif; max-width: 720px; margin: 2em auto; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border-bottom: 1px solid #ddd; padding: 6px 10px; text-align: right; }
  th:first-child, td:first-child { text-align: left; }
</style>
<h1>vlm-probe results</h1>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--out", default="results/report.html")
    args = p.parse_args()

    with open(args.csv) as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("empty csv")

    cols = list(rows[0].keys())
    out = [HEAD, "<table><thead><tr>"]
    out.extend(f"<th>{html.escape(c)}</th>" for c in cols)
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>")
        for c in cols:
            v = (r.get(c) or "").strip()
            if c != "model" and v:
                try:
                    v = f"{float(v):.3f}"
                except ValueError:
                    pass
            out.append(f"<td>{html.escape(v)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    open(args.out, "w").write("\n".join(out))
    print("wrote", args.out)


if __name__ == "__main__":
    main()
