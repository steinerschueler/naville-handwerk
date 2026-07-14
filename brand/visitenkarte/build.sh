#!/usr/bin/env bash
# Baut die druckfertige Visitenkarten-PDF aus front-print.html / back-print.html.
# Endformat 85x55 mm + 3 mm Beschnitt, Schnittmarken, TrimBox/BleedBox.
#
# VOR DEM FINALEN BUILD: in back-print.html die Telefonnummer einsetzen
# (Platzhalter "+41 XX XXX XX XX" ersetzen). Die PDF mit echter Nummer NICHT committen
# (Repo ist oeffentlich).
#
# Voraussetzungen: chromium (headless), pikepdf (pip), poppler (pdfunite/pdfinfo) optional.
set -euo pipefail
cd "$(dirname "$0")"
UD="${TMPDIR:-/tmp}/_chrome_ud_vk"; mkdir -p "$UD"

for side in front back; do
  chromium --headless=new --no-sandbox --user-data-dir="$UD" \
    --no-pdf-header-footer --virtual-time-budget=8000 \
    --print-to-pdf="$side.pdf" "file://$PWD/$side-print.html"
done

python3 - << 'PY'
import pikepdf
from pikepdf import Array
MM = 2.8346456693  # pt/mm
def boxes(pageH):
    # Inhalt ist per CSS von oben-links verankert -> von oben messen
    trim  = [6*MM, pageH-61*MM, 91*MM, pageH-6*MM]   # 85 x 55, 6 mm inset
    bleed = [3*MM, pageH-64*MM, 94*MM, pageH-3*MM]   # 91 x 61, 3 mm inset
    return trim, bleed
out = pikepdf.Pdf.new()
for f in ("front.pdf","back.pdf"):
    with pikepdf.Pdf.open(f) as src:
        out.pages.append(src.pages[0])
for pg in out.pages:
    mb=[float(x) for x in pg.MediaBox]; pageH=mb[3]-mb[1]
    trim,bleed=boxes(pageH)
    pg.TrimBox  = Array([round(v,3) for v in trim])
    pg.BleedBox = Array([round(v,3) for v in bleed])
    pg.CropBox  = Array([round(v,3) for v in mb])
out.save("naville-handwerk-visitenkarte.pdf")
print("fertig: naville-handwerk-visitenkarte.pdf")
PY
