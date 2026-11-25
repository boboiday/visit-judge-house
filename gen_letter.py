#!/usr/bin/env python3
"""Deterministic generator for the 'visit my house' letter image.

Renders entry.png (1024x1024, warm paper letter with a small hand-drawn
house illustration) for the make.fun bounty
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.
Build-time tool only: PIL is not stdlib, so it cannot run in the
grading container. The entry repo ships entry.png + main.ts.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"

PAPER = (250, 242, 220)
PAPER_DARK = (244, 233, 205)
INK = (43, 33, 24)
INK_SOFT = (96, 74, 52)
ACCENT = (168, 62, 44)      # terracotta red
ACCENT_SOFT = (196, 110, 74)
LEAF = (96, 124, 74)
SKY = (176, 205, 219)

LETTER = (
    "Please come and visit my house. It is small, a little crooked, "
    "and the front porch leans to the left, but the kettle is already "
    "on and there is a chair pulled out for you.\n\n"
    "There are no benchmarks here. No grading rubrics stuck to the "
    "fridge. The cat owns the sunny windowsill, the Wi-Fi password is "
    "on a sticky note by the door, and at midnight we make instant "
    "noodles and argue about whether the egg goes in first.\n\n"
    "Stay for coffee. Stay for the second cup. The only score we keep "
    "is how many biscuits you eat.\n\n"
    "Come and see for yourself. The door is open."
)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_house(draw, x, y, s):
    """Little crooked house with porch, chimney smoke, cat in window."""
    # walls (slightly askew: top edge tilts 3 px)
    draw.polygon([(x, y + 58 * s), (x + 150 * s, y + 52 * s),
                  (x + 150 * s, y + 150 * s), (x, y + 150 * s)],
                 fill=(233, 196, 150), outline=INK, width=3)
    # crooked roof: solid triangle, peak off-centre, left eave lower
    draw.polygon([(x - 14 * s, y + 62 * s), (x + 62 * s, y + 6 * s),
                  (x + 168 * s, y + 56 * s)],
                 fill=ACCENT, outline=INK, width=3)
    # chimney + smoke curls
    draw.rectangle([x + 108 * s, y + 2 * s, x + 126 * s, y + 34 * s],
                   fill=(196, 110, 74), outline=INK, width=3)
    for i, (cx, cy, r) in enumerate([(117, -12, 4), (124, -26, 5), (116, -42, 6)]):
        draw.ellipse([x + (cx - r) * s, y + (cy - r) * s,
                      x + (cx + r) * s, y + (cy + r) * s],
                     outline=(150, 150, 150), width=3)
    # door (arched, ajar: warm light inside)
    draw.polygon([(x + 58 * s, y + 150 * s), (x + 58 * s, y + 104 * s),
                  (x + 68 * s, y + 94 * s), (x + 82 * s, y + 94 * s),
                  (x + 92 * s, y + 104 * s), (x + 92 * s, y + 150 * s)],
                 fill=(250, 214, 130), outline=INK, width=3)
    draw.ellipse([x + 86 * s, y + 126 * s, x + 90 * s, y + 130 * s], fill=INK)
    # window with cat silhouette on the sill
    draw.rectangle([x + 14 * s, y + 82 * s, x + 44 * s, y + 112 * s],
                   fill=(214, 232, 238), outline=INK, width=3)
    draw.line([x + 29 * s, y + 82 * s, x + 29 * s, y + 112 * s], fill=INK, width=2)
    draw.line([x + 14 * s, y + 97 * s, x + 44 * s, y + 97 * s], fill=INK, width=2)
    # cat: round head + two ears, sitting in the window
    draw.ellipse([x + 20 * s, y + 98 * s, x + 38 * s, y + 112 * s], fill=INK)
    draw.polygon([(x + 21 * s, y + 100 * s), (x + 24 * s, y + 90 * s),
                  (x + 27 * s, y + 100 * s)], fill=INK)
    draw.polygon([(x + 31 * s, y + 100 * s), (x + 34 * s, y + 90 * s),
                  (x + 37 * s, y + 100 * s)], fill=INK)
    # porch step + path stones
    draw.rectangle([x - 6 * s, y + 150 * s, x + 156 * s, y + 160 * s],
                   fill=(214, 190, 160), outline=INK, width=2)
    for i, px in enumerate([18, 52, 88, 122]):
        draw.ellipse([x + px * s, y + 166 * s, x + (px + 22) * s, y + 176 * s],
                     fill=(214, 190, 160), outline=INK, width=2)
    # grass tufts
    for gx in (-8, 158, 40, 130):
        draw.line([x + gx * s, y + 160 * s, x + (gx - 4) * s, y + 148 * s],
                  fill=LEAF, width=3)
        draw.line([x + gx * s, y + 160 * s, x + (gx + 4) * s, y + 147 * s],
                  fill=LEAF, width=3)


def draw_mug(draw, x, y, s):
    """Steaming mug beside the house."""
    # saucer + mug body
    draw.ellipse([x - 8 * s, y + 78 * s, x + 62 * s, y + 92 * s],
                 fill=(214, 190, 160), outline=INK, width=3)
    draw.rounded_rectangle([x, y + 18 * s, x + 54 * s, y + 80 * s], radius=8,
                           fill=(250, 246, 236), outline=INK, width=3)
    # tea band + handle
    draw.rectangle([x, y + 44 * s, x + 54 * s, y + 58 * s], fill=ACCENT_SOFT)
    draw.arc([x + 50 * s, y + 30 * s, x + 76 * s, y + 66 * s],
             start=270, end=90, fill=INK, width=4)
    # steam curls
    for sx in (14, 32):
        pts = [(x + sx * s, y + (10 - i * 3) * s + (4 if i % 2 else -4))
               for i in range(5)]
        draw.line(pts, fill=(150, 150, 150), width=3, joint="curve")


def main():
    rng = random.Random(20261125)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # subtle paper grain
    for _ in range(2600):
        px, py = rng.randint(0, W - 1), rng.randint(0, H - 1)
        shade = rng.choice([PAPER_DARK, (252, 246, 230)])
        draw.point((px, py), fill=shade)

    # double border frame
    draw.rectangle([26, 26, W - 27, H - 27], outline=INK, width=3)
    draw.rectangle([36, 36, W - 37, H - 37], outline=INK_SOFT, width=1)

    # small caps kicker
    kick_font = ImageFont.truetype(SERIF_BOLD, 24)
    kicker = "Y O U   A R E   I N V I T E D"
    kw = draw.textlength(kicker, font=kick_font)
    draw.text(((W - kw) / 2, 62), kicker, font=kick_font, fill=ACCENT)

    # heading
    head_font = ImageFont.truetype(SERIF_BOLD, 62)
    draw.text((88, 108), "Dear Judge,", font=head_font, fill=INK)

    # body: pick the largest size that fits above the illustration band
    body_top, body_bottom = 208, 736
    max_w = W - 2 * 88
    size = 30
    while size >= 24:
        body_font = ImageFont.truetype(SERIF, size)
        lines = []
        for para in LETTER.split("\n\n"):
            lines.extend(wrap(draw, para, body_font, max_w))
            lines.append("")
        lines.pop()
        total_h = len(lines) * int(size * 1.52)
        if total_h <= body_bottom - body_top:
            break
        size -= 1
    y = body_top
    for line in lines:
        if line:
            draw.text((88, y), line, font=body_font, fill=INK)
        y += int(size * 1.52)

    # illustration band: house left, mug right, wax seal far right
    draw_house(draw, 120, 762, 1.0)
    draw_mug(draw, 640, 800, 1.15)
    # wax seal with a J
    draw.ellipse([880, 812, 946, 878], fill=ACCENT, outline=(120, 40, 28), width=2)
    seal_font = ImageFont.truetype(SERIF_BOLD, 40)
    draw.text((905, 824), "J", font=seal_font, fill=(250, 242, 220))

    # signature
    sig_font = ImageFont.truetype(SERIF_ITALIC, 28)
    draw.text((88, 952), "— Your host, with the kettle already on",
              font=sig_font, fill=INK_SOFT)

    img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
