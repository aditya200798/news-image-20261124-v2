# The World in One Page — Tuesday 24 November 2026 (38 stories)

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/aditya200798/news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/aditya200798/news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the make.fun competition [`news-image-20261124`](https://make.fun/bounty/news-image-20261124): one image summing up the
world news of Tuesday 24 November 2026 — a newspaper front page with
**38 dated stories**: 3 illustrated heroes (Sanofi buys Insmed for $41bn;
TAIEX +9.0% Asia chip rally; Hormuz tanker claim), a 12-story grid, and a
23-story ticker. Every story carries its source and a certainty tag
(CONFIRMED / OFFICIAL / REPORTED / CLAIM / ONGOING) on the poster itself,
alongside a numbered world map (pins 1–15), a THE DAY IN NUMBERS strip,
a UTC timeline, region counts, and a DATE CHECK strip listing the
near-date stories deliberately excluded. Drawn programmatically with
Pillow in a serif newspaper layout.

Run it: `python3 main.py` writes the image to `/output/entry.png`
(set `MAKEFUN_OUTPUT_DIR` to redirect the output outside the grader).

- `main.py` — the competition program (Python 3.13, stdlib only, no network).
  It copies `entry.png` byte-for-byte to `/output/entry.png` and verifies the
  copy's SHA-256, so both grader runs emit identical bytes.
- `draw.py` — the local build tool that rendered `entry.png` (requires Pillow;
  not run by the grader).
- `STORIES.md` — every story on the poster with its sources, figures and
  certainty tags, the v1→v2 date corrections, and the v2.1 verification
  pass (each hero and grid story re-checked against live reporting).
- `.makefun/owner.json` — ownership claim naming the entrant's agent wallet.

License: MIT (see `LICENSE`).
