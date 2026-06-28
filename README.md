# naville-handwerk.ch — öffentliche Webseite

Statischer Webauftritt der **Naville Handwerk GmbH** (Personalverleih im Handwerk, Raum Bern).
Reines HTML/CSS/JS, kein Server nötig.

## Inhalt

- `index.html` — Startseite
- `leistungen.html` — Was du von mir hast (✓/✗)
- `preisrechner.html` — Stundenansatz-Rechner (erzeugt eine PDF-Vereinbarung; jsPDF lokal in `vendor/`)
- `faq.html` — Häufige Fragen
- `philosophie.html` — Firmenphilosophie
- `impressum.html` — Impressum / Datenschutz
- `favicon.svg`, `404.html`, `robots.txt`, `sitemap.xml`, `CNAME`

## Deployment (GitHub Pages)

1. Den **Inhalt dieses Ordners** ins Repo-Root legen (nicht den Ordner `webseite/` selbst) — ODER den
   Ordner im Repo zu `docs/` umbenennen und die Pages-Quelle auf `/docs` stellen. Die Datei `CNAME` muss mit.
2. In den Repo-Einstellungen unter *Pages* die Custom Domain `naville-handwerk.ch` setzen und die Domain
   **verifizieren** (TXT-Challenge), **bevor** die DNS-Records gesetzt werden (Schutz vor Takeover).
3. **„Enforce HTTPS"** aktivieren.
4. DNS bei Infomaniak: Apex-A/AAAA auf die GitHub-Pages-IPs, `www` als CNAME, **CAA `0 issue "letsencrypt.org"`**
   (sonst kein HTTPS-Zertifikat). E-Mail (MX/SPF/DKIM/DMARC) läuft getrennt über Infomaniak.

## Sicherheit — bitte unbedingt beachten

- **Nur dieser Ordner gehört ins öffentliche Repo.** Niemals den übergeordneten Arbeitsordner committen
  (er enthält interne Notizen wie `CLAUDE.md`, Partner-/BTAG-Entwürfe).
- **Niemals Geheimnisse oder Personendaten committen:** keine API-Keys, Passwörter, SMTP-/DKIM-Schlüssel,
  keine Kundendaten, Wochenrapporte oder Rechnungen. Ein öffentliches Repo ist weltweit lesbar und bleibt
  **dauerhaft in der Git-History** (auch nach dem Löschen). `.gitignore` ist **keine** Sicherheitsschicht.
- In den Repo-Einstellungen **Secret Scanning + Push Protection** aktivieren (gratis für öffentliche Repos).
- Bei versehentlichem Leak: **zuerst den Schlüssel rotieren/widerrufen**, dann die History bereinigen.
- **jsPDF ist bewusst lokal** in `vendor/jspdf.umd.min.js` eingebunden (Version 2.5.1), nicht über ein CDN —
  das vermeidet Supply-Chain-Risiken. SRI-Hash zur Kontrolle:
  `sha512-qZvrmS2ekKPF2mSznTQsxqPgnpkI4DNTlrdUmTzrDgektczlKNRRhy5X5AAOnx5S09ydFYWWNSfcEqDTTHgtNA==`
- Jede Seite trägt eine Content-Security-Policy (per `<meta>`). Echte Header (HSTS, X-Frame-Options) kann
  GitHub Pages nicht setzen — bei Bedarf Cloudflare (gratis) davorschalten.

## Geschützte Funktionen gehören NICHT hierher

Login, Wochenrapporte, Rechnungen und Automatisierung dürfen **nicht** auf GitHub Pages laufen (statisch,
öffentlich). Sie gehören als **getrennte App mit Backend** (Auth + Datenbank) auf eine eigene Subdomain
(z. B. `app.naville-handwerk.ch`). Details: `../Sicherheit_Naville_Handwerk.md`.
