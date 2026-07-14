#!/usr/bin/env python3
# Laced (gekreuztes) Speichenrad wie ein echtes Velo-Rad, statt radial.
import math, sys
def wheel_svg(cross=3, R=150, tire=26, nsp=32, hub=17, sw=2.1, color="#000000", inner="#FAF6EF"):
    cx=cy=180
    rimR = R - tire/2 - 2
    hr   = hub + 7            # Nabenflansch-Radius (Speichen starten hier)
    gap  = 2*math.pi/nsp
    delta= cross*gap          # tangentiale Kreuzung
    s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360">']
    for k in range(nsp):
        ah = gap*k
        sign = 1 if k%2==0 else -1
        ar = ah + sign*delta
        x1=cx+hr*math.cos(ah); y1=cy+hr*math.sin(ah)
        x2=cx+rimR*math.cos(ar); y2=cy+rimR*math.sin(ar)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R-tire/2:.1f}" fill="none" stroke="{color}" stroke-width="{tire}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R-tire-3:.1f}" fill="none" stroke="{color}" stroke-width="2.5"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{hub}" fill="{color}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{hub-6}" fill="{inner}"/>')
    s.append('</svg>')
    return "\n".join(s)
cross=int(sys.argv[1]); out=sys.argv[2]; color=sys.argv[3] if len(sys.argv)>3 else "#000000"
open(out,'w').write(wheel_svg(cross=cross,color=color))
print("wrote",out,"cross",cross)
