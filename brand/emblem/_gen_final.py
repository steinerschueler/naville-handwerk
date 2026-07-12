import importlib.util
from PIL import Image, ImageFilter
import numpy as np
spec=importlib.util.spec_from_file_location("g","/home/eric/naville_handwerk/tmp/_gen.py")
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
ROT=(193,18,28); BLACK=(0,0,0); CREME=(250,246,239); ANTH=(35,37,43)
GEO=dict(trshift=90,wshift=55,trdy=12,presign=False)
BLK=("bike2x_blk.png","bed2x_blk.png","wheel2x_blk.png")
RED=("bike2x_red.png","bed2x_red.png","wheel2x_red.png")

def on_creme(assets,drawcol,shadowcol):
    # Anhänger-Rad-Innenscheibe in Creme, damit obere Speichen nicht rot durch die Schild-Platte scheinen
    return g.emblem(*assets,drawcol,CREME,shadow=True,shadowcol=shadowcol,wheeldisc=True,disccol=CREME,**GEO).convert("RGB")

def transparent(assets,drawcol):
    return g.emblem(*assets,drawcol,"trans",shadow=False,**GEO)  # RGBA

def on_red_halo(assets,drawcol,maxf=19):
    em=g.emblem(*assets,drawcol,"trans",shadow=False,**GEO)
    a=np.array(em)[:,:,3]
    dil=np.array(Image.fromarray(a).filter(ImageFilter.MaxFilter(maxf)))
    rim=np.clip(dil.astype(int)-a.astype(int),0,255).astype(np.uint8)
    rimimg=np.zeros((em.height,em.width,4),np.uint8); rimimg[:,:,0:3]=255; rimimg[:,:,3]=rim
    b=Image.new("RGBA",em.size,ROT+(255,)); b.alpha_composite(Image.fromarray(rimimg)); b.alpha_composite(em)
    return b.convert("RGB")

L="/home/eric/naville_handwerk/logo"
# Creme
on_creme(BLK,BLACK,ANTH).save(L+"/emblem-schwarzrot-auf-creme.png")
on_creme(RED,ROT,ROT).save(L+"/emblem-rot-auf-creme.png")
# Rot, weiss umrandet
on_red_halo(BLK,BLACK).save(L+"/emblem-schwarzrot-auf-rot.png")
on_red_halo(RED,ROT).save(L+"/emblem-rot-weiss-umrandet-auf-rot.png")
# Transparent (beschnitten)
def save_trim(im,path):
    a=np.array(im); ys,xs=np.where(a[:,:,3]>8); im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).save(path)
save_trim(transparent(BLK,BLACK),L+"/emblem-schwarzrot-transparent.png")
save_trim(transparent(RED,ROT),L+"/emblem-rot-transparent.png")
print("6 Emblem-PNGs neu in logo/")
