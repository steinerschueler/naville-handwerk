#!/usr/bin/env python3
"""Small logo v2: extended-h spine, 'naville' beside it top-right, letters stretched
vertically into a rectangular figure."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

font = TTFont("/home/eric/naville_handwerk/archivo-600.woff2")
upm = font["head"].unitsPerEm
cmap = font.getBestCmap()
gs = font.getGlyphSet()
hmtx = font["hmtx"]

INK, RED, PAPER, LINE = "#22242A", "#C1121C", "#EFEEE8", "#DCD6CB"
STEM_L, STEM_R, ASC = 65, 187, 723   # measured h stem + ascender top (font units)

def draw(word, sx, sy, x0_px, baseline_px, pen):
    """x0_px = px where font-x=0 lands; baseline_px = px of baseline. Returns advance px."""
    penx = 0.0
    for ch in word:
        g = cmap[ord(ch)]
        t = (sx, 0, 0, -sy, x0_px + penx * sx, baseline_px)
        gs[g].draw(TransformPen(pen, t))
        penx += hmtx[g][0]
    return penx * sx

def word_d(word, sx, sy, x0, base):
    pen = SVGPathPen(gs); draw(word, sx, sy, x0, base, pen); return pen.getCommands()

def word_bounds(word, sx, sy, x0, base):
    bp = BoundsPen(gs); draw(word, sx, sy, x0, base, bp); return bp.bounds

def build(k=1.35, HW=30, box=64, y_top=10, y_base=54, hx=None, gap=2.2,
          bg="paper", border="line"):
    sx = HW / upm
    sy = sx * k
    # anchor h so its glyph x=65 (stem left) lands at hx
    if hx is None:
        hx = 11.0
    x0_hw = hx - STEM_L * sx          # px where font-x=0 lands for hw
    # hw right edge & stem px
    hwb = word_bounds("hw", sx, sy, x0_hw, y_base)
    hw_right = hwb[2]
    stem_l_px = x0_hw + STEM_L * sx
    stem_r_px = x0_hw + STEM_R * sx
    # naville spans [stem_r_px+gap, hw_right]; pick its font-size from that width
    nav_left = stem_r_px + gap
    avail = hw_right - nav_left
    # natural naville width at sx=1px-em is 2.986*em ; solve nsx
    NAT = 2.9857  # width('naville')@1000upm /1000  (=298.57/100 per 100px earlier)
    nsx = avail / (NAT * upm) * upm    # = avail/ (2.9857*em... ) -> compute directly:
    nsx = avail / (2.9857 * upm) * upm  # placeholder; recompute cleanly below
    # width('naville') in px = penx_units * nsx ; penx_units('naville')=2985.7 (units)
    NAV_UNITS = 2985.7
    nsx = avail / NAV_UNITS
    nsy = nsx * k
    # naville baseline so its ascender-top (ASC) sits at y_top
    nav_base = y_top + ASC * nsy
    nav_x0 = nav_left - 65 * nsx      # font-x=0 anchor (n starts at x=65)
    # --- paths ---
    hw_d = word_d("hw", sx, sy, x0_hw, y_base)
    nav_d = word_d("naville", nsx, nsy, nav_x0, nav_base)
    # extended stem rect (red): from y_top down into existing stem (overlap past ASC top)
    stem_top_px = y_base - ASC * sy
    ext = f'<rect x="{stem_l_px:.2f}" y="{y_top:.2f}" width="{stem_r_px-stem_l_px:.2f}" height="{stem_top_px - y_top + 3:.2f}" fill="{RED}"/>'
    # --- assemble ---
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box} {box}">']
    if bg == "paper": p.append(f'<rect width="{box}" height="{box}" rx="14" fill="{PAPER}"/>')
    elif bg == "white": p.append(f'<rect width="{box}" height="{box}" rx="14" fill="#fff"/>')
    if border == "line": p.append(f'<rect x="1.25" y="1.25" width="{box-2.5}" height="{box-2.5}" rx="13" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    p.append(f'<path d="{hw_d}" fill="{RED}"/>')
    p.append(ext)
    p.append(f'<path d="{nav_d}" fill="{INK}"/>')
    p.append("</svg>")
    return "\n".join(p)

if __name__ == "__main__":
    out = "/home/eric/naville_handwerk/tmp/_logo"
    for name, kw in {
        "t10": dict(k=1.00, HW=33),
        "t12": dict(k=1.18, HW=32),
        "t13": dict(k=1.30, HW=32),
        "s16": dict(k=1.60, HW=31),
    }.items():
        open(f"{out}/{name}.svg", "w").write(build(**kw))
        print("wrote", name)
