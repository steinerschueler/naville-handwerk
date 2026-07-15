#!/usr/bin/env python3
# Baut alle 6 Comic-Emblem-Fassungen fuer logo/.
#  - schwarzrot: schwarzes Werkzeugkasten-Schild + Comic-Umriss (schwarz).
#  - rot (einfarbig): rotes Werkzeugkasten-Schild (Creme-Details), KEIN schwarzer Umriss.
# Comic-Umriss wird auf der transparenten Fassung (Vollcanvas) berechnet und dann auf
# Creme/Rot gesetzt -> loest das "Alpha-Trick greift nur transparent"-Problem.
import importlib.util, sys, os, shutil
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

BASE="/home/eric/naville_handwerk/tmp"
spec=importlib.util.spec_from_file_location("g", BASE+"/_gen.py")
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
R=BASE+"/_render"

ROT=(193,18,28); BLACK=(0,0,0); CREME=(250,246,239); ANTH=(35,37,43)
GEO=dict(trshift=90, wshift=55, trdy=23, presign=False)  # trdy 12->23: laced-Rad 11px zu hoch -> ganzen Anhaenger runter
BLK=("bike2x_blk.png","bed2x_blk.png","wheel2x_blk.png")
RED=("bike2x_red.png","bed2x_red.png","wheel2x_red.png")

def use_sign(which):  # "blk" | "red"
    shutil.copy(R+"/sign_"+which+".png", R+"/sign.png")

def transparent(assets, drawcol):
    return g.emblem(*assets, drawcol, "trans", shadow=False, **GEO)          # 1500x700 RGBA

def on_creme(assets, drawcol, shadowcol):
    return g.emblem(*assets, drawcol, CREME, shadow=True, shadowcol=shadowcol,
                    wheeldisc=True, disccol=CREME, **GEO).convert("RGBA")     # 1500x700

def comic_outline_full(im, outer=9, redln=9):
    # wie comic_outline.py, aber OHNE Endbeschnitt (Vollcanvas, fuer Komposition)
    a=np.array(im.convert("RGBA")); rgb=a[:,:,:3].astype(int); al=a[:,:,3]
    ink = al>110
    red = (rgb[:,:,0]>100)&(rgb[:,:,1]<95)&(rgb[:,:,2]<95)&ink
    def dil(mask,s): return np.array(Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(s)))>128
    bg=Image.fromarray(((~ink)*255).astype(np.uint8)); ImageDraw.floodfill(bg,(0,0),128)
    outside=np.array(bg)==128
    filled = ink | ((~ink) & (~outside))
    outer_ring = dil(filled,outer) & (~filled)
    red_ring   = dil(red,redln) & (~ink)
    ring = outer_ring | red_ring
    res=a.copy(); res[ring]=[0,0,0,255]
    return Image.fromarray(res,"RGBA")

def trim(im):
    a=np.array(im); ys,xs=np.where(a[:,:,3]>8)
    return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))

def halo_on_red(emb_full, maxf=19):
    a=np.array(emb_full)[:,:,3]
    dil=np.array(Image.fromarray(a).filter(ImageFilter.MaxFilter(maxf)))
    rim=np.clip(dil.astype(int)-a.astype(int),0,255).astype(np.uint8)
    rimimg=np.zeros((emb_full.height,emb_full.width,4),np.uint8); rimimg[:,:,0:3]=255; rimimg[:,:,3]=rim
    b=Image.new("RGBA",emb_full.size,ROT+(255,)); b.alpha_composite(Image.fromarray(rimimg)); b.alpha_composite(emb_full)
    return b.convert("RGB")

L=sys.argv[1]; os.makedirs(L, exist_ok=True)

# ---------- SCHWARZROT (schwarzes Schild + Comic-Umriss) ----------
use_sign("blk")
blk_full = comic_outline_full(transparent(BLK, BLACK), 9, 9)      # 1500x700, ausgeumrisst
trim(blk_full).save(L+"/emblem-schwarzrot-transparent.png")
base = on_creme(BLK, BLACK, ANTH); base.alpha_composite(blk_full)
base.convert("RGB").save(L+"/emblem-schwarzrot-auf-creme.png")
halo_on_red(blk_full).save(L+"/emblem-schwarzrot-auf-rot.png")

# ---------- ROT einfarbig (rotes Schild, KEIN schwarzer Umriss) ----------
use_sign("red")
red_full = transparent(RED, ROT)                                  # 1500x700, kein Umriss
trim(red_full).save(L+"/emblem-rot-transparent.png")
on_creme(RED, ROT, ROT).convert("RGB").save(L+"/emblem-rot-auf-creme.png")
halo_on_red(red_full).save(L+"/emblem-rot-weiss-umrandet-auf-rot.png")

use_sign("blk")  # Standard zuruecksetzen
# full emblem (transparent, ausgeumrisst) auch fuer Lockups exportieren
trim(blk_full).save(L+"/_full_blk_outlined.png")
print("6 Emblem-PNGs + _full_blk_outlined ->", L)
