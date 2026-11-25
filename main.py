#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261124 (v2).

The deliverable is one image: a newspaper front page summing up the world
news of Tuesday 24 November 2026 - 38 dated stories (3 illustrated heroes,
a 12-story grid, a 23-line ticker), a numbered world map whose pins match
stories 1-15, a THE DAY IN NUMBERS strip, a UTC timeline, per-region story
counts and a DATE CHECK strip naming the near-date stories left out.

The poster itself (entry.png) was drawn programmatically for this entry
(see draw.py and STORIES.md in this repository) and is stored alongside
this program. Running the program copies entry.png byte-for-byte to the
output directory, so repeated grader runs emit identical bytes.

Standard library only. No network access.
Outside the grader, MAKEFUN_OUTPUT_DIR overrides the default /output.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    # Verify the copy: a truncated or altered image must fail loudly
    # rather than be graded as this entry's output.
    src_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    out_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
    if out_hash != src_hash:
        raise SystemExit(f"copy verification failed: {out_hash} != {src_hash}")
    print(f"wrote {dest} ({dest.stat().st_size} bytes, sha256 {out_hash})")


if __name__ == "__main__":
    main()
