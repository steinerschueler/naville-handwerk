import math
ANTH="#23252B"
def wheel_svg(R=150, tire=26, nsp=32, hub=17):
    cx=cy=180
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360">']
    # feine Speichen
    for k in range(nsp):
        a=2*math.pi*k/nsp
        x=cx+(R-tire//2-2)*math.cos(a); y=cy+(R-tire//2-2)*math.sin(a)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{ANTH}" stroke-width="2.1"/>')
    # Reifen (fetter Ring)
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R-tire/2:.1f}" fill="none" stroke="{ANTH}" stroke-width="{tire}"/>')
    # Felge (dünne innere Linie)
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R-tire-3:.1f}" fill="none" stroke="{ANTH}" stroke-width="2.5"/>')
    # Nabe
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{hub}" fill="{ANTH}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{hub-6}" fill="#FAF6EF"/>')
    s.append('</svg>')
    return "\n".join(s)
open("wheel.svg","w").write(wheel_svg())
print("wheel.svg ok")
