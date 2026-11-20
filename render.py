#!/usr/bin/env python3
"""FIELDNOTES World Desk — build-time poster renderer.

Draws entry.png (1024x1024), a one-page newspaper front page summing up the
world news of Friday 20 November 2026. Build-time only: the shipped entry
program is main.py, which copies the rendered PNG. Every fact on the poster
is sourced in SOURCES.md; facts locked 12:11 UTC, 20 November 2026.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 46
CW = W - 2 * MARGIN  # content width

PAPER = (246, 241, 229)
INK = (22, 19, 14)
RED = (176, 32, 24)
MUTED = (98, 90, 74)
LINE = (198, 188, 164)
WHITE = (250, 248, 242)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF_I = FONT_DIR + "LiberationSerif-Italic.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"
MONO_B = FONT_DIR + "LiberationMono-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if text_w(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(d, xy, s, f, tracking, fill):
    """Draw text with extra letter tracking; returns the end x."""
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += text_w(d, ch, f) + tracking
    return x - tracking


def spaced_w(d, s, f, tracking):
    return sum(text_w(d, ch, f) for ch in s) + tracking * (len(s) - 1)


def block(d, x, y, text, f, lh, max_w, fill=INK):
    """Draw a wrapped paragraph; returns y after the last line."""
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def kicker(d, x, y, label, size=19):
    d.rectangle([x, y + 3, x + 10, y + 13], fill=RED)
    spaced(d, (x + 18, y), label, font(SANS_B, size), 2.2, RED)
    return y + size + 10


def panel(d, x, y, w, kick, head, head_size, stand, stand_size=16):
    y = kicker(d, x, y, kick, 17)
    y = block(d, x, y, head, font(SERIF_B, head_size), int(head_size * 1.15), w)
    y += 4
    y = block(d, x, y, stand, font(SANS, stand_size), int(stand_size * 1.375), w)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------------
    d.line([MARGIN, 30, W - MARGIN, 30], fill=INK, width=3)
    d.line([MARGIN, 36, W - MARGIN, 36], fill=INK, width=1)

    title = "FIELDNOTES"
    tf = font(SERIF_B, 86)
    tw = text_w(d, title, tf)
    d.text(((W - tw) / 2, 40), title, font=tf, fill=INK)

    sub_y = 136
    lf = font(SANS_B, 19)
    spaced(d, (MARGIN, sub_y), "WORLD DESK", lf, 3.0, INK)
    mid = "ONE PAGE · ONE DAY"
    mf = font(SANS, 17)
    mw = spaced_w(d, mid, mf, 2.0)
    spaced(d, ((W - mw) / 2, sub_y + 1), mid, mf, 2.0, MUTED)
    rt = "DAY EDITION"
    rw = spaced_w(d, rt, lf, 3.0)
    spaced(d, (W - MARGIN - rw, sub_y), rt, lf, 3.0, INK)
    d.line([MARGIN, 164, W - MARGIN, 164], fill=INK, width=1)

    # --- date band ------------------------------------------------------
    band_y = 174
    d.rectangle([MARGIN, band_y, W - MARGIN, band_y + 48], fill=INK)
    d.text((MARGIN + 18, band_y + 10), "FRIDAY 20 NOVEMBER 2026",
           font=font(SANS_B, 27), fill=WHITE)
    lock = "FACTS LOCKED 12:11 UTC"
    lf2 = font(MONO_B, 16)
    d.text((W - MARGIN - 18 - text_w(d, lock, lf2), band_y + 15), lock,
           font=lf2, fill=(214, 205, 182))

    # --- lead story -----------------------------------------------------
    y = 244
    d.line([MARGIN, y - 12, W - MARGIN, y - 12], fill=RED, width=2)
    y = kicker(d, MARGIN, y, "THE HAGUE — JUSTICE", 20)
    y = block(d, MARGIN, y, "WORLD COURT RULES MYANMAR COMMITTED GENOCIDE",
              font(SERIF_B, 50), 57, CW)
    y += 6
    y = block(d, MARGIN, y,
              "The ICJ finds the 2017 campaign against the Rohingya was "
              "genocide — the first time a state has been held responsible. "
              "Naypyidaw calls it unfair; Dhaka floats returns within 18 "
              "months for the 1.2m refugees in Bangladesh.",
              font(SANS, 20), 27, CW)
    y += 10
    d.line([MARGIN, y, W - MARGIN, y], fill=LINE, width=1)
    y += 12

    # --- four panels, two by two ----------------------------------------
    gap = 30
    col_w = (CW - gap) // 2
    x2 = MARGIN + col_w + gap
    row1 = y
    e1 = panel(d, MARGIN, row1, col_w, "SHENZHEN — DIPLOMACY",
               "TRUMP, XI, PUTIN SIGN 'PEACE DECLARATION'", 27,
               "First three-way summit, at APEC in Shenzhen, ends in a "
               "four-point declaration. Europe warns: no Ukraine deal "
               "without us. Canada and Japan cut side deals.")
    e2 = panel(d, x2, row1, col_w, "MARKETS — TECH",
               "ANTHROPIC HITS $2 TRILLION — STOCKS SINK ANYWAY", 27,
               "The biggest IPO ever briefly makes a $2tn company, closing "
               "+17%. Then the AI sell-off bites: S&P 500 −2%, a fifth "
               "straight fall; Nikkei −4.8%; gold −4.2%.")
    row2 = max(e1, e2) + 14
    e3 = panel(d, MARGIN, row2, col_w, "UKRAINE — WAR",
               "UKRAINE BLOWS CRIMEA BRIDGE SPAN; KYIV HIT", 27,
               "A third strike this week wrecks the bridge's road span and "
               "halts rail traffic. Overnight missiles damage three Kyiv "
               "bridges; six killed. Allies meet in Berlin.")
    e4 = panel(d, x2, row2, col_w, "RIYADH — MIDEAST",
               "HOUTHI MISSILE DAMAGES RIYADH'S PIF TOWER", 27,
               "The sovereign fund's HQ, the capital's tallest tower, is "
               "damaged in the strike, as Saudi air defences intercept "
               "another missile over the south.")
    y = max(e3, e4) + 12
    d.line([MARGIN, y, W - MARGIN, y], fill=LINE, width=1)
    y += 10

    # --- climate strip ----------------------------------------------------
    y = kicker(d, MARGIN, y, "COP31 — CLIMATE", 17)
    y = block(d, MARGIN, y, "AFRICA BIDS TO TRIPLE CLIMATE CASH",
              font(SERIF_B, 25), 29, CW)
    y = block(d, MARGIN, y,
              "Europe answers: spend what is already pledged. Meta rethinks "
              "its 2030 climate goals as AI data centres push emissions up.",
              font(SERIF_I, 18), 24, CW)

    # --- ticker -----------------------------------------------------------
    tick_y = H - 74
    d.rectangle([0, tick_y, W, H], fill=INK)
    tf2 = font(MONO_B, 15)
    lines = wrap(d,
                 "GTA VI'S FIRST DAY: EST. $2.36BN — BIGGEST ENTERTAINMENT "
                 "LAUNCH EVER (SENSOR TOWER) · ESTONIA SHUTS RUSSIAN BORDER "
                 "FROM 1 DEC · US CYBER CHIEF OUSTED AFTER OUTAGE WAVE · "
                 "LAS VEGAS GP PRACTICE WASHED OUT",
                 tf2, CW)
    ty = tick_y + 13
    for line in lines[:3]:
        d.text((MARGIN, ty), line, font=tf2, fill=WHITE)
        ty += 21

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
