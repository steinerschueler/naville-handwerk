from PIL import Image, ImageDraw, ImageFilter
import numpy as np, sys
OUT="/home/eric/naville_handwerk/tmp/_render"
ROT=(193,18,28); ANTH=(35,37,43); BLACK=(0,0,0); CREME=(250,246,239); WHITE=(255,255,255)

def emblem(bikep,bedp,wheelp,drawcol,bg,trshift=0,wshift=0,shadow=True,shadowcol=ANTH,wheeldisc=False,disccol=(255,255,255),return_plate=False,presign=True,trdy=0):
    # bg: (r,g,b) tuple oder "trans". trshift: Bett+Deichsel nach rechts (final px), Schild fix. wshift: Rad nach LINKS.
    ss=2; W,H=1500,700; W2,H2=W*ss,H*ss; G=560*ss
    def s(v): return int(v*ss)
    dtr=-trshift*ss
    bike=Image.open(OUT+"/"+bikep).convert("RGBA"); bed=Image.open(OUT+"/"+bedp).convert("RGBA"); wheel=Image.open(OUT+"/"+wheelp).convert("RGBA")
    sign=Image.open(OUT+"/sign.png").convert("RGBA")
    bike_x=s(760); bike_y=s(237); tr_x0=s(240); tr_x=tr_x0+dtr; tr_y=s(406)+trdy*ss
    Sn=1360/1400; Str=bed.width/1400
    axle=(bike_x+int(327*Sn), bike_y+int(524*Sn)); stand_x=bike_x+int(540*Sn)
    twx=tr_x+(bed.width-int((600-(-160))*Str))+wshift*ss; twy=tr_y+int((250-60)*Str)
    fw_x=bike_x+int(1127*Sn); rw_x=bike_x+int(327*Sn)
    c=Image.new("RGBA",(W2,H2),((0,0,0,0) if bg=="trans" else bg+(255,)))
    if shadow and bg!="trans":
        sh=Image.new("RGBA",(W2,H2),(0,0,0,0)); sd=ImageDraw.Draw(sh)
        def contact(cx,w,al): sd.ellipse((cx-w,G-s(10),cx+w,G+s(16)),fill=shadowcol+(al,))
        for cx in (fw_x,rw_x,twx): contact(cx,s(120),55)
        contact(stand_x,s(72),45)
        sh=sh.filter(ImageFilter.GaussianBlur(s(9))); c.alpha_composite(sh)
    d=ImageDraw.Draw(c)
    piv=(stand_x+s(8),G-s(70))
    gb=G+s(7)  # Boden = Rad-Unterkante: Pad-Unterkante final y=571, damit beide Ständerfuesse exakt aufstehen
    for foot in (stand_x-s(24),stand_x+s(30)):
        d.line([piv,(foot,gb)],fill=drawcol,width=s(13)); d.line([(foot-s(13),gb),(foot+s(13),gb)],fill=drawcol,width=s(8))
    c.alpha_composite(bed,(tr_x,tr_y))
    rail_y=tr_y+int((196-60)/380*bed.height)
    P1=(tr_x+int((1400-(120-(-160)))*Str)-s(6), rail_y); P2=(P1[0]-s(66),rail_y); Q=(P1[0]+s(42),rail_y+s(9))
    d.line([axle,Q],fill=drawcol,width=s(12)); d.line([Q,P1],fill=drawcol,width=s(11)); d.line([Q,P2],fill=drawcol,width=s(11))
    for P in (P1,P2): d.line([(P[0]-s(12),P[1]),(P[0]+s(12),P[1])],fill=drawcol,width=s(10))
    d.ellipse([Q[0]-s(7),Q[1]-s(7),Q[0]+s(7),Q[1]+s(7)],fill=drawcol); d.ellipse([axle[0]-s(11),axle[1]-s(11),axle[0]+s(11),axle[1]+s(11)],fill=drawcol)
    sx=tr_x0
    bed_l=sx+int((1400-(1150-(-160)))*Str); bed_r=sx+int((1400-(120-(-160)))*Str); bed_w=bed_r-bed_l
    bed_top=tr_y+int((150-60)/380*bed.height)
    sw=int(bed_w*0.99); shh=int(sw/1.94); sign2=sign.resize((sw,shh)); sign_x=bed_l+(bed_w-sw)//2; sign_y=bed_top-shh+s(4)
    if presign: c.alpha_composite(sign2,(sign_x,sign_y))
    c.alpha_composite(wheel,(twx-wheel.width//2, twy-wheel.height//2))
    c.alpha_composite(bike,(bike_x,bike_y))
    c=c.transpose(Image.FLIP_LEFT_RIGHT)
    msign_x=W2-(sign_x+sw); c.alpha_composite(sign2,(msign_x,sign_y))
    mtw_x=W2-twx
    if wheeldisc:
        rr=s(58); ImageDraw.Draw(c).ellipse([mtw_x-rr,twy-rr,mtw_x+rr,twy+rr],fill=disccol+(255,))
    c.alpha_composite(wheel,(mtw_x-wheel.width//2, twy-wheel.height//2))
    if return_plate:
        # Maske der roten Platte an finaler (gespiegelter) Position, 2x-Aufloesung.
        # Alpha von sign2 = volle gekappte Platte (TR/BL 45-Grad gekappt, TL/BR rechtwinklig).
        M2=Image.new("L",(W2,H2),0); M2.paste(sign2.split()[3],(msign_x,sign_y))
        # Platzierung (2x-Koord) fuer die Rekonstruktion der Schild-Geometrie (sign.html-Polygone):
        geom={"sw":sw,"shh":shh,"msign_x":msign_x,"sign_y":sign_y}
        return c.resize((W,H), Image.LANCZOS), M2, geom
    return c.resize((W,H), Image.LANCZOS)

def white_base(trshift=0,wshift=0):
    we=emblem("bike2x_w.png","bed2x_w.png","wheel2x_w.png",WHITE,"trans",trshift,wshift,shadow=False)  # weisses Emblem, transparent
    a=np.array(we)[:,:,3]
    dil=np.array(Image.fromarray(a).filter(ImageFilter.MaxFilter(17)))
    rim=np.clip(dil.astype(int)-a.astype(int),0,255).astype(np.uint8)
    rimimg=np.zeros((we.height,we.width,4),np.uint8); rimimg[:,:,0:3]=255; rimimg[:,:,3]=rim
    b=Image.new("RGBA",we.size,ROT+(255,)); b.alpha_composite(Image.fromarray(rimimg)); b.alpha_composite(we)
    return b.convert("RGB")

if __name__=="__main__":
    # Validierung: weisse Basis bei ALTER Geometrie vs. aktuelles emblem-weiss-auf-rot
    wb=white_base(0,0); wb.save(OUT+"/_wb_old.png")
    cur=np.array(Image.open("/home/eric/naville_handwerk/tmp/emblem-weiss-auf-rot.png").convert("RGB")).astype(int)
    arr=np.array(wb).astype(int); diff=np.abs(arr-cur).sum(2)
    print("weisse Basis alt vs. aktuell:  %.2f%% Pixel >30 abweichend, mean %.2f"%((diff>30).mean()*100, diff.mean()))

def white_base2(trshift=0,wshift=0,maxf=19,outer=True):
    from PIL import ImageDraw as DD
    we=emblem("bike2x_w.png","bed2x_w.png","wheel2x_w.png",WHITE,"trans",trshift,wshift,shadow=False)
    a=np.array(we)[:,:,3]
    dil=np.array(Image.fromarray(a).filter(ImageFilter.MaxFilter(maxf)))
    rim=np.clip(dil.astype(int)-a.astype(int),0,255).astype(np.uint8)
    rimimg=np.zeros((we.height,we.width,4),np.uint8); rimimg[:,:,0:3]=255; rimimg[:,:,3]=rim
    b=Image.new("RGBA",we.size,ROT+(255,)); b.alpha_composite(Image.fromarray(rimimg)); b.alpha_composite(we)
    if outer:
        d=DD.Draw(b)
        # Aussen-Rechteck ums Schild (Schild fix an alter Position) — gemessene Geometrie
        d.rectangle([740,200,1232,214],fill=(255,255,255))   # oben
        d.rectangle([740,200,754,466],fill=(255,255,255))     # links
        d.rectangle([1218,200,1232,466],fill=(255,255,255))   # rechts
    return b.convert("RGB")

def schwarzrot_auf_rot(trshift=90,wshift=46,maxf=19,outer=True):
    wb=white_base2(trshift,wshift,maxf,outer).convert("RGBA")
    ov=emblem("bike2x_blk.png","bed2x_blk.png","wheel2x_blk.png",BLACK,"trans",trshift,wshift,shadow=False)
    wb.alpha_composite(ov); return wb.convert("RGB")
