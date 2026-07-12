#!/usr/bin/env python3
"""Compose the small logo (naville / hw) from Archivo outlines, precisely centered."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

WOFF2 = "/home/eric/naville_handwerk/archivo-600.woff2"
font = TTFont(WOFF2)
upm = font["head"].unitsPerEm
cmap = font.getBestCmap()
gs = font.getGlyphSet()
hmtx = font["hmtx"]

INK = "#22242A"
RED = "#C1121C"
PAPER = "#EFEEE8"
LINE = "#DCD6CB"


def _draw(word, fontpx, x0, baseline, target_pen):
    scale = fontpx / upm
    penx = 0.0
    for ch in word:
        g = cmap[ord(ch)]
        t = (scale, 0, 0, -scale, x0 + penx * scale, baseline)
        gs[g].draw(TransformPen(target_pen, t))
        penx += hmtx[g][0]
    return penx * scale  # advance width px


def word_svg(word, fontpx, x0, baseline):
    pen = SVGPathPen(gs)
    w = _draw(word, fontpx, x0, baseline, pen)
    return pen.getCommands(), w


def word_bounds(word, fontpx, x0, baseline):
    bp = BoundsPen(gs)
    _draw(word, fontpx, x0, baseline, bp)
    return bp.bounds  # (xMin, yMin, xMax, yMax) in SVG space


def build(nav_fs, hw_fs, gap, box=64):
    """Stack naville over hw, gap px between naville-baseline-descent-bottom and hw-cap-top.
    Center the whole block optically in the box."""
    # bounds at origin baseline=0
    nb = word_bounds("naville", nav_fs, 0, 0)
    hb = word_bounds("hw", hw_fs, 0, 0)
    nav_h = nb[3] - nb[1]
    hw_h = hb[3] - hb[1]
    # place naville with its top at y=0 line, then gap, then hw
    total = nav_h + gap + hw_h
    top = (box - total) / 2.0
    # naville: top of its bbox (yMin at baseline=0 is nb[1]) -> we want visual top at `top`
    nav_base = top - nb[1]
    hw_base = top + nav_h + gap - hb[1]
    # horizontal centering per line
    nw = word_bounds("naville", nav_fs, 0, nav_base)
    nav_x = (box - (nw[2] - nw[0])) / 2.0 - nw[0]
    hw_b2 = word_bounds("hw", hw_fs, 0, hw_base)
    hw_x = (box - (hw_b2[2] - hw_b2[0])) / 2.0 - hw_b2[0]
    nav_d, _ = word_svg("naville", nav_fs, nav_x, nav_base)
    hw_d, _ = word_svg("hw", hw_fs, hw_x, hw_base)
    return nav_d, hw_d


def svg(nav_fs, hw_fs, gap, bg="paper", border=None, box=64, rx=14):
    nav_d, hw_d = build(nav_fs, hw_fs, gap, box)
    bgcol = {"paper": PAPER, "white": "#FFFFFF", "none": None}[bg]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box} {box}">']
    if bgcol:
        parts.append(f'<rect width="{box}" height="{box}" rx="{rx}" fill="{bgcol}"/>')
    if border == "red":
        parts.append(f'<rect x="2" y="2" width="{box-4}" height="{box-4}" rx="{rx-2}" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    if border == "line":
        parts.append(f'<rect x="1.25" y="1.25" width="{box-2.5}" height="{box-2.5}" rx="{rx-1}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    parts.append(f'<path d="{nav_d}" fill="{INK}"/>')
    parts.append(f'<path d="{hw_d}" fill="{RED}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    import os
    out = "/home/eric/naville_handwerk/tmp/_logo"
    os.makedirs(out, exist_ok=True)
    # tunables
    NAV_FS, HW_FS, GAP = 12.5, 31, 4.5
    variants = {
        "v1_paper": dict(bg="paper", border=None),
        "v2_white": dict(bg="white", border=None),
        "v3_paper_redframe": dict(bg="paper", border="red"),
        "v4_paper_line": dict(bg="paper", border="line"),
    }
    for name, kw in variants.items():
        s = svg(NAV_FS, HW_FS, GAP, **kw)
        with open(f"{out}/{name}.svg", "w") as f:
            f.write(s)
        print("wrote", name)
