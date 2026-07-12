from PIL import Image, ImageDraw, ImageFilter
import numpy as np, math
import importlib.util
spec=importlib.util.spec_from_file_location("g","/home/eric/naville_handwerk/tmp/_gen.py")
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
OUT="/home/eric/naville_handwerk/tmp/_render"
ROT=(193,18,28); BLACK=(0,0,0); WHITE=(255,255,255)
SQ2=math.sqrt(2)

def chamf_poly(L,R,T,B,c):
    # gekappte Ecken oben-RECHTS und unten-LINKS, im Uhrzeigersinn
    return [(L,T),(R-c,T),(R,T+c),(R,B),(L+c,B),(L,B-c)]

def fill_poly(size,pts):
    m=Image.new("L",size,0); ImageDraw.Draw(m).polygon(pts,fill=255); return np.array(m)>0

def inner_frame_rect(geom):
    # Innerer weisser Rahmen aus sign.html (Mittellinie, stroke 6):
    #   Polygon 34,34 854,34 897,77 897,446 77,446 34,403
    #   -> Rechteck L=34,R=897,T=34,B=446 mit 45-Grad-Fase 43 px an TR/BL (854,34->897,77).
    # An finale Position umrechnen (nach Flip: sign2 bei msign_x,sign_y, Bild danach /2).
    sw=geom["sw"]; shh=geom["shh"]; msign_x=geom["msign_x"]; sign_y=geom["sign_y"]
    PL=msign_x/2.0; PT=sign_y/2.0            # Platten-Ecke oben-links final
    kx=(sw/2.0)/931.0; ky=(shh/2.0)/480.0    # sign-Koord -> final (x/y ~ gleich => 45 Grad)
    L=PL+34*kx; R=PL+897*kx; T=PT+34*ky; B=PT+446*ky
    c=43.0*kx                                 # Fasen-Laenge inneren Rahmens, final
    return L,R,T,B,c,kx

def frame_masks(size, geom, d_red, WIDTH):
    # rotes Feld + weisser Aussenrand KONZENTRISCH zum INNEREN RAHMEN (nicht zur Platte).
    # Struktur innen->aussen: innerer Rahmen | rotes Feld (d_red) | weisser Rand (WIDTH) | rot.
    # Miter-Offset der gekappten Rechteck-Form -> rote Bahn ueberall gleich breit (Gerade==Fase),
    # die 45-Grad-Fasen aller drei Linien liegen konzentrisch/parallel.
    L,R,T,B,c,k=inner_frame_rect(geom)
    s=3.0*k                       # halbe Strichbreite (stroke 6) -> Aussenkante inneren Rahmens
    bi=s+d_red                    # Innenkante des Aussenrands (= Aussenkante rotes Feld)
    bo=bi+WIDTH                   # Aussenkante des Aussenrands
    def off(d): return (L-d,R+d,T-d,B+d, c+d*(2-SQ2))   # Miter-Offset um d nach aussen
    outer_edge=fill_poly(size, chamf_poly(*off(bo)))
    red_zone=outer_edge & ~fill_poly(size, chamf_poly(*off(s)))   # Rahmen-Aussenkante .. Rand-Aussenkante
    border  =outer_edge & ~fill_poly(size, chamf_poly(*off(bi)))  # bi .. bo
    return red_zone, border

def plate_cut_mask(size, geom, e=2.0):
    # Die beiden 45-Grad-KAPPUNGS-Dreiecke der PLATTE (TR, BL). Dort scheint durch den Flip
    # (Doppel-Composite von sign2) die gespiegelte Platte durch -> Stoerdreieck. Die Dreiecke
    # bleiben INNERHALB des Platten-Rechtecks (kein Anhaenger/Bett beruehrt).
    sw=geom["sw"]; shh=geom["shh"]; msign_x=geom["msign_x"]; sign_y=geom["sign_y"]
    pL=msign_x/2.0; pT=sign_y/2.0; pR=(msign_x+sw)/2.0; pB=(sign_y+shh)/2.0
    ch=77.0*(sw/2.0)/931.0        # Platten-Fase (77 px bei 931), final
    m=Image.new("L",size,0); dd=ImageDraw.Draw(m)
    dd.polygon([(pR-ch-e,pT),(pR,pT),(pR,pT+ch+e)],fill=255)        # TR (Ecke bei pR,pT)
    dd.polygon([(pL,pB),(pL+ch+e,pB),(pL,pB-ch-e)],fill=255)        # BL (Ecke bei pL,pB)
    return np.array(m)>0

def white_base_ch(trshift=0,wshift=0,maxf=19,d_red=15.5,WIDTH=14.0):
    # Rot-Basis + Halo-Rim + weisses Emblem  (unveraendert)
    we,M2,geom=g.emblem("bike2x_w.png","bed2x_w.png","wheel2x_w.png",WHITE,"trans",trshift,wshift,shadow=False,return_plate=True)
    a=np.array(we)[:,:,3]
    dil=np.array(Image.fromarray(a).filter(ImageFilter.MaxFilter(maxf)))
    rim=np.clip(dil.astype(int)-a.astype(int),0,255).astype(np.uint8)
    rimimg=np.zeros((we.height,we.width,4),np.uint8); rimimg[:,:,0:3]=255; rimimg[:,:,3]=rim
    b=Image.new("RGBA",we.size,ROT+(255,)); b.alpha_composite(Image.fromarray(rimimg)); b.alpha_composite(we)
    red_zone,border=frame_masks(we.size,geom,d_red,WIDTH)
    arr=np.array(b)
    arr[red_zone]=[ROT[0],ROT[1],ROT[2],255]   # rotes Feld sauber
    arr[border]=[255,255,255,255]              # weisser Aussenrand
    return Image.fromarray(arr).convert("RGB")

def szr_ch(trshift=90,wshift=46,d_red=15.5,WIDTH=14.0,**kw):
    wb=white_base_ch(trshift,wshift,d_red=d_red,WIDTH=WIDTH,**kw).convert("RGBA")
    ov,_,geom=g.emblem("bike2x_blk.png","bed2x_blk.png","wheel2x_blk.png",BLACK,"trans",trshift,wshift,shadow=False,wheeldisc=True,return_plate=True)
    wb.alpha_composite(ov)
    # Overlay enthaelt sign2 erneut -> bringt das Flip-Stoerdreieck an den Platten-Fasen zurueck.
    # NUR in den beiden Platten-Kappungs-Dreiecken das konzentrische Feld/Rand rekonstruieren
    # (Bett/Deichsel/Rad bleiben unberuehrt, da die Dreiecke im Platten-Rechteck liegen).
    red_zone,border=frame_masks(wb.size,geom,d_red,WIDTH)
    cut=plate_cut_mask(wb.size,geom)
    arr=np.array(wb)
    arr[cut & ~border]=[ROT[0],ROT[1],ROT[2],255]
    arr[cut & border ]=[255,255,255,255]
    return Image.fromarray(arr).convert("RGB")

if __name__=="__main__":
    im=szr_ch(90,46); im.save("/home/eric/naville_handwerk/tmp/_szr_fix2.png")
    _,_,geom=g.emblem("bike2x_w.png","bed2x_w.png","wheel2x_w.png",WHITE,"trans",90,46,shadow=False,return_plate=True)
    L,R,T,B,c,k=inner_frame_rect(geom)
    print("inner-frame final: L%.1f R%.1f T%.1f B%.1f  Fase=%.2f px  (k=%.4f)"%(L,R,T,B,c,k))
    def z(box,out,zoom=8):
        cc=im.crop(box); cc=cc.resize((cc.width*zoom,cc.height*zoom),Image.NEAREST); cc.save(out)
    z((1160,190,1245,270),"/home/eric/naville_handwerk/tmp/_fix2_tr.png")
    z((730,400,815,480),"/home/eric/naville_handwerk/tmp/_fix2_bl.png")
    print("ok  _szr_fix2.png / _fix2_tr.png / _fix2_bl.png")
