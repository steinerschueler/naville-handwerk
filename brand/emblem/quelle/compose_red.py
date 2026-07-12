from PIL import Image, ImageDraw, ImageFilter
OUT="/home/eric/naville_handwerk/tmp/_render"
ROT=(193,18,28); ANTH=(35,37,43); CREME=(250,246,239)
bike=Image.open("bike_red.png").convert("RGBA").resize((680,340))
bed=Image.open("trailer_bed_red.png").convert("RGBA").transpose(Image.FLIP_LEFT_RIGHT)
wheel=Image.open("wheel_red.png").convert("RGBA")
sign=Image.open(OUT+"/sign.png").convert("RGBA")
W,H=1500,700; c=Image.new("RGBA",(W,H),CREME+(255,))
G=560; bike_x=W-680-60; bike_y=G-323; tr_x=bike_x-520; tr_y=G-154
S=680/1400; Str=634/1400
# Positionen
axle=(bike_x+int(327*S), bike_y+int(524*S))                 # Velo-Hinterrad-Nabe
tw=(tr_x+ (bed.width-int((600-(-160))*Str)), tr_y+int((250-60)*Str))  # Anhaenger-Rad-Mitte (geflippt)
fw_x=bike_x+int(1127*S); rw_x=bike_x+int(327*S); stand_x=bike_x+int(540*S)
# Kontaktschatten
sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
def contact(cx,w,al): sd.ellipse((cx-w,G-10,cx+w,G+16),fill=ROT+(al,))
for cx in (fw_x,rw_x,tw[0]): contact(cx,120,55)
contact(stand_x,72,45)
sh=sh.filter(ImageFilter.GaussianBlur(9)); c.alpha_composite(sh)
d=ImageDraw.Draw(c)
# Veloständer vor dem Hinterrad
piv=(stand_x+8,G-70)
for foot in (stand_x-24,stand_x+30):
    d.line([piv,(foot,G-2)],fill=ROT,width=13)
    d.line([(foot-13,G-2),(foot+13,G-2)],fill=ROT,width=8)
# Anhaenger-Bett (ohne Rad)
c.alpha_composite(bed,(tr_x,tr_y))
# Deichsel Bett -> Velo-Achse
rail_y=tr_y+int((196-60)/380*bed.height)
P1=(tr_x+int((1400-(120-(-160)))*Str)-6, rail_y)   # vordere Anlenkung am Chassis
P2=(P1[0]-66, rail_y)                                # hintere Anlenkung
Q=(P1[0]+42, rail_y+9)                               # Gabelpunkt der Deichsel
d.line([axle, Q], fill=ROT, width=12)               # Hauptrohr zur Velo-Achse
d.line([Q, P1], fill=ROT, width=11); d.line([Q, P2], fill=ROT, width=11)  # A-Triangulierung
for P in (P1,P2): d.line([(P[0]-12,P[1]),(P[0]+12,P[1])], fill=ROT, width=10)  # Anlenk-Bracket
d.ellipse([Q[0]-7,Q[1]-7,Q[0]+7,Q[1]+7], fill=ROT)  # Gelenk
d.ellipse([axle[0]-11,axle[1]-11,axle[0]+11,axle[1]+11], fill=ROT)  # Kupplung an der Nabe
# Schild fuellt Bett
bed_l=tr_x+int((1400-(1150-(-160)))*Str); bed_r=tr_x+int((1400-(120-(-160)))*Str); bed_w=bed_r-bed_l
bed_top=tr_y+int((150-60)/380*bed.height)
sw=int(bed_w*0.99); shh=int(sw/1.94); sign2=sign.resize((sw,shh))
c.alpha_composite(sign2,(bed_l+(bed_w-sw)//2, bed_top-shh+4))
# Anhaenger-Rad im VORDERGRUND (nach Bett+Schild)
c.alpha_composite(wheel,(tw[0]-wheel.width//2, tw[1]-wheel.height//2))
# Velo drueber
c.alpha_composite(bike,(bike_x,bike_y))
c.convert("RGB").save(OUT+"/emblem_red.png")
print("ok tw",tw,"axle",axle)
