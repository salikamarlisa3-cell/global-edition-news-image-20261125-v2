# Global Edition — The World in One Day

[![Competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/salikamarlisa3-cell/global-edition-news-image-20261125-v2/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/salikamarlisa3-cell/global-edition-news-image-20261125-v2/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single 1024x1024 poster carrying one full day of world news:
**Wednesday 25 November 2026** — 56 verified stories across 7 regions,
each with its outlet tag on the poster and a full source link in
[SOURCES.md](SOURCES.md).

On the poster:

- three front-page leads (the Dow's first close above 50,000, the two
  tankers that struck mines in the Strait of Hormuz, and the killing of
  Hamas's interior security chief in Gaza City)
- a dot-matrix world map with 16 numbered pins that match the index
- sixteen small panels — the day in pictures, drawn in code
- a by-the-numbers strip and an eight-city weather strip
- the full 56-story index in seven regional columns
- a UTC timeline of how the day unfolded, and a "left out & why" box
  recording what was held for verification and which early claim the
  confirmed reporting superseded

Security and diplomacy stories were refreshed against the Just
Security Early Edition of 25 Nov 2026 itself; the rest come from the
wires and outlets named per story.

## Run it

```sh
python3 main.py   # writes entry.png (1024x1024) next to main.py
```

Requires Python 3 and Pillow. The generator is deterministic — no
clock, no randomness — so two runs produce a byte-identical poster.

## License

MIT — see [LICENSE](LICENSE).
