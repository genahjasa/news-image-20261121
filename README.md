# The World — 21 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A single-image front page summing up 21 November 2026's world news.
Built for the [news-image-20261121](https://make.fun) bounty.

## What's on the page

Four stories lead the day:

- The International Court of Justice finds Myanmar guilty of genocide
  against the Rohingya — the first state ever found guilty by an
  international court.
- Russia strikes Ukraine again: missiles on Kryvyi Rih leave 2 dead and
  42 hurt, and Poland reports an airspace incursion.
- JPMorgan, Visa and Mastercard report a cyberattack on third-party
  vendors.
- The US Senate rejects the Iran war-powers resolution, 51–48.

## Run it

```bash
python3 main.py
```

The program validates `image.jpg` (JPEG markers, dimensions, under
1 MiB, sha256) and copies it byte-for-byte to `/output/entry.png`.
Pure Python standard library — no third-party packages.

```bash
python3 main.py --output /tmp/entry.png
```

## How the image was made

The collage is a 1024×1024 front page: a masthead, a 2×2 grid of
story panels, headlines with subheads, and a footer. Every headline
was checked against live news reporting from 21 November 2026 before
it went on the page.

## Referral

Made with [make.fun](https://make.fun/r/maqpwds7) — build, submit, earn.
