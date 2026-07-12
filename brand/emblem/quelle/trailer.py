import math
ROT="#C1121C"; W="#FFFFFF"
def spokes(cx,cy,r,n=8):
    inr=r-16; s=""
    for k in range(n):
        a=math.pi*2*k/n - math.pi/12
        x=cx+inr*math.cos(a); y=cy+inr*math.sin(a)
        s+=f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{W}" stroke-width="4"/>'
    return s
# LAENGERE Ladeflaeche; Rad zentraler; transparent (kein bg-rect)
WH=(820,522); rW=132
bedY=372; bedH=40; bedX0=150; bedX1=1540
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-120 20 1680 690" stroke-linecap="round" stroke-linejoin="round">
<g fill="none">
<circle cx="{WH[0]}" cy="{WH[1]}" r="{rW}" stroke="{ROT}" stroke-width="26"/>
{spokes(*WH,rW)}<circle cx="{WH[0]}" cy="{WH[1]}" r="11" fill="{ROT}" stroke="none"/>
<rect x="{bedX0}" y="{bedY}" width="{bedX1-bedX0}" height="{bedH}" rx="6" fill="{ROT}" stroke="none"/>
{''.join(f'<rect x="{x}" y="{bedY+7}" width="20" height="8" rx="2" fill="{W}" stroke="none"/>' for x in range(bedX0+30,bedX1-20,64))}
<line x1="{bedX1}" y1="{bedY}" x2="{bedX1}" y2="{bedY-46}" stroke="{ROT}" stroke-width="14"/>
<line x1="{bedX0}" y1="{bedY+bedH-6}" x2="-70" y2="{bedY+bedH+40}" stroke="{ROT}" stroke-width="13"/>
<circle cx="-84" cy="{bedY+bedH+46}" r="14" stroke="{ROT}" stroke-width="9"/>
<line x1="{WH[0]}" y1="{bedY+bedH}" x2="{WH[0]}" y2="{WH[1]-8}" stroke="{ROT}" stroke-width="10"/>
</g></svg>'''
open("trailer.svg","w").write(svg); print("langer Anhaenger ok, viewBox 1680")
