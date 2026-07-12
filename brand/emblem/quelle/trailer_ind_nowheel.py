import math
ROT="#C1121C"; ANTH="#23252B"; CREME="#FAF6EF"
def wheel(cx,cy,R=150,tire=40,nsp=36,hub=17):
    s=""
    for k in range(nsp):
        a=2*math.pi*k/nsp
        x=cx+(R-tire/2-2)*math.cos(a); y=cy+(R-tire/2-2)*math.sin(a)
        s+=f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{ANTH}" stroke-width="1.9"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="{R-tire/2:.1f}" fill="none" stroke="{ANTH}" stroke-width="{tire}"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="{R-tire-3:.1f}" fill="none" stroke="{ANTH}" stroke-width="2.5"/>'
    s+=f'<circle cx="{cx}" cy="{cy}" r="{hub}" fill="{ANTH}"/><circle cx="{cx}" cy="{cy}" r="{hub-7}" fill="{CREME}"/>'
    return s
# Layout: Rad Mitte (600,250) R150 -> Boden 400
wx,wy,R=600,250,150; ground=wy+R
bedT=150; bedB=196; bedX0=120; bedX1=1150
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-160 60 1400 380" stroke-linecap="round" stroke-linejoin="round">
<!-- Rad separat im Vordergrund -->
<!-- Anthrazit-Fahrwerk unter dem Bett + Achsstrebe -->
<rect x="{bedX0}" y="{bedB-6}" width="{bedX1-bedX0}" height="10" fill="{ANTH}"/>
<path d="M{wx-70} {bedB} L{wx} {wy} L{wx+70} {bedB} Z" fill="{ANTH}"/>
<!-- rotes Bett (satter Balken) -->
<rect x="{bedX0}" y="{bedT}" width="{bedX1-bedX0}" height="{bedB-bedT}" rx="4" fill="{ROT}"/>
<!-- Bordwand hinten -->
<rect x="{bedX1-14}" y="{bedT-40}" width="14" height="46" fill="{ROT}"/>
<!-- Zurr-Schlitze auf der Bettkante (anthrazit) -->
{''.join(f'<rect x="{x}" y="{bedT+8}" width="22" height="7" rx="2" fill="{ANTH}"/>' for x in range(bedX0+40,bedX1-30,74))}
<!-- (Deichsel wird in der Komposition gezeichnet) -->
</svg>'''
open("trailer_ind.svg","w").write(svg); print("trailer_ind.svg ok")
