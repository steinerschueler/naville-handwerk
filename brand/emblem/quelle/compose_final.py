import math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
OUT="/home/eric/naville_handwerk/tmp/_render"
ROT=(193,18,28); ANTH=(35,37,43); BLACK=(0,0,0); CREME=(250,246,239)

def build(bike_p,bed_p,wheel_p,linecol,bg,shadow,elements='all'):
    ss=2; W,H=1500,700; W2,H2=W*ss,H*ss; G=560*ss
    def s(v): return int(v*ss)
    bike=Image.open(bike_p).convert("RGBA"); bed=Image.open(bed_p).convert("RGBA"); wheel=Image.open(wheel_p).convert("RGBA")
    sign=Image.open(OUT+"/sign.png").convert("RGBA")
    bike_x=s(760); bike_y=s(237); tr_x=s(240); tr_y=s(406)
    Sn=1360/1400; Str=bed.width/1400
    axle=(bike_x+int(327*Sn), bike_y+int(524*Sn)); stand_x=bike_x+int(540*Sn)
    tw=(tr_x+(bed.width-int((600-(-160))*Str)), tr_y+int((250-60)*Str))
    fw_x=bike_x+int(1127*Sn); rw_x=bike_x+int(327*Sn)
    ALL = (elements=='all')
    c=Image.new("RGBA",(W2,H2),((0,0,0,0) if bg=="trans" else bg+(255,)))
    if shadow and ALL:
        sh=Image.new("RGBA",(W2,H2),(0,0,0,0)); sd=ImageDraw.Draw(sh)
        def contact(cx,w,al): sd.ellipse((cx-w,G-s(10),cx+w,G+s(16)),fill=ANTH+(al,))
        for cx in (fw_x,rw_x,tw[0]): contact(cx,s(120),55)
        contact(stand_x,s(72),45)
        sh=sh.filter(ImageFilter.GaussianBlur(s(9))); c.alpha_composite(sh)
    d=ImageDraw.Draw(c)
    if ALL:
        piv=(stand_x+s(8),G-s(70))
        for foot in (stand_x-s(24),stand_x+s(30)):
            d.line([piv,(foot,G-s(2))],fill=linecol,width=s(13))
            d.line([(foot-s(13),G-s(2)),(foot+s(13),G-s(2))],fill=linecol,width=s(8))
    c.alpha_composite(bed,(tr_x,tr_y))
    if ALL:
        rail_y=tr_y+int((196-60)/380*bed.height)
        P1=(tr_x+int((1400-(120-(-160)))*Str)-s(6), rail_y); P2=(P1[0]-s(66),rail_y); Q=(P1[0]+s(42),rail_y+s(9))
        d.line([axle,Q],fill=linecol,width=s(12)); d.line([Q,P1],fill=linecol,width=s(11)); d.line([Q,P2],fill=linecol,width=s(11))
        for P in (P1,P2): d.line([(P[0]-s(12),P[1]),(P[0]+s(12),P[1])],fill=linecol,width=s(10))
        d.ellipse([Q[0]-s(7),Q[1]-s(7),Q[0]+s(7),Q[1]+s(7)],fill=linecol)
        d.ellipse([axle[0]-s(11),axle[1]-s(11),axle[0]+s(11),axle[1]+s(11)],fill=linecol)
    bed_l=tr_x+int((1400-(1150-(-160)))*Str); bed_r=tr_x+int((1400-(120-(-160)))*Str); bed_w=bed_r-bed_l
    bed_top=tr_y+int((150-60)/380*bed.height)
    sw=int(bed_w*0.99); shh=int(sw/1.94); sign2=sign.resize((sw,shh))
    sign_x=bed_l+(bed_w-sw)//2; sign_y=bed_top-shh+s(4)
    c.alpha_composite(sign2,(sign_x,sign_y))
    c.alpha_composite(wheel,(tw[0]-wheel.width//2, tw[1]-wheel.height//2))
    if ALL: c.alpha_composite(bike,(bike_x,bike_y))
    # spiegeln + Schild/Rad lesbar
    c=c.transpose(Image.FLIP_LEFT_RIGHT)
    msign_x=W2-(sign_x+sw); c.alpha_composite(sign2,(msign_x,sign_y))
    mtw_x=W2-tw[0]; c.alpha_composite(wheel,(mtw_x-wheel.width//2, tw[1]-wheel.height//2))
    return c.resize((W,H), Image.LANCZOS)

if __name__=="__main__":
    build("bike2x.png","bed2x.png","wheel2x.png",ANTH,CREME,True).convert("RGB").save(OUT+"/emblem_ind.png")
    build("bike2x_red.png","bed2x_red.png","wheel2x_red.png",ROT,CREME,True).convert("RGB").save(OUT+"/emblem_red.png")
    build("bike2x_blk.png","bed2x_blk.png","wheel2x_blk.png",BLACK,CREME,True).convert("RGB").save(OUT+"/emblem_blk.png")
    build("bike2x.png","bed2x.png","wheel2x.png",ANTH,"trans",False).save(OUT+"/emblem_ind_trans.png")
    build("bike2x_red.png","bed2x_red.png","wheel2x_red.png",ROT,"trans",False).save(OUT+"/emblem_red_trans.png")
    build("bike2x_blk.png","bed2x_blk.png","wheel2x_blk.png",BLACK,"trans",False).save(OUT+"/emblem_blk_trans.png")
    print("Fassungen ok")
