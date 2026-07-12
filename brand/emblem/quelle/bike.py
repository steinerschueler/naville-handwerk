import math, sys
ROT="#C1121C"; W="#FFFFFF"; CREME="#FAF6EF"
BG = sys.argv[1] if len(sys.argv)>1 else CREME
def spokes(cx,cy,r,n=8):
    inr=r-16; s=""
    for k in range(n):
        a=math.pi*2*k/n - math.pi/12
        x=cx+inr*math.cos(a); y=cy+inr*math.sin(a)
        s+=f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{W}" stroke-width="4"/>'
    return s
RW=(327,522); FW=(1127,526); rW=132
BB=(700,505); HT=(958,258); HTb=(1002,338); ST=(600,298)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="80 20 1250 690" stroke-linecap="round" stroke-linejoin="round">
<rect x="80" y="20" width="1250" height="690" fill="{BG}"/>
<g fill="none">
<circle cx="{RW[0]}" cy="{RW[1]}" r="{rW}" stroke="{ROT}" stroke-width="26"/>
{spokes(*RW,rW)}<circle cx="{RW[0]}" cy="{RW[1]}" r="11" fill="{ROT}" stroke="none"/>
<circle cx="{FW[0]}" cy="{FW[1]}" r="{rW}" stroke="{ROT}" stroke-width="26"/>
{spokes(*FW,rW)}<circle cx="{FW[0]}" cy="{FW[1]}" r="11" fill="{ROT}" stroke="none"/>

<!-- Longtail-Heck -->
<line x1="120" y1="308" x2="{ST[0]}" y2="{ST[1]}" stroke="{ROT}" stroke-width="20"/>
<line x1="150" y1="308" x2="150" y2="548" stroke="{ROT}" stroke-width="16"/>
<line x1="{BB[0]}" y1="{BB[1]}" x2="150" y2="548" stroke="{ROT}" stroke-width="18"/>
<line x1="490" y1="305" x2="490" y2="548" stroke="{ROT}" stroke-width="12"/>

<!-- Hauptrahmen -->
<line x1="{BB[0]}" y1="{BB[1]}" x2="{HT[0]}" y2="{HT[1]}" stroke="{ROT}" stroke-width="34"/>
<line x1="{BB[0]}" y1="{BB[1]}" x2="{ST[0]}" y2="{ST[1]}" stroke="{ROT}" stroke-width="22"/>
<line x1="{BB[0]}" y1="{BB[1]}" x2="{RW[0]}" y2="{RW[1]}" stroke="{ROT}" stroke-width="14"/>
<line x1="{HT[0]}" y1="{HT[1]}" x2="{HTb[0]}" y2="{HTb[1]}" stroke="{ROT}" stroke-width="22"/>
<line x1="{HTb[0]}" y1="{HTb[1]}" x2="{FW[0]}" y2="{FW[1]}" stroke="{ROT}" stroke-width="15"/>
<!-- Cockpit -->
<line x1="{HT[0]}" y1="{HT[1]}" x2="988" y2="54" stroke="{ROT}" stroke-width="15"/>
<line x1="940" y1="60" x2="1044" y2="46" stroke="{ROT}" stroke-width="14"/>
<!-- Sattel -->
<line x1="{ST[0]}" y1="{ST[1]}" x2="548" y2="104" stroke="{ROT}" stroke-width="14"/>
<path d="M486 96 Q548 78 606 96 Q560 112 508 108 Z" fill="{ROT}" stroke="none"/>
<!-- Kurbel -->
<circle cx="{BB[0]}" cy="{BB[1]}" r="30" stroke="{ROT}" stroke-width="9"/>
<circle cx="{BB[0]}" cy="{BB[1]}" r="6" fill="{ROT}" stroke="none"/>
<line x1="{BB[0]}" y1="{BB[1]}" x2="742" y2="548" stroke="{ROT}" stroke-width="10"/>
</g></svg>'''
open("bike.svg","w").write(svg); print("ok")
