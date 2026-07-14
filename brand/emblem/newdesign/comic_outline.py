#!/usr/bin/env python3
# Comic-Umriss v2: aeusserer Silhouetten-Umriss (Loecher/Speichen NICHT gefuellt-dilatiert)
# + schwarze Kontur nur um die ROTEN Flaechen. Raeder bleiben scharf.
import sys
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

src=sys.argv[1]; dst=sys.argv[2]
outer=int(sys.argv[3]) if len(sys.argv)>3 else 9   # Silhouetten-Strich
redln=int(sys.argv[4]) if len(sys.argv)>4 else 9   # Rot-Strich

im=Image.open(src).convert("RGBA"); a=np.array(im)
rgb=a[:,:,:3].astype(int); al=a[:,:,3]
ink = al>110
red = (rgb[:,:,0]>100)&(rgb[:,:,1]<95)&(rgb[:,:,2]<95)&ink

def dil(mask, s):
    return np.array(Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(s)))>128

# Loecher fuellen: Hintergrund von der Ecke fluten -> "aussen"; nicht erreichter Hintergrund = Loecher
bg=Image.fromarray(((~ink)*255).astype(np.uint8))
ImageDraw.floodfill(bg,(0,0),128)
outside=np.array(bg)==128
filled = ink | ((~ink) & (~outside))   # Silhouette mit gefuellten Loechern (Speichen etc.)

outer_ring = dil(filled, outer) & (~filled)     # nur aussen um die Silhouette
red_ring   = dil(red, redln) & (~ink)           # um Rot herum, in Hintergrund/Zwischenraeume
ring = outer_ring | red_ring

res=a.copy(); res[ring]=[0,0,0,255]
out=Image.fromarray(res,"RGBA")
a2=np.array(out); ys,xs=np.where(a2[:,:,3]>8)
out.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).save(dst)
print(f"outer={outer} red={redln} -> {dst}", Image.open(dst).size)
