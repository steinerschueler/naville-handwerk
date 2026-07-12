import sys
from PIL import Image, ImageFilter
import numpy as np
OUT="/home/eric/naville_handwerk/tmp/_render"
S=0.448; yoff=206; SIGN_H=int(sys.argv[1]) if len(sys.argv)>1 else 300
ROT=(193,18,28,255)
bike=Image.open("bike_t.png").convert("RGBA").transpose(Image.FLIP_LEFT_RIGHT)
trailer=Image.open("trailer_t.png").convert("RGBA")
sign=Image.open(OUT+"/sign.png").convert("RGBA")
sw=int(sign.width*SIGN_H/sign.height); sign=sign.resize((sw,SIGN_H))
W,Hc=1340,560
def build(bg):
    c=Image.new("RGBA",(W,Hc),bg); bx=40; c.alpha_composite(bike,(bx,yoff))
    cargo_right=bx+(bike.width-(120-80)*S)
    tleft=int(cargo_right-24); c.alpha_composite(trailer,(tleft,yoff))
    bed_top=yoff+int((372-20)*S); wheel_abs=tleft+int((820+120)*S)
    c.alpha_composite(sign,(wheel_abs-sw//2, bed_top-SIGN_H+6))
    return c
tr=build((0,0,0,0)); tr.save(OUT+"/emblem_trans.png")
build((250,246,239,255)).convert("RGB").save(OUT+"/emblem_creme.png")
a=np.array(tr)[:,:,3]
dil=np.array(Image.fromarray(a).filter(ImageFilter.MaxFilter(17)))
rim=np.clip(dil.astype(int)-a.astype(int),0,255).astype(np.uint8)
white=np.zeros((Hc,W,4),np.uint8); white[:,:,0:3]=255; white[:,:,3]=rim
b=Image.new("RGBA",(W,Hc),ROT); b.alpha_composite(Image.fromarray(white)); b.alpha_composite(tr)
b.convert("RGB").save(OUT+"/emblem_onred.png")
print("v5 ok (ohne Kiste/Gurt), sign_w",sw)
