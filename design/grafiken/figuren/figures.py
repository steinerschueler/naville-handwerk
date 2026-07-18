"""
Parametrische Piktogramm-Figuren — Naville Handwerk.

Erzeugt gefuellte Piktogramm-Figuren als SVG (zu PNG gerendert via headless Chromium).
Zweck: Erzaehl-Werkzeug fuer Website/Deliverables — Szenen aus Figuren, die eine Aussage
zeigen (z. B. mehrere Bauarbeiter mit verschiedenen Taetigkeiten).

Nur Python-Standardlib (math). Siehe README.md fuer Bauart, Stand und offene Punkte.

STAND:
  * resting_figure()  — Ruhepose ("Variante B"): SOLID, abgestimmt. Arme neben Torso mit
    Spalt, gerade Aussenlinie Bein->Achsel, Schulter proportional, keine Naehte.
  * keyline_out()     — weisse Kontur fuer KREUZENDE Arme: Prototyp (getestet, nicht in
    resting_figure integriert). Aussen ums Glied, quert nie, stoppt frueh, runder Stopp.
  * prop_drill/martini — Requisiten: Prototyp, Form roh.
  * pose_figure()     — posierbare Kapsel-Figur mit Keyline: Prototyp. Nutzt (noch) KEINEN
    Ruhe-Spalt; das Zusammenfuehren von Ruhe-Modus (Spalt) und Kreuz-Modus (Keyline) ist
    der naechste Schritt.

Canvas: 100x100 pro Figur.
"""
import math

INK = "#22242A"
WHITE = "#ffffff"
RED = "#C1121C"

# ----------------------------------------------------------------------------- Helfer
def f(x): return f"{x:.2f}"
def pt(p, l, a):
    """Punkt ab p, Laenge l, Winkel a (Grad). 0=oben, 90=rechts, 180=unten, 270=links."""
    r = math.radians(a); return (p[0] + l * math.sin(r), p[1] - l * math.cos(r))
def U(a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1e-9; return (dx/L, dy/L)
def cap(a, b, w, col=INK):
    return (f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" '
            f'stroke="{col}" stroke-width="{f(w)}" stroke-linecap="round"/>')
def circ(c, r, col=INK):
    return f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{col}"/>'
def rect(x, y, w, h, rx=0, col=INK):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{col}"/>'
def svg(inner, w=100, h=100):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'

# ============================================================ RUHEPOSE (Variante B, SOLID)
# Bauart (alle Werte im 100er-Canvas):
#   zentrale Saeule (Torso = Beinspanne): x 41.5-58.5
#   Beine: Mittellinie 45/55, Breite 7 -> Aussenkante 41.5/58.5, Schritt-Spalt ~3, y59-90
#   Torso: gerade Seiten, y30-62 (reicht UNTER den Yoke -> keine Naht in Achselhoehe)
#   Arme:  Mittellinie 37/63, Breite 6.5 -> Spalt zum Torso ~2, y31-57 (enden Huefthoehe)
#   Yoke:  x = Arm-Aussenkante (33.75-66.25), y26-34, rx7
#   Kopf:  Kreis r9 bei (50,14), separat (kein Hals)
# Zeichenreihenfolge: Arme, Beine, Torso, Yoke, Kopf (Ueberlappung deckt Naehte).
RESTING = dict(central=(41.5, 58.5), leg_c=(45, 55), leg_w=7, arm_c=(37, 63), arm_w=6.5,
               torso_y=(30, 62), arm_y=(31, 57), leg_y=(59, 90), yoke_y=(26, 34), yoke_rx=7,
               head_c=(50, 14), head_r=9)

def resting_figure(P=RESTING):
    cx0, cx1 = P["central"]
    ax0 = P["arm_c"][0] - P["arm_w"]/2   # Arm-Aussenkante (=Yoke-Aussenkante)
    parts = [
        cap((P["arm_c"][0], P["arm_y"][0]), (P["arm_c"][0], P["arm_y"][1]), P["arm_w"]),
        cap((P["arm_c"][1], P["arm_y"][0]), (P["arm_c"][1], P["arm_y"][1]), P["arm_w"]),
        cap((P["leg_c"][0], P["leg_y"][0]), (P["leg_c"][0], P["leg_y"][1]), P["leg_w"]),
        cap((P["leg_c"][1], P["leg_y"][0]), (P["leg_c"][1], P["leg_y"][1]), P["leg_w"]),
        rect(cx0, P["torso_y"][0], cx1 - cx0, P["torso_y"][1] - P["torso_y"][0]),
        rect(ax0, P["yoke_y"][0], (100 - ax0) - ax0, P["yoke_y"][1] - P["yoke_y"][0], P["yoke_rx"]),
        circ(P["head_c"], P["head_r"]),
    ]
    return svg("".join(parts))

# ==================================================== KEYLINE fuer kreuzende Arme (Prototyp)
# Weisse Kontur AUSSEN ums Glied, nur an den Laengskanten + Handkappe, quert nie die Breite,
# stoppt frueh (Wurzel bleibt verbunden), runder Stopp. Kein spitzer Taper in den Torso.
def _side_edge(ttr, off, side):
    def nrm(t): return (-t[1]*side, t[0]*side)
    E = []; segs = list(zip(ttr[:-1], ttr[1:]))
    for i, (a, b) in enumerate(segs):
        n = nrm(U(a, b))
        if i == 0: E.append((a[0]+n[0]*off, a[1]+n[1]*off))
        E.append((b[0]+n[0]*off, b[1]+n[1]*off))
        if i+1 < len(segs):
            n2 = nrm(U(b, segs[i+1][1])); a0 = math.atan2(n[1], n[0]); a1 = math.atan2(n2[1], n2[0])
            d = (a1-a0+math.pi) % (2*math.pi) - math.pi
            if d*side > 0:
                for k in range(1, 7): aa = a0 + d*k/7; E.append((b[0]+math.cos(aa)*off, b[1]+math.sin(aa)*off))
    return E
def _trunc(E, u):
    Le = sum(math.hypot(E[i+1][0]-E[i][0], E[i+1][1]-E[i][1]) for i in range(len(E)-1)) or 1e-9
    out = [E[0]]; acc = 0
    for i in range(1, len(E)):
        dd = math.hypot(E[i][0]-E[i-1][0], E[i][1]-E[i-1][1])
        if acc+dd > Le*u:
            t = (Le*u-acc)/dd; out.append((E[i-1][0]+(E[i][0]-E[i-1][0])*t, E[i-1][1]+(E[i][1]-E[i-1][1])*t)); break
        acc += dd; out.append(E[i])
    return out
def _tip_arc(tip, pL, off, tipdir, n=9):
    aL = math.atan2(pL[1]-tip[1], pL[0]-tip[0]); ta = aL + math.pi/2
    dot = math.cos(ta)*tipdir[0] + math.sin(ta)*tipdir[1]; sweep = math.pi if dot > 0 else -math.pi
    return [(tip[0]+math.cos(aL+sweep*i/n)*off, tip[1]+math.sin(aL+sweep*i/n)*off) for i in range(1, n)]
def keyline_out(root_to_tip, w, k=2.2, u_stop=0.85, margin=0.35):
    """Weisse Kontur ums Glied root_to_tip=[wurzel,...,hand]. u_stop: Bruchteil Richtung Wurzel
    (Arm ~0.82, Bein ~0.9). Auf dem ink-Glied (das VOR dem Koerper liegt) ZULETZT zeichnen."""
    ttr = root_to_tip[::-1]; off = w/2 + k/2 + margin; tip = ttr[0]; tipdir = U(ttr[1], ttr[0])
    L = _trunc(_side_edge(ttr, off, +1), u_stop); R = _trunc(_side_edge(ttr, off, -1), u_stop)
    path = L[::-1] + _tip_arc(tip, L[0], off, tipdir) + R
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in path)
    return f'<path d="{d}" fill="none" stroke="{WHITE}" stroke-width="{f(k)}" stroke-linecap="round" stroke-linejoin="round"/>'

# =============================================================== REQUISITEN (Prototyp, roh)
def prop_drill(wrist, fa):
    """Rote Pistolen-Bohrmaschine. fa = Bohrrichtung (0=oben,90=rechts)."""
    def P(p, l, a): return pt(p, l, a)
    gt = P(wrist, 8, fa-68); bb = P(gt, 5, fa+180); bf = P(gt, 10, fa)
    ch = P(bf, 2.5, fa); bit = P(bf, 8, fa)
    return "".join([
        cap(wrist, gt, 6.5, RED), cap(bb, bf, 9, RED),
        cap(bf, ch, 5.5, INK), cap(ch, bit, 2.2, INK)])
def prop_martini(wrist, fa):
    def P(l, a): return pt(wrist, l, a)
    top = P(13, fa); st = P(6, fa); rL = pt(top, 7, fa-90); rR = pt(top, 7, fa+90)
    fL = pt(wrist, 4, fa-90); fR = pt(wrist, 4, fa+90); ol = P(4.5, fa)
    return "".join([
        cap(wrist, st, 2.2, INK), cap(fL, fR, 2.2, INK),
        f'<path d="M{f(rL[0])} {f(rL[1])} L{f(rR[0])} {f(rR[1])} L{f(st[0])} {f(st[1])} Z" fill="{INK}"/>',
        circ(ol, 1.7, RED)])

# ============================================ POSIERBARE KAPSEL-FIGUR mit Keyline (Prototyp)
# Hinweis: nutzt (noch) KEINEN Ruhe-Spalt. Vereinheitlichung Ruhe/Kreuz = naechster Schritt.
AW, LW = 6.5, 8.0
def joints(armL, armR, legL, legR):
    shL, shR = (36, 32), (64, 32); hipL, hipR = (45, 59), (55, 59)
    elL = pt(shL, 15, armL[0]); wrL = pt(elL, 14, armL[1]); elR = pt(shR, 15, armR[0]); wrR = pt(elR, 14, armR[1])
    knL = pt(hipL, 18, legL[0]); anL = pt(knL, 18, legL[1]); knR = pt(hipR, 18, legR[0]); anR = pt(knR, 18, legR[1])
    return dict(armL=[shL, elL, wrL], armR=[shR, elR, wrR], legL=[hipL, knL, anL], legR=[hipR, knR, anR])
def pose_figure(j, order, prop=None):
    body = rect(41.5, 30, 17, 32) + rect(33.75, 26, 32.5, 8, 7)
    limbs = "".join(cap(j[k][0], j[k][1], AW if 'arm' in k else LW) + cap(j[k][1], j[k][2], AW if 'arm' in k else LW)
                    for k in ['armL', 'armR', 'legL', 'legR'])
    ustop = {'armL': 0.82, 'armR': 0.82, 'legL': 0.9, 'legR': 0.9}
    keys = "".join(keyline_out(j[k], AW if 'arm' in k else LW, u_stop=ustop[k]) for k in order)
    ps = ""
    if prop:
        name, side, ang = prop; wr = j['armR' if side == 'R' else 'armL'][2]
        ps = {'drill': prop_drill, 'martini': prop_martini}[name](wr, ang)
    return svg(limbs + body + circ((50, 14), 9) + keys + ps)


if __name__ == "__main__":
    # Demo: Ruhepose + posierte Figuren nebeneinander -> demo.html
    rest = resting_figure()
    drill = pose_figure(joints((205, 222), (118, 100), (188, 182), (172, 170)),
                        ['legL', 'legR', 'armL', 'armR'], prop=('drill', 'R', 108))
    martini = pose_figure(joints((198, 205), (150, 120), (184, 184), (176, 176)),
                          ['legL', 'legR', 'armL', 'armR'], prop=('martini', 'R', 25))
    cells = [("Ruhepose (solid)", rest), ("gebeugt + Bohrer (Prototyp)", drill), ("Martini (Prototyp)", martini)]
    row = "".join(f'<div style="text-align:center"><div style="width:200px;height:200px;border:1px solid #ccc;background:#fff">'
                  f'<div style="width:200px;height:200px">{s}</div></div><div style="font:600 12px system-ui;color:#666;margin-top:4px">{l}</div></div>'
                  for l, s in cells)
    html = ('<!doctype html><meta charset=utf-8><style>svg{width:200px;height:200px}</style>'
            f'<body style="margin:0;background:#EFEEE8;padding:20px"><div style="display:flex;gap:18px">{row}</div>')
    with open("demo.html", "w") as fh:
        fh.write(html)
    print("wrote demo.html")
