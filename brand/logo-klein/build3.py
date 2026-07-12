#!/usr/bin/env python3
"""Small logo v3: naville on a normal line just above hw; h left stem extended up
to exactly naville's top (flush); compact; auto-fit + centered in tile."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

font = TTFont("/home/eric/naville_handwerk/archivo-600.woff2")
upm = font["head"].unitsPerEm
cmap = font.getBestCmap(); gs = font.getGlyphSet(); hmtx = font["hmtx"]
INK, RED, PAPER, LINE = "#22242A", "#C1121C", "#EFEEE8", "#DCD6CB"
STEM_L, STEM_R, ASC, XH = 65, 187, 723, 526
NAV_UNITS = 2985.7  # advance-width of 'naville' in font units

def _draw(word, sx, sy, x0, base, pen):
    penx = 0.0
    for ch in word:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (sx, 0, 0, -sy, x0 + penx * sx, base)))
        penx += hmtx[g][0]
    return penx * sx

def _d(word, sx, sy, x0, base):
    p = SVGPathPen(gs); _draw(word, sx, sy, x0, base, p); return p.getCommands()

def _b(word, sx, sy, x0, base):
    p = BoundsPen(gs); _draw(word, sx, sy, x0, base, p); return p.bounds

def build(k=1.15, HW=32, gap_h=2.2, gap_v=3.0, box=64, pad=8.0,
          bg="paper", border="line", rx=14, mode=None):
    if mode == "tile":
        pad, border, rx = 8.0, "line", 14
    elif mode == "bleed":
        pad, border, rx = 13.0, None, 0
    sx = HW / upm; sy = sx * k
    y_base = 100.0
    x0_hw = 0.0
    hwb = _b("hw", sx, sy, x0_hw, y_base)
    hw_right = hwb[2]
    stem_l = x0_hw + STEM_L * sx
    stem_r = x0_hw + STEM_R * sx
    h_top_nat = y_base - ASC * sy          # natural top of h stem
    xh_top = y_base - XH * sy               # x-height line (top of w / h-bowl)
    # naville: width-locked to hw right edge, sits gap_v above x-height line
    nav_left = stem_r + gap_h
    avail = hw_right - nav_left
    nsx = avail / NAV_UNITS; nsy = nsx * k
    nav_base = xh_top - gap_v
    nav_x0 = nav_left - STEM_L * nsx        # 'n' starts at x=65 like h
    nav_top = nav_base - ASC * nsy
    # spine extension: from nav_top down into the natural stem (overlap)
    spine_top = nav_top
    ext_h = (h_top_nat + 4) - spine_top
    # figure bbox
    fig_l, fig_r = stem_l, hw_right
    fig_t, fig_b = spine_top, y_base
    figW, figH = fig_r - fig_l, fig_b - fig_t
    avail_box = box - 2 * pad
    s = avail_box / max(figW, figH)
    tx = (box - figW * s) / 2 - fig_l * s
    ty = (box - figH * s) / 2 - fig_t * s
    # elements
    hw_d = _d("hw", sx, sy, x0_hw, y_base)
    nav_d = _d("naville", nsx, nsy, nav_x0, nav_base)
    ext = f'<rect x="{stem_l:.3f}" y="{spine_top:.3f}" width="{stem_r-stem_l:.3f}" height="{ext_h:.3f}" fill="{RED}"/>'
    g = (f'<g transform="translate({tx:.3f},{ty:.3f}) scale({s:.4f})">'
         f'<path d="{hw_d}" fill="{RED}"/>{ext}<path d="{nav_d}" fill="{INK}"/></g>')
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box} {box}">']
    if bg == "paper": out.append(f'<rect width="{box}" height="{box}" rx="{rx}" fill="{PAPER}"/>')
    elif bg == "white": out.append(f'<rect width="{box}" height="{box}" rx="{rx}" fill="#fff"/>')
    if border == "line": out.append(f'<rect x="1.25" y="1.25" width="{box-2.5}" height="{box-2.5}" rx="{rx-1}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    out.append(g); out.append("</svg>")
    return "\n".join(out)

if __name__ == "__main__":
    out = "/home/eric/naville_handwerk/tmp/_logo"
    # FINAL: k=1.15
    open(f"{out}/final_tile.svg", "w").write(build(k=1.15, mode="tile"))
    open(f"{out}/final_bleed.svg", "w").write(build(k=1.15, mode="bleed"))
    print("wrote final_tile, final_bleed")
