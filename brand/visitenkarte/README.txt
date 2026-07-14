VISITENKARTE — Naville Handwerk
===============================
Stand: 2026-07-14. Zweiseitig, 85 x 55 mm (CH-Standard) + 3 mm Beschnitt ringsum.
Gerendert bei 300 dpi = 1075 x 720 px (inkl. Beschnitt).

DATEIEN
-------
- front.html / back.html   Quellen (Chromium-render, 1075x720, DSF1, transparenter BG).
- front.png / back.png     gerenderte Seiten (300 dpi).
- emblem-velo-card.png      Comic-Emblem der Werbeseite (finaler Stand, OHNE i.G.).
- archivo-600.woff2         Display-Font (SIL OFL 1.1).

DESIGN
------
Werbeseite (front): Creme (#FAF6EF). Comic-Emblem (Werkzeugkasten-Velo, laced-Rad,
  schwarzer Comic-Umriss) mit Schild „NAVILLE HANDWERK GMBH" (OHNE i.G. — die Karte
  wird erst nach der Gruendung gebraucht). Darunter Claim „Der Notstromer fuer
  Berner Elektrikerfirmen" (dunkel, „Notstromer" rot).
Kontaktseite (back): Creme, roter Draht oben. Kopf „naville handwerk GmbH" ueber die
  volle Breite (dominiert oberes Drittel). Darunter, nach rechts eingerueckt: Name,
  Funktion, grosse rote Telefonnummer, dann E-Mail / Web / Adresse mit Symbolen
  (Telefon, Mail, Globe, Pin — rot).

PLATZHALTER / VOR DEM DRUCK ERGAENZEN
------------------------------------
- Telefonnummer: aktuell „+41 XX XXX XX XX" -> echte Nummer eintragen (back.html).
- Kein Portraetfoto (bewusst; Slogan ebenfalls bewusst weggelassen).
- Emblem traegt „GMBH" ohne i.G. — passt fuer die Zeit NACH dem HR-Eintrag. Falls
  frueher gebraucht: i.G.-Emblem aus brand/emblem/newdesign/ (sign_box_ig.html) bauen.

DRUCKFERTIGE PDF (erledigt — Pipeline im Ordner)
------------------------------------------------
- front-print.html / back-print.html : Druck-Bogen je Seite (97x67 mm) mit der auf
  91x61 mm skalierten Karte + Schnittmarken; Text bleibt vektoriell.
- build.sh : rendert beide Seiten (Chromium --print-to-pdf), fuehrt sie zusammen und
  setzt TrimBox 85x55 / BleedBox 91x61 (pikepdf) -> naville-handwerk-visitenkarte.pdf.
- DRUCK-INFO.txt : Format-/Farb-/Beschnitt-Spez fuer die Druckerei (Marken-Rot CMYK
  0/100/100/10 vermerkt; PDF selbst liegt in RGB).
- OFFEN nur: echte CMYK-/PDF-X-Datei nur auf Druckerei-Wunsch (Zielwerte in DRUCK-INFO).

DATENSCHUTZ — TELEFONNUMMER NICHT COMMITTEN
-------------------------------------------
- Repo ist OEFFENTLICH. back-print.html traegt die Nummer nur als Platzhalter
  „+41 XX XXX XX XX“. Fuer den Druck die echte Nummer lokal einsetzen und build.sh
  laufen lassen; die PDF mit echter Nummer NICHT committen (bleibt lokal / geht an die Druckerei).

REPRODUKTION DES KARTEN-EMBLEMS
-------------------------------
Wie das Website-Emblem, aber Schild sign_box.html (GMBH, ohne i.G.) statt
sign_box_ig.html — siehe brand/emblem/newdesign/README.txt.
