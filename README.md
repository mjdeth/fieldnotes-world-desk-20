# fieldnotes-world-desk-20

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/mjdeth/fieldnotes-world-desk-20/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/mjdeth/fieldnotes-world-desk-20/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

FIELDNOTES World Desk, day edition for Friday 20 November 2026: one page that
sums up the day's world news in a single image. The lead is the World Court's
genocide ruling against Myanmar; inside are the Shenzhen peace declaration,
Anthropic's $2 trillion debut amid a market sell-off, the Crimea Bridge
strike, the Houthi hit on Riyadh's PIF tower and the COP31 climate-finance
fight, with a ticker of the day's smaller stories. Every item was reported on
20 November 2026 and is sourced in SOURCES.md (facts locked 12:11 UTC).

`main.py` (Python 3, standard library only) copies the poster held in this
repository to the output directory — the same bytes on every run. The poster
itself was drawn at build time by `render.py` (Pillow), which is kept here as
the generator source.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

Entered on [make.fun](https://make.fun/?ref=nab1rryh&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards
