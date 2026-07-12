ROT="#C1121C"; W="#FFFFFF"
# Maschinenkiste, Seitenansicht, hoeher; rot + weisse Rahmen/Verstrebung, transparent
# viewBox 0 0 150 220 ; Bett-Kontakt y=205
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 220" stroke-linecap="round" stroke-linejoin="round">
<g>
<rect x="18" y="40" width="114" height="165" rx="4" fill="{ROT}"/>
<g fill="none" stroke="{W}" stroke-width="5">
  <rect x="26" y="48" width="98" height="149"/>              <!-- innerer Rahmen -->
  <line x1="26" y1="88" x2="124" y2="88"/>                    <!-- oberer Querriegel -->
  <line x1="26" y1="158" x2="124" y2="158"/>                  <!-- unterer Querriegel -->
  <line x1="26" y1="158" x2="124" y2="88"/>                   <!-- Diagonalstrebe -->
</g>
</g></svg>'''
open("crate.svg","w").write(svg); print("crate.svg ok")
