ROT="#C1121C"; W="#FFFFFF"
# Werkzeugbox mit Spannset (Zurrgurt) — rot + weisse Details, transparent
# viewBox 0..180 x, 0..150 y; Bett-Kontakt y=128
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 150" stroke-linecap="round" stroke-linejoin="round">
<g>
<!-- Griff -->
<rect x="74" y="30" width="30" height="14" rx="4" fill="none" stroke="{ROT}" stroke-width="7"/>
<!-- Deckel -->
<rect x="24" y="42" width="130" height="20" rx="4" fill="{ROT}"/>
<!-- Korpus -->
<rect x="30" y="58" width="118" height="70" rx="5" fill="{ROT}"/>
<!-- Deckelnaht + Schloesser (weiss) -->
<line x1="34" y1="62" x2="144" y2="62" stroke="{W}" stroke-width="3"/>
<rect x="52" y="66" width="10" height="9" rx="2" fill="none" stroke="{W}" stroke-width="3"/>
<rect x="116" y="66" width="10" height="9" rx="2" fill="none" stroke="{W}" stroke-width="3"/>
<!-- Spannset: zwei weisse Gurte ueber die Box, Ratsche vorne -->
<line x1="60" y1="36" x2="60" y2="128" stroke="{W}" stroke-width="7"/>
<line x1="118" y1="36" x2="118" y2="128" stroke="{W}" stroke-width="7"/>
<rect x="52" y="92" width="16" height="13" rx="2" fill="{ROT}" stroke="{W}" stroke-width="3"/>
</g></svg>'''
open("toolbox.svg","w").write(svg); print("toolbox.svg ok")
