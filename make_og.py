#!/usr/bin/env python3
"""make_og.py — og.png 1200x630 for Deanna's Wine Bar & Bert's Pig Shop demo host.
Fork of the honey-bistro painter (lane pattern). Header-line width guards live:
tracked mono lines get measured and asserted before save (jeyas 2026-11-25 lesson:
shorten the line, never shrink tracking below 4). Palette = site wine-label system."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public", "og.png")

W, H = 1200, 630
INK = (32, 10, 18)      # --ink
WINE_DK = (92, 22, 38)  # --wine-dk
WINE = (126, 34, 53)    # --wine
CREAM = (246, 239, 225)
BLUSH = (226, 183, 166)
WALK = (47, 90, 63)     # kept-walkway green hairline

def F(size, bold=False, italic=False):
    cands = []
    if bold:
        cands += ["/System/Library/Fonts/Supplemental/Iowan Old Style Bold.ttf",
                  "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"]
    elif italic:
        cands += ["/System/Library/Fonts/Supplemental/Iowan Old Style Italic.ttf",
                  "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"]
    cands += ["/System/Library/Fonts/Supplemental/Iowan Old Style Roman.ttf",
              "/System/Library/Fonts/Supplemental/Times New Roman.ttf"]
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                continue
    return ImageFont.load_default()

def MONO(size):
    for c in ["/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf"]:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                continue
    return ImageFont.load_default()

def tracked_width(draw, text, font, tracking):
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=font) + tracking
    return total - tracking

def center(draw, y, text, font, fill, tracking=0):
    tw = tracked_width(draw, text, font, tracking)
    x = (W - tw) // 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return tw

os.makedirs(os.path.join(HERE, "public"), exist_ok=True)
img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# wine-label double frame, cream on ink; green hairline = kept walkway homage
d.rectangle((0, 0, W - 1, 6), fill=WALK)
d.rectangle((26, 26, W - 27, H - 27), outline=BLUSH, width=1)
d.rectangle((34, 34, W - 35, H - 35), outline=WINE, width=3)

rows = [
    ( 68, "PIG-TO-TABLE WINE BAR",                     MONO(24),  10, BLUSH),
    (104, "WEST ASHLEY \u2014 CHARLESTON, SOUTH CAROLINA", MONO(21), 7,  BLUSH),
]
for y, line, fnt, tr, col in rows:
    wpt = tracked_width(d, line, fnt, tr)
    assert wpt <= 1088, "header line %r renders %dpx > 1088 (shorten line, keep tracking>=4)" % (line, wpt)
    center(d, y, line, fnt, col, tr)

h1 = F(92, bold=True)
w1 = tracked_width(d, "Deanna\u2019s Wine Bar", h1, 0)
assert w1 <= 1120, "h1 renders %dpx" % w1
center(d, 172, "Deanna\u2019s Wine Bar", h1, CREAM, 0)

sub = F(48, italic=True)
center(d, 296, "and Bert\u2019s Pig Shop", sub, BLUSH, 1)

d.rectangle((W // 2 - 120, 380, W // 2 + 120, 381), fill=WINE, )
d.rectangle((W // 2 - 120, 384, W // 2 + 120, 385), fill=BLUSH)

l1 = F(30, bold=True)
line1 = "CHARCUTERIE RENDERED ON SITE \u00b7 FRESH PORK"
w = tracked_width(d, line1, MONO(23), 6)
assert w <= 1100, "line1 renders %dpx" % w
center(d, 414, line1, MONO(23), CREAM, 6)

line2 = "SMALL-PRODUCER WINES AT NEIGHBORHOOD PRICES"
w = tracked_width(d, line2, MONO(23), 6)
assert w <= 1100, "line2 renders %dpx" % w
center(d, 452, line2, MONO(23), BLUSH, 6)

foot1 = "OPENING LATE 2026"
w = tracked_width(d, foot1, MONO(24), 10)
assert w <= 1100, "foot1 renders %dpx" % w
center(d, 520, foot1, MONO(24), BLUSH, 10)

foot2 = "521 WAPPOO ROAD \u00b7 CHARLESTON SC"
w = tracked_width(d, foot2, MONO(21), 6)
assert w <= 1100, "foot2 renders %dpx" % w
center(d, 556, foot2, MONO(21), (173, 138, 133), 6)

img.save(OUT, "PNG")
print("wrote %s %s 1200x630 og: image done" % (OUT, os.path.getsize(OUT)))
