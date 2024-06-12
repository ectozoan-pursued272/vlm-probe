"""Download / unpack the small image bundle used in the tasks.

The bundle is ~500 MB of CC-BY images plus a few synthetic compositions we made
ourselves. URL is pinned in the README.
"""
import argparse
import hashlib
import os
import sys
import urllib.request

BUNDLE_URL = "https://example.org/vlm-probe/images-v1.tar.gz"  # FIXME: replace with real host
BUNDLE_SHA = "5a4f0e9a8c2b1d3e7f6a9c0d4e2b1a3c5d8f7e6a9c0d4e2b1a3c5d8f7e6a9c0d"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    tgz = os.path.join(args.out, "images-v1.tar.gz")
    if not os.path.exists(tgz):
        print("downloading", BUNDLE_URL)
        urllib.request.urlretrieve(BUNDLE_URL, tgz)
    got = sha256(tgz)
    if got != BUNDLE_SHA:
        print("warning: SHA mismatch")
        print("  expected", BUNDLE_SHA)
        print("  got     ", got)
    os.system(f"tar xzf {tgz} -C {args.out}")
    print("ready:", args.out)


if __name__ == "__main__":
    main()
