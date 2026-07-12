#!/usr/bin/env python3
"""Extract Archivo-600 glyph outlines from the woff2 as SVG paths (no font dep)."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

WOFF2 = "/home/eric/naville_handwerk/archivo-600.woff2"

font = TTFont(WOFF2)
upm = font["head"].unitsPerEm
cmap = font.getBestCmap()
gs = font.getGlyphSet()
hmtx = font["hmtx"]
os2 = font["OS/2"]
print("unitsPerEm:", upm)
print("capHeight:", getattr(os2, "sCapHeight", None), "xHeight:", getattr(os2, "sxHeight", None))
print("ascender:", font["hhea"].ascent, "descender:", font["hhea"].descent)


def word_path(word, fontpx, x0, baseline, letterspacing=0.0):
    """Return (svg_d, width_px). Coords in SVG space (y-down), baseline at `baseline`."""
    scale = fontpx / upm
    penx_units = 0.0
    d_parts = []
    for ch in word:
        gname = cmap[ord(ch)]
        # transform: scale + flip-y, offset by current pen x and baseline
        xoff = x0 + penx_units * scale
        t = (scale, 0, 0, -scale, xoff, baseline)
        pen = SVGPathPen(gs)
        tpen = TransformPen(pen, t)
        gs[gname].draw(tpen)
        d_parts.append(pen.getCommands())
        penx_units += hmtx[gname][0] + letterspacing * upm / fontpx
    width_px = penx_units * scale
    return " ".join(p for p in d_parts if p), width_px


if __name__ == "__main__":
    # measure natural widths at fontpx=100 for planning
    for w in ("naville", "hw", "handwerk"):
        _, wpx = word_path(w, 100, 0, 0)
        print(f"width '{w}' @100px = {wpx:.1f}")
