#!/usr/bin/env python3
"""Generate LCLC brand marks as outlined SVG (no font needed, safe for print/merch).
  python3 tools/make_logo.py
Outputs assets/img/lclc-badge.svg, lclc-wordmark.svg, lclc-mark.svg."""
import math, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"
ANTON = TTFont(ROOT / "assets/fonts/anton.woff2")
GS = ANTON.getGlyphSet(); CMAP = ANTON.getBestCmap(); UPM = ANTON["head"].unitsPerEm
HM = ANTON["hmtx"]
CAP = ANTON["OS/2"].sCapHeight if hasattr(ANTON["OS/2"], "sCapHeight") and ANTON["OS/2"].sCapHeight else int(UPM * .72)
YEL, GRN, INK, PINK = "#ffd60a", "#7cff3a", "#05010c", "#ff2bd6"

def adv(ch, size, track=0): return HM[CMAP[ord(ch)]][0] * size / UPM + track
def width(s, size, track=0): return sum(adv(c, size, track) for c in s) - track

def glyph(ch, size, x, y, rot=0, cx=0, cy=0):
    """path d for one glyph, baseline at (x,y), optional rotation (deg) about (cx,cy)."""
    pen = SVGPathPen(GS); s = size / UPM
    a = math.radians(rot); ca, sa = math.cos(a), math.sin(a)
    # glyph -> scale/flip -> translate -> rotate about (cx,cy)
    # point p' = R*( (x + s*gx, y - s*gy) - c ) + c
    xx, xy = ca * s, sa * s
    yx, yy = sa * s, -ca * s  # because of y flip: (gx,gy)->(s*gx, -s*gy), then rotate
    tx = ca * (x - cx) - sa * (y - cy) + cx
    ty = sa * (x - cx) + ca * (y - cy) + cy
    # matrix (a,b,c,d,e,f): x' = a*gx + c*gy + e ; y' = b*gx + d*gy + f
    m = (ca * s, sa * s, sa * s, -ca * s, tx, ty)
    GS[CMAP[ord(ch)]].draw(TransformPen(pen, m))
    return pen.getCommands()

def line(s, size, x, y, track=0, anchor="middle"):
    w = width(s, size, track)
    x0 = x - w / 2 if anchor == "middle" else x
    out = []
    for c in s:
        if c != " ": out.append(glyph(c, size, x0, y))
        x0 += adv(c, size, track)
    return " ".join(out), w

def arc(s, size, cx, cy, r, center_deg, track=0, bottom=False):
    """text along a circle; center_deg measured clockwise from 12 o'clock."""
    total = width(s, size, track); out = []
    # angle per unit length
    k = 360 / (2 * math.pi * r)
    if not bottom:
        a = center_deg - total * k / 2
        for c in s:
            w = adv(c, size, track); mid = a + (w - track) * k / 2
            if c != " ":
                rad = math.radians(mid)
                px, py = cx + r * math.sin(rad), cy - r * math.cos(rad)
                out.append(glyph(c, size, px - (w - track) / 2, py, rot=mid, cx=px, cy=py))
            a += w * k
    else:  # bottom arc, reads left-to-right, glyphs upright-ish
        a = center_deg + total * k / 2
        for c in s:
            w = adv(c, size, track); mid = a - (w - track) * k / 2
            if c != " ":
                rad = math.radians(mid)
                rr = r + CAP * size / UPM  # baseline outside so caps sit inside the ring
                px, py = cx + rr * math.sin(rad), cy - rr * math.cos(rad)
                out.append(glyph(c, size, px - (w - track) / 2, py, rot=mid - 180, cx=px, cy=py))
            a -= w * k
    return " ".join(out)

def star(cx, cy, r, ir=None, n=5, rot=-90):
    ir = ir or r * .45; pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else ir; a = math.radians(rot + i * 180 / n)
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return "M" + " L".join(pts) + "Z"

# ---- badge (1000x1000) ----
C = 500
lc, lw = line("LCLC", 215, C, C + CAP * 215 / UPM / 2, track=5)
top = arc("LOW COST LEGENDS CLUB", 74, C, C, 375, 0, track=4)
bot = arc("BY SMOKEROACH", 64, C, C, 352, 180, track=6, bottom=True)
s1, s2 = star(C - 418 + 40, C, 22), star(C + 418 - 40, C, 22)
badge = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000" role="img" aria-labelledby="t">
<title id="t">Low Cost Legends Club (LCLC) by SmokeRoach</title>
<circle cx="500" cy="500" r="490" fill="{INK}"/>
<circle cx="500" cy="500" r="470" fill="none" stroke="{YEL}" stroke-width="14"/>
<circle cx="500" cy="500" r="290" fill="none" stroke="{GRN}" stroke-width="8"/>
<path fill="{YEL}" d="{top}"/>
<path fill="{GRN}" d="{bot}"/>
<path fill="{PINK}" d="{s1} {s2}"/>
<path fill="#ffffff" d="{lc}"/>
<rect x="{C - lw/2:.1f}" y="{C + CAP*215/UPM/2 + 20:.1f}" width="{lw:.1f}" height="12" rx="6" fill="{YEL}"/>
</svg>
'''
(IMG / "lclc-badge.svg").write_text(badge)

# ---- compact mark for header/avatar (square, just LCLC in a roundel) ----
lc2, lw2 = line("LCLC", 150, 200, 200 + CAP * 150 / UPM / 2, track=3)
mark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400" role="img" aria-label="LCLC">
<circle cx="200" cy="200" r="196" fill="{INK}"/><circle cx="200" cy="200" r="182" fill="none" stroke="{YEL}" stroke-width="16"/>
<path fill="#ffffff" d="{lc2}"/><rect x="{200 - lw2/2:.1f}" y="{200 + CAP*150/UPM/2 + 14:.1f}" width="{lw2:.1f}" height="10" rx="5" fill="{GRN}"/>
</svg>
'''
(IMG / "lclc-mark.svg").write_text(mark)

# ---- horizontal wordmark ----
t1, w1 = line("LOW COST LEGENDS CLUB", 120, 0, 120, track=3, anchor="start")
t2, w2 = line("BY SMOKEROACH", 52, 0, 200, track=10, anchor="start")
W = max(w1, w2) + 40
word = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -10 {W:.0f} 230" width="{W:.0f}" height="230" role="img" aria-label="Low Cost Legends Club by SmokeRoach">
<path fill="{YEL}" d="{t1}"/><path fill="{GRN}" d="{t2}"/>
</svg>
'''
(IMG / "lclc-wordmark.svg").write_text(word)
print("wrote lclc-badge.svg, lclc-mark.svg, lclc-wordmark.svg")
