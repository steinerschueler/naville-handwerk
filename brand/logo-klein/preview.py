#!/usr/bin/env python3
"""Homescreen reality check: apply iOS squircle + Android circle masks, check safe zone."""
from PIL import Image, ImageDraw
import math

bleed = Image.open("tmp/_logo/final_bleed_512.png").convert("RGBA")
S = bleed.width

def circle_mask(img):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse([0, 0, S-1, S-1], fill=255)
    out = img.copy(); out.putalpha(m); return out

def squircle_mask(img, n=5.0):
    m = Image.new("L", (S, S), 0); px = m.load()
    a = S/2.0
    for y in range(S):
        for x in range(S):
            u = (x-a+0.5)/a; v = (y-a+0.5)/a
            if abs(u)**n + abs(v)**n <= 1.0: px[x, y] = 255
    out = img.copy(); out.putalpha(m); return out

circ = circle_mask(bleed)
squ = squircle_mask(bleed)

# safe-zone overlay: 80%-diameter circle on the unmasked bleed
safe = bleed.copy(); d = ImageDraw.Draw(safe)
r = 0.4*S
d.ellipse([S/2-r, S/2-r, S/2+r, S/2+r], outline=(0,120,255,255), width=3)

# compose a preview on a "wallpaper" gradient
def wallpaper(w, h):
    bg = Image.new("RGB", (w, h))
    for y in range(h):
        t = y/h
        bg.paste((int(60+40*t), int(70+50*t), int(90+60*t)), [0, y, w, y+1])
    return bg

tiles = [("randlos (unmaskiert)", bleed), ("iOS Squircle", squ),
         ("Android Kreis", circ), ("Safe-Zone 80%", safe)]
disp = 150
pad = 26; label_h = 30
W = len(tiles)*disp + (len(tiles)+1)*pad
H = disp + 2*pad + label_h
canvas = wallpaper(W, H).convert("RGBA")
d = ImageDraw.Draw(canvas)
x = pad
for name, im in tiles:
    t = im.resize((disp, disp), Image.LANCZOS)
    canvas.alpha_composite(t, (x, pad))
    d.text((x+6, pad+disp+8), name, fill=(255,255,255,255))
    x += disp + pad
canvas.convert("RGB").save("tmp/_logo/_homescreen_preview.png")
print("saved homescreen preview", canvas.size)
