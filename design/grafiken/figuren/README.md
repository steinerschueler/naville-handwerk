# Figuren-System (parametrische Piktogramm-Figuren)

**Zweck:** Erzaehl-Werkzeug fuer die Website und andere Deliverables: Szenen aus gefuellten
Piktogramm-Figuren, die eine Aussage *zeigen* statt sie im Fliesstext zu erklaeren (z. B.
„mehrere Bauarbeiter, jede mit anderer Taetigkeit", „einer schuftet, einer feiert").
Figuren sind **posierbar**, halten **Requisiten** (Bohrmaschine, Werkzeug, Glas …) und werden
programmatisch als SVG erzeugt, zu PNG gerendert.

## Arbeitsweise fuer spaetere Instanzen

- **Brauchbare Ergebnisse** (Modul, Doku, wiederverwendbare Renders, Referenzen) gehoeren
  hierher: `design/grafiken/figuren/`.
- **Alles andere** (Probe-Renders, Experimente, Zwischenschritte) in `tmp/` (gitignored) —
  nicht hier ablegen.
- Am Ende einer Session: Brauchbares hierher, `tmp/`-Kram aufraeumen.
- **Nur Python-Standardlib** (`math`) verwenden — keine Fremd-Libraries (bewusst).
- Immer am **gerenderten PNG** pruefen (inline-SVG rendert bei Eric nicht), reinzoomen,
  dann urteilen.

> ⚠️ **Deploy-Hinweis:** Die Website referenziert Assets aus `design/` (Emblem unter
> `design/logo/`, Icons unter `design/`), daher wird `design/` bewusst **mit-committet und
> -deployed**. Folge: auch die `.py`/`.html` hier sind dann oeffentlich unter der Domain
> erreichbar (harmlos, keine Geheimnisse) — **keine sensiblen Daten in `design/` ablegen**.
> (Optional koennte man spaeter nur `design/grafiken/figuren/*.py`+`*.html` gitignoren, um die
> Skripte aus dem Deploy zu halten; die Assets muessen deployen.) Commit/Push nur auf Erics Wort.

---

## Dateien

- `figures.py` — das Modul (stdlib-only). Enthaelt `resting_figure()` (solid),
  `keyline_out()`, `prop_drill/martini`, `pose_figure()` (Prototypen). `python3 figures.py`
  schreibt `demo.html`.
- `demo.png` — Beispiel-Render (Ruhepose + posierte Prototypen).
- `referenz/pictogramm-mann.png` — **Ziel-Bauart** (ISO-Piktogramm): Arme neben Torso,
  Spalt, gerade Aussenlinie.
- `referenz/person-brustbild.png` — fruehere Referenz (Kopf/Schulter-Verhaeltnis).
- `referenz/ruhepose-entstehung.png` — Entstehung der Ruhepose (Naht-Fix).

## Render-Setup

Chromium headless unter `$HOME` (Snap-Sandbox), Figuren als SVG in eine HTML-Huelle:
```
/snap/bin/chromium --headless=new --no-sandbox \
  --user-data-dir=$HOME/naville_handwerk/tmp/_ud \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=B,H \
  --screenshot=OUT file://…/demo.html
```

---

## Stil-Grundsaetze (aus vielen Iterationen entschieden)

1. **Gefuellte Silhouette**, kein duennes Strichmaennchen. Schema wie Ausfaelle-Symbol /
   ISO-Piktogramm (`referenz/pictogramm-mann.png`).
2. **Kopf** = separater Kreis mit kleiner Luecke, **kein gezeichneter Hals**.
   (Aktuell r9 = Ausfaelle-Grosse; Referenz hat ihn kleiner — offen.)
3. **Ruhearme liegen NEBEN dem Torso**, nicht darueber: aeussere Saeulen, getrennt durch einen
   **duennen weissen Spalt** (Negativraum), oben an den **Schultern** verbunden.
4. **Gerade Aussenlinie**: Torso-Aussenkante = Bein-Aussenkante → durchgehende Linie Beine→Achseln.
5. **Schultern** buendig zur Arm-Aussenkante, proportional zur Torso-Breite.
6. **Kreuzende Arme** (Arm VOR dem Koerper) bekommen eine weisse **Keyline** (kein Spalt moeglich).

## Bauart Ruhepose ("Variante B", SOLID — in `resting_figure()`)

Canvas 100x100. Alle Teile `#22242A`, ueberlappend (Naehte vermeiden = ueberlappen, nicht anstossen).
- Zentrale Saeule (Torso = Beine): x **41.5–58.5**.
- Beine: Mittellinie 45/55, Breite 7 → Aussenkante 41.5/58.5, Schritt-Spalt ~3, y59–90.
- Torso: **gerade Seiten**, y **30**→62 (reicht nach oben UNTER den Yoke → keine Naht in Achselhoehe).
- Arme: Mittellinie **37/63**, Breite 6.5 → Spalt ~2, y31–57 (enden Huefthoehe, oben vom Yoke gedeckt).
- Yoke: abgerundetes Rechteck, x = Arm-Aussenkante 33.75–66.25, y26–34, rx7.
- Kopf: Kreis r9 bei (50,14).
- Reihenfolge: Arme, Beine, Torso, Yoke, Kopf.

## Keyline fuer kreuzende Arme (Prototyp — in `keyline_out()`)

- **AUSSEN** ums Glied (Offset w/2 + k/2 + Rand), nicht im Glied.
- Nur **zwei Laengskanten + Handkappe**; **quert nie** die Gliedbreite (sonst halbiert — kam von
  runden Endkappen). **Runder Stopp.**
- **Stoppt frueh** (Arm ~82 %, Bein ~90 % Richtung Wurzel) → Wurzel bleibt verbunden. **Kein
  spitzer Taper** in den Torso.
- Auf dem ink-Glied (das vorne liegt) ZULETZT zeichnen.

## Requisiten (Prototyp, roh — `prop_drill`, `prop_martini`)

Am Handgelenk platziert, um Richtung `fa` rotiert. Bohrmaschine liest noch mittelmaessig → Form schaerfen.

---

## Stand

- ✅ **Ruhepose** (`resting_figure`): abgestimmt & solid.
- 🟡 **Keyline** (`keyline_out`): Prototyp gelöst, **nicht** in die Ruhepose-Bauart integriert.
- 🟡 **posierbare Figur** (`pose_figure`): Prototyp; nutzt (noch) KEINEN Ruhe-Spalt.
- 🟡 **Requisiten**: Prototyp, Form roh.

## Naechste Schritte

1. **Vereinheitlichen**: Ruhe-Modus (Spalt zwischen ruhendem Arm und Torso) und Kreuz-Modus
   (Keyline fuer Arm vor dem Koerper) pro Arm sauber zusammenfuehren, auf Basis der crispen
   Ruhepose-Bauart (kein goo-Blur).
2. Kopfgroesse entscheiden (Ausfaelle-gross vs. Referenz-schlank).
3. Schritt-Ausschnitt ggf. runden.
4. Requisiten-Bibliothek ausbauen (Bohrer v2, Hammer, Kelle, Kabelrolle, Laptop, Kaffee …).
5. Interaktiver Poser (HTML, Slider/Gelenke ziehen) → Bedien-Tool, das Parameter/SVG ausgibt.
6. Erste Anwendung: **Termindruck-Figur** (Haende in den Haaren) fuer das Website-Symbol
   (Sektion „Wann ich einspringe", `index.html`).

## Gelernte Fehler (NICHT wiederholen)

- **Nicht durch Umpositionieren „glaetten"** — Whack-a-Mole (jede Korrektur bricht die naechste).
  Uebergaenge sind **Geometrie**, nicht Positionierung. (Eric-Grundsatz.)
- Verworfen: duennes Strichmaennchen · konischer/realistischer Torso · Ragdoll-Stoss-Gelenke ·
  goo-Blur (weiche Kanten → durch crispe Flaeche + Spalt ersetzt) · Keyline IM Glied · Keyline
  QUER uebers Glied (halbiert) · spitzer Taper in den Torso · „Kurzhosen"-Saum · Naht in
  Achselhoehe (Torso muss den Yoke ueberlappen).

## Recherche (Keyline-Technik)

Drei Rechercheagenten (SVG-nativ · Illustrations-/Werkzeug-Konventionen · Geometrie/Offset):
Ursache des „Halbierens" = runde Endkappe → Querbogen. Loesung: zwei Offset-Kantenlinien (butt)
oder getaperter gefuellter Kanten-Pfad. Profi-Konvention „interior line / self-occlusion outline"
nur an der Ueberlappung, endet ausgetapert („lost edge") — bei uns als frueher Stopp gewaehlt.
Kein natives Variable-Width-Stroke in SVG; Offset analytisch (shapely/pyclipper nicht noetig).
