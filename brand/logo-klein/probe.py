#!/usr/bin/env python3
"""Probe h stem geometry + key metrics in font units."""
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen

font = TTFont("/home/eric/naville_handwerk/archivo-600.woff2")
upm = font["head"].unitsPerEm
cmap = font.getBestCmap()
gs = font.getGlyphSet()
hmtx = font["hmtx"]

def bounds(ch):
    bp = BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp); return bp.bounds

for ch in "hwnavile":
    b = bounds(ch)
    print(f"{ch}: bbox={tuple(round(v) for v in b)} adv={hmtx[cmap[ord(ch)]][0]}")

# h contour points to find left stem
rp = RecordingPen(); gs[cmap[ord('h')]].draw(rp)
xs = set()
for cmd, args in rp.value:
    for pt in args:
        if isinstance(pt, tuple):
            xs.add(round(pt[0]))
print("\nh unique x (sorted):", sorted(xs))
# ascender top = yMax of h
print("h yMax (ascender top):", round(bounds('h')[3]))
print("x-height:", getattr(font['OS/2'],'sxHeight',None), "cap:", getattr(font['OS/2'],'sCapHeight',None))
