EMBLEM-NEUDESIGN (Comic-Werkzeugkasten) — Reproduktion & Rückbau
================================================================
Stand: 2026-07-14. Ersetzt das flache rot-weisse Schild durch einen
3D-Werkzeugkasten im Comic-Stil. LIVE auf der Website ist die Fassung
emblem-schwarzrot-transparent.png (Hero + Footer aller Seiten).

WAS NEU IST (gegenüber dem alten flachen Schild)
------------------------------------------------
- Anhänger-Schild = 3D-WERKZEUGKASTEN: schwarze Fassung (Rahmen), Eckbeschläge,
  Deckelnaht, zwei Schnappverschlüsse. KEIN Tragegriff (bewusst entfernt).
- Schrift SCHWARZ mit DICKEM weissem Saum (paint-order stroke). Grosse Zeilen
  stroke-width 22, GMBH-Zeile 16. Web-Schild trägt "GMBH i.G.", Karte "GMBH".
- Box HÖHER als früher -> Pipeline-Seitenverhältnis geändert: in _gen.py ist
  shh = int(sw/1.6052)  (früher /1.94). Das Schild-SVG ist 931x580 (=1.6052).
- COMIC-UMRISS: schwarze Kontur um Silhouette + rote Flächen (comic_outline.py).
- ANHÄNGERRAD: gekreuzte (laced) Speichen statt radial (wheel_laced.py, cross=3),
  passend zu den foto-getracten Velo-Rädern.

DATEIEN HIER
------------
- _gen.py               Kern (emblem()), MIT shh=/1.6052. Erwartet Assets in tmp/_render/.
- build_emblem.py       baut die 6 Emblem-PNGs (Logik wie _gen_final.py).
- sign_box_ig.html      Werkzeugkasten-Schild, "GMBH i.G." (WEBSITE).
- sign_box.html         Werkzeugkasten-Schild, "GMBH" (VISITENKARTE, ohne i.G.).
- wheel_laced.py        laced-Rad-Generator (cross=3). Erzeugt SVG -> 274px PNG.
- wheel2x_blk_laced.png / wheel2x_red_laced.png   fertige laced-Räder (schwarz/rot).
- comic_outline.py      Comic-Umriss (outer + red), Alpha-basiert (transparente Fassung).
- emblem-schwarzrot-transparent_NEU.png   das aktuell live deployte Emblem.
- ../pre-newdesign/emblem-schwarzrot-transparent_OLD-ig-flat.png   die ALTE Fassung.

NEU BAUEN (transparente Website-Fassung)
----------------------------------------
1. tmp/_render/ mit 2x-Assets füllen: brand/emblem/render/*.png nach tmp/_render/;
   font archivo-600.woff2 dorthin.
2. Rad ersetzen: wheel2x_blk_laced.png -> tmp/_render/wheel2x_blk.png
   (rote Variante: wheel2x_red_laced.png -> wheel2x_red.png).
3. Schild rendern (Chromium headless, DSF1, 931x580, transparenter BG):
   sign_box_ig.html -> tmp/_render/sign.png   (Karte: sign_box.html)
4. _gen.py -> tmp/_gen.py ; dann:  python3 build_emblem.py tmp/_out
5. Comic-Umriss auf die transparente Fassung:
   python3 comic_outline.py tmp/_out/emblem-schwarzrot-transparent.png OUT.png 9 9
   -> OUT.png ist das fertige emblem-schwarzrot-transparent.png.

RÜCKBAU auf das ALTE flache Schild
----------------------------------
- Einfach: pre-newdesign/emblem-schwarzrot-transparent_OLD-ig-flat.png zurück nach
  logo/emblem-schwarzrot-transparent.png (auf main), committen, deployen.
- Baseline-Commit auf main VOR dem Neudesign: 950d901 (dort die alte Fassung).

ALLE logo/-FASSUNGEN NACHGEZOGEN (2026-07-15, erledigt)
-------------------------------------------------------
- build_comic.py baut alle 6 Emblem-Fassungen (Ausgabe-Ordner als Argument):
  * schwarzrot (auf-creme/auf-rot/transparent): schwarzes Schild (sign_box_ig.html)
    + Comic-Umriss. Der Umriss wird auf der TRANSPARENTEN Fassung (Vollcanvas)
    berechnet und dann auf Creme/Rot gesetzt -> loest das "Alpha-Trick greift nur
    transparent"-Problem der nicht-transparenten Fassungen.
  * rot einfarbig (auf-creme/transparent/weiss-umrandet-auf-rot): ROTES Schild
    (sign_box_ig_red.html: rote Flaechen, Creme-Details = Papier-Aussparung),
    KEIN schwarzer Umriss. Der schwarze 3D-Kasten reduziert nicht auf eine Farbe,
    daher eigenes rotes Schild.
- Schild-Renders: sign_box_ig.html -> sign_blk.png, sign_box_ig_red.html ->
  sign_red.png (Chromium DSF1, 931x580, transparent) nach tmp/_render/;
  build_comic.py schaltet per use_sign("blk"/"red") um.
- 4 Lockups: ../../lockup/a.html (Vollemblem) + b.html (Schild). Bilder ersetzt:
  ../../lockup/emblem_full.png (Comic-Vollemblem) + emblem_sign.png (Comic-Kasten).
- RAD-FIX: das laced-Rad (274x274) ist kleiner/hoeher zentriert als das alte
  radiale -> Anhaengerrad lag 11px zu hoch. In build_comic.py GEO trdy 12->23
  (ganzen Anhaenger runter) -> alle drei Raeder auf einer Bodenlinie. Auch das
  live Website-Emblem wurde damit neu gebaut (main-Commit).
- i.G.: sobald Handelsregister-Eintrag durch -> auf dem Web-Schild "i.G." raus
  (sign_box_ig.html -> sign_box.html-Variante) und neu bauen. Siehe auch
  ../pre-ig-baseline/ROLLBACK-i.G.txt.
