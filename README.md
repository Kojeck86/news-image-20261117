# The World in One Page — 17 November 2026

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Kojeck86/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Kojeck86/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

Entry for [news-image-20261117](https://make.fun/bounty/news-image-20261117):
one image that sums up the world's news of **Tuesday 17 November 2026**.

`main.py` (Python 3.13, standard library only) draws a newspaper front
page procedurally — no network, no system fonts, no image files. Text is
rendered with an embedded 5×7 bitmap font; every picture (the Kerch
bridge, the radar dish, the airliner, the jet, the scales) is drawn from
shapes. The program runs twice and writes byte-identical output.

The page is built to be read without a news feed: the masthead names the
day, the lead story carries the biggest event with a picture of it, and
each of the four secondary stories pairs a headline with its own
illustration, so a viewer who missed the day can tell what happened
from the image alone.

## The day's news

- **Lead:** bridges under fire — the Kerch road span collapses into the
  sea while Russian missiles hit Kyiv's North and South bridges over the
  Dnipro, cutting heat, water and power.
- Iran drone hits a US radar site in Bahrain; a US carrier arrives and a
  tanker is struck near Hormuz.
- Trump flies to Asia for the APEC summit, with a trilateral with Xi
  Jinping and Putin set for 19 November.
- Japan scrambles jets after Russian planes are accused of violating its
  airspace.
- Britain sanctions eight Israeli firms building settlements in the West
  Bank.
- Also today: the US loses its measles-free status after nearly 30
  years; Gérard Depardieu pleads guilty; Houthis advance in Yemen;
  five EU states plan a joint Rwanda deportation hub.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024 PNG, under 1 MiB). Run it twice and
compare hashes — the bytes are identical every time.

## License

MIT — see [LICENSE](LICENSE).
