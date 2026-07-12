NAVILLE HANDWERK — Marken-Quellen (Brand-Assets)
==================================================

Dieser Branch `brand-assets` sichert die QUELLEN für Logo, Icons, Symbole und
Emblem — das, woraus wir Web-Grafiken, Ausdrucke und Merchandise erzeugen.
Er wird NICHT auf die öffentliche Website deployt (GitHub Pages läuft aus `main`).

Zugriff von einem anderen Gerät:  git clone …  &&  git checkout brand-assets

Die FERTIGEN Deliverables liegen bereits in `main`:
  - logo/            große Embleme (schwarzrot/rot, auf creme/rot/transparent) + Claim-Lockups
  - favicon.svg, favicon-32.png, apple-touch-icon.png, icon-192.png, icon-512.png
  - fonts/archivo-600.woff2 (+ OFL.txt)

Inhalt hier:
------------
logo-klein/   Neues kleines Logo (Wortmarke "naville/hw", h-Vertikale hochgezogen).
              final_tile.svg  = Favicon-Kachel (Papier + feine Linie)
              final_bleed.svg = randlose Fläche für Homescreen-Icons
              extract.py/build3.py = erzeugen die Pfade aus Archivo-Outlines (fonttools)
              v*/c*/s*/t*.svg = Zwischenstände/Varianten

emblem/       Großes Emblem (Lastenvelo + Anhänger + Firmenschild).
              _gen.py / _gen_final.py = AKTUELLE Pipeline (baut die vier logo/-Fassungen)
              quelle/  = Bausteine: bike/trailer/wheel/crate/toolbox (SVG+py),
                         multi_3col.png (3-Farb-Vektorisierung des Velo-Fotos),
                         sign.html/png (Blech-Schild in Archivo), 2x-Assets
              render/  = 2x-gerenderte Assets, die _gen.py zusammensetzt
              Hinweis: quelle/compose_final.py ist ALT (Box-Kappungs-Bug) — nicht nutzen.

symbole/      Die vier Kategorie-Symbole der Startseite/Leistungen als SVG:
              Auftragsspitzen, Ausfall, Reduzierte Pensen (Kalender), Kurzfristig (Velo).
              Lizenz-Herkunft: Bootstrap Icons (MIT), Material Symbols (Apache-2.0),
              Font Awesome Free (CC BY 4.0 → Namensnennung), teils selbst gezeichnet.

lockup/       Claim-Lockups "Der Notstromer für Berner Elektrikerfirmen"
              (Emblem + Text in Archivo, via Chromium gerendert). Quelle = a/b.html + style.css.

referenz/     FREMDE Referenzfotos, NUR zum Nachzeichnen des Emblems — nicht weiterverbreiten:
              multitinker.jpg  = Riese & Müller Multitinker (Herstellerfoto)
              anhänger.webp    = Hinterher-Anhänger (Herstellerfoto)

Marken-Farben:  Rot #C1121C (RAL 3020 Verkehrsrot) · Anthrazit #23252B/#22242A ·
                Papier #EFEEE8 · Grün #127A3C · Schild-Schrift/Display: Archivo (SIL OFL 1.1).

Werkzeuge:  Python mit PIL+numpy (Emblem-Komposition), fonttools (logo-klein aus Outlines),
            Chromium-Headless für Text-/Schild-Rendering (muss unter $HOME laufen, Snap-Sandbox).
