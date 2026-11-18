#!/usr/bin/env python3
"""Disegni SVG del cheatsheet e del prontuario di CALC.

Rigenerabili: `python3 genera_svg.py` scrive gli .svg in questa cartella.
Stessi colori dei PDF grafici (scripts/pdf_grafico/stile.css):
blu = regola/CPU, verde = esempio/dato, arancio = attenzione, viola = bit di firma/CS.
Ogni disegno ha un fondo bianco, così si legge anche nel tema scuro di Obsidian.
"""
from pathlib import Path

QUI = Path(__file__).parent
TESTO, TENUE, LINEA = "#1d2330", "#5b6475", "#c9d0dc"
BLU, BLU_C = "#2457c5", "#eaf0fd"
VERDE, VERDE_C = "#1f8a5b", "#e7f6ee"
ARANCIO, ARANCIO_C = "#c46a12", "#fdf1e3"
VIOLA, VIOLA_C = "#6b3fb8", "#f1ebfb"
GRIGIO_C = "#f2f3f6"
SANS = "Inter, 'Liberation Sans', 'DejaVu Sans', sans-serif"
MONO = "'JetBrains Mono', 'DejaVu Sans Mono', monospace"


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    def rect(self, x, y, w, h, fill="#fff", stroke=LINEA, r=6, sw=1.2, extra=""):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
                      f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def text(self, x, y, s, size=13, fill=TESTO, anchor="middle", weight=400, mono=False, italic=False):
        fam = MONO if mono else SANS
        st = ' font-style="italic"' if italic else ""
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.p.append(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
                      f'text-anchor="{anchor}" font-weight="{weight}"{st}>{s}</text>')

    def line(self, x1, y1, x2, y2, stroke=TENUE, sw=1.5, arrow=False, dash=False, color_marker=None):
        m = f' marker-end="url(#f{(color_marker or stroke).lstrip("#")})"' if arrow else ""
        d = ' stroke-dasharray="4 3"' if dash else ""
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
                      f'stroke-width="{sw}"{m}{d}/>')

    def path(self, d, stroke=TENUE, sw=1.5, arrow=False, fill="none", dash=False):
        m = f' marker-end="url(#f{stroke.lstrip("#")})"' if arrow else ""
        da = ' stroke-dasharray="4 3"' if dash else ""
        self.p.append(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"{m}{da}/>')

    def save(self, nome):
        colori = {TENUE, BLU, VERDE, ARANCIO, VIOLA, TESTO}
        marker = "".join(
            f'<marker id="f{c.lstrip("#")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for c in colori)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="{self.w}" height="{self.h}"><defs>{marker}</defs>'
               f'<rect width="{self.w}" height="{self.h}" fill="#ffffff" rx="10"/>'
               + "".join(self.p) + "</svg>\n")
        (QUI / nome).write_text(svg, encoding="utf-8")
        print("✔", nome)


# ---------------------------------------------------------------- 1. una cifra = 4 bit
def cifre_bit():
    s = Svg(780, 200)
    s.text(20, 28, "Un indirizzo DLX: 32 bit = 8 cifre esadecimali, ogni cifra = 4 bit",
           14, anchor="start", weight=700)
    cifre = "80000000"
    x0, cw, gap = 20, 88, 5
    for i, c in enumerate(cifre):
        x = x0 + i * (cw + gap)
        prima = i == 0
        s.rect(x, 44, cw, 40, fill=VIOLA_C if prima else BLU_C, stroke=VIOLA if prima else BLU)
        s.text(x + cw / 2, 72, c, 22, weight=700, mono=True, fill=VIOLA if prima else BLU)
        bits = format(int(c, 16), "04b")
        for j, b in enumerate(bits):
            bx = x + j * (cw / 4)
            s.rect(bx + 2, 96, cw / 4 - 4, 28, fill="#fff" if b == "0" else ARANCIO_C,
                   stroke=ARANCIO if b == "1" else LINEA, r=3)
            s.text(bx + cw / 8, 115, b, 14, mono=True, weight=700 if b == "1" else 400,
                   fill=ARANCIO if b == "1" else TENUE)
        alto = 31 - 4 * i
        s.text(x + 2, 142, f"BA{alto}", 10, anchor="start", fill=TENUE, mono=True)
        s.text(x + cw - 2, 142, f"BA{alto - 3}", 10, anchor="end", fill=TENUE, mono=True)
    s.text(20, 172, "80000000h = 1000 0000 … 0000: è a 1 solo BA31, il primo bit della prima cifra.",
           12, anchor="start", fill=TESTO)
    s.text(20, 190, "Pesi dentro ogni cifra, da sinistra: 8 4 2 1.   Prima cifra = BA31..BA28, ultima = BA3..BA0.",
           12, anchor="start", fill=TENUE)
    s.save("cifre_bit.svg")


# ---------------------------------------------------------------- 2. il giro dello zero
def nastro_zero():
    s = Svg(780, 300)
    s.text(20, 28, "Sotto lo zero si ricomincia dal numero più grande", 14, anchor="start", weight=700)
    celle = ["FFFFFFF0", "FFFFFFF1", "…", "FFFFFFFE", "FFFFFFFF", "00000000", "00000001"]
    x0, cw, y = 20, 102, 150
    pos = {}
    for i, c in enumerate(celle):
        x = x0 + i * (cw + 4)
        pos[c] = x + cw / 2
        if c == "…":
            s.text(x + cw / 2, y + 26, "… 12 caselle …", 11, fill=TENUE)
            continue
        zero = c == "00000000"
        meta = c == "FFFFFFF0"
        fill = VERDE_C if zero else (ARANCIO_C if meta else BLU_C)
        st = VERDE if zero else (ARANCIO if meta else BLU)
        s.rect(x, y, cw, 40, fill=fill, stroke=st)
        s.text(x + cw / 2, y + 26, c, 13.5, mono=True, weight=700, fill=st)
    # giro tra FFFFFFFF e 00000000
    xg = x0 + 5 * (cw + 4) - 2
    s.line(xg, y - 14, xg, y + 54, stroke=ARANCIO, sw=2, dash=True)
    s.text(xg, y + 70, "qui il conto «gira»", 11, fill=ARANCIO, weight=600)
    # archi: −1 e −16
    z = pos["00000000"]
    s.path(f"M{z},{y - 4} C{z},{y - 34} {pos['FFFFFFFF']},{y - 34} {pos['FFFFFFFF']},{y - 6}",
           stroke=BLU, arrow=True)
    s.text((z + pos["FFFFFFFF"]) / 2, y - 30, "−1", 13, fill=BLU, weight=700)
    s.path(f"M{z},{y - 6} C{z},{y - 100} {pos['FFFFFFF0']},{y - 100} {pos['FFFFFFF0']},{y - 6}",
           stroke=ARANCIO, sw=2, arrow=True)
    s.text((z + pos["FFFFFFF0"]) / 2, y - 80, "−10h  (16 passi indietro)", 13.5, fill=ARANCIO, weight=700)
    s.text((z + pos["FFFFFFF0"]) / 2, y - 62, "SUBI R22,R0,0x0010   →   R22 = FFFFFFF0h", 12.5,
           fill=TESTO, mono=True)
    # contachilometri
    yc = 248
    s.text(20, yc, "Come il contachilometri a 4 cifre:", 12, anchor="start", fill=TENUE)
    for i, (num, col) in enumerate([("0000", VERDE), ("9999", BLU)]):
        x = 250 + i * 190
        s.rect(x, yc - 20, 96, 30, fill="#222833", stroke="#222833", r=4)
        s.text(x + 48, yc + 1, num, 17, mono=True, fill="#ffffff", weight=700)
    s.line(352, yc - 5, 434, yc - 5, stroke=BLU, arrow=True)
    s.text(393, yc - 12, "−1 km", 11, fill=BLU, weight=600)
    s.text(552, yc, "in esadecimale la cifra più grande è F, non 9", 12, anchor="start", fill=TENUE)
    s.text(20, 285, "Quanti passi? Da 00000000 a FFFFFFF0 mancano 10h = 16: il primo passo porta a FFFFFFFF, gli altri 15 scendono fino a F0.",
           11.5, anchor="start", fill=TESTO)
    s.save("nastro_zero.svg")


# ---------------------------------------------------------------- 3. riporto e prestito
def riporto_prestito():
    s = Svg(780, 290)
    cw = 40

    def colonna(x0, y, cifre, col=TESTO, peso=400):
        for i, c in enumerate(cifre):
            s.text(x0 + i * cw + cw / 2, y, c, 22, mono=True, fill=col, weight=peso)

    # somma
    s.rect(10, 10, 370, 270, fill=VERDE_C, stroke=VERDE_C, r=10)
    s.text(30, 38, "Somma: il riporto scatta a 16", 14, anchor="start", weight=700, fill=VERDE)
    x0 = 120
    s.text(x0 - 30, 110, "", 18)
    s.text(x0 + 0 * cw + cw / 2, 72, "1", 14, fill=ARANCIO, weight=700, mono=True)
    s.path(f"M{x0 + 1 * cw + cw / 2},{80} C{x0 + 1 * cw + 10},{60} {x0 + cw / 2 + 10},{60} {x0 + cw / 2 + 6},{66}",
           stroke=ARANCIO, arrow=True)
    colonna(x0, 110, "2800")
    s.text(x0 - 22, 145, "+", 22, mono=True)
    colonna(x0, 145, "0800")
    s.line(x0 - 30, 158, x0 + 4 * cw + 6, 158, stroke=TESTO, sw=1.5)
    colonna(x0, 190, "3000", col=VERDE, peso=700)
    s.text(30, 225, "colonna del 8:  8 + 8 = 16 = 10h", 12, anchor="start", mono=True)
    s.text(30, 243, "→ scrivi 0, porta 1 a sinistra (non 16)", 12, anchor="start")
    s.text(30, 265, "colonna del 2:  2 + 0 + 1 = 3", 12, anchor="start", mono=True)

    # sottrazione
    s.rect(400, 10, 370, 270, fill=ARANCIO_C, stroke=ARANCIO_C, r=10)
    s.text(420, 38, "Sottrazione: il prestito vale 16", 14, anchor="start", weight=700, fill=ARANCIO)
    x1 = 510
    # cifre corrette sopra
    s.text(x1 + 1 * cw + cw / 2, 72, "0", 13, fill=ARANCIO, weight=700, mono=True)
    s.text(x1 + 2 * cw + cw / 2, 72, "F", 13, fill=ARANCIO, weight=700, mono=True)
    s.text(x1 + 3 * cw + cw / 2, 72, "16", 13, fill=ARANCIO, weight=700, mono=True)
    colonna(x1, 110, "0100")
    for i in (1, 2, 3):
        if i < 3:
            s.line(x1 + i * cw + 10, 104, x1 + i * cw + cw - 10, 92, stroke=ARANCIO, sw=1.6)
    s.text(x1 - 22, 145, "−", 22, mono=True)
    colonna(x1, 145, "0014")
    s.line(x1 - 30, 158, x1 + 4 * cw + 6, 158, stroke=TESTO, sw=1.5)
    colonna(x1, 190, "00EC", col=VERDE, peso=700)
    s.text(420, 222, "0 − 4 non si può: chiedi in prestito a sinistra.", 12, anchor="start")
    s.text(420, 239, "Lo 0 non ha niente: chiede all'1 → 1 diventa 0,", 12, anchor="start")
    s.text(420, 256, "lo 0 diventa F, l'ultima colonna 16 − 4 = 12 = C.", 12, anchor="start")
    s.text(420, 273, "F − 1 = E.  ✘ 16/11: 00FC (la F non scesa a E)", 12, anchor="start",
           fill=ARANCIO, weight=600)
    s.save("riporto_prestito.svg")


# ---------------------------------------------------------------- 4. mappa a 16 tacche
def mappa_blocchi():
    s = Svg(780, 250)
    s.text(20, 26, "La linea degli indirizzi: 16 tacche, una per valore della prima cifra hex (prova 2025-01-08)",
           13, anchor="start", weight=700)
    x0, W, y, h = 20, 740, 90, 46
    t = W / 16
    blocchi = [  # (inizio, fine) in sedicesimi
        (0, 4, "EPROM 1 GB", BLU, BLU_C),
        (4, 6, "EPROM 512 MB", BLU, BLU_C),
        (6, 6.25, "", BLU, BLU_C),
        (7, 8, "", VIOLA, VIOLA_C),
        (8, 16, "RAM 2 GB", VERDE, VERDE_C),
    ]
    s.rect(x0, y, W, h, fill=GRIGIO_C, stroke=LINEA, r=4)
    for a, b, nome, st, fi in blocchi:
        s.rect(x0 + a * t, y, (b - a) * t, h, fill=fi, stroke=st, r=3)
        if nome:
            s.text(x0 + (a + b) / 2 * t, y + 28, nome, 13, fill=st, weight=700)
    s.text(x0 + 6.6 * t, y + 23, "libero", 11, fill=TENUE)
    s.text(x0 + 6.6 * t, y + 37, "(buco)", 10, fill=TENUE)
    s.text(x0 + 6.12 * t, y - 26, "EPROM 64 MB", 11, fill=BLU, weight=700)
    s.line(x0 + 6.12 * t, y - 22, x0 + 6.12 * t, y - 2, stroke=BLU, arrow=True)
    s.text(x0 + 7.5 * t, y - 26, "porta (tutta 7…)", 11, fill=VIOLA, weight=700)
    s.line(x0 + 7.5 * t, y - 22, x0 + 7.5 * t, y - 2, stroke=VIOLA, arrow=True)
    for i in range(17):
        x = x0 + i * t
        s.line(x, y + h, x, y + h + 8, stroke=TENUE, sw=1)
        if i < 16:
            s.text(x + t / 2, y + h + 22, f"{i:X}", 13, mono=True, weight=700, fill=TESTO)
    s.text(x0, y + h + 40, "prima cifra dell'indirizzo:  0 = 0xxxxxxxh … F = Fxxxxxxxh; ogni tacca = 256 MB = 10000000h",
           11.5, anchor="start", fill=TENUE)
    # inizio/fine
    s.text(x0, 212, "inizio + taglia = primo fuori   →   fine = primo fuori − 1", 12.5, anchor="start",
           weight=700, fill=BLU)
    s.text(x0, 232, "40000000h + 20000000h = 60000000h  →  fine 5FFFFFFFh          RAM in alto: FFFFFFFFh − 80000000h + 1 = 80000000h (inizio)",
           11, anchor="start", mono=True)
    s.save("mappa_blocchi.svg")


# ---------------------------------------------------------------- 5. i tre campi dell'indirizzo
def campi_indirizzo():
    s = Svg(780, 250)
    s.text(20, 26, "Dove va ogni bit di BA: esempio blocco da 512 MB (2^29) in 4 banchi da 128 MB (2^27)",
           13, anchor="start", weight=700)
    x0, W, y, h = 20, 740, 60, 44
    b = W / 32
    campi = [(31, 29, "firma", VIOLA, VIOLA_C), (28, 2, "cella dentro il banco", BLU, BLU_C),
             (1, 0, "", ARANCIO, ARANCIO_C)]
    for alto, basso, nome, st, fi in campi:
        xa = x0 + (31 - alto) * b
        w = (alto - basso + 1) * b
        s.rect(xa, y, w, h, fill=fi, stroke=st, r=3)
        if nome:
            s.text(xa + w / 2, y + 27, nome, 13, fill=st, weight=700)
        s.text(xa + 2, y + h + 15, f"BA{alto}", 10, anchor="start", mono=True, fill=TENUE)
        if alto != basso:
            s.text(xa + w - 2, y + h + 15, f"BA{basso}", 10, anchor="end", mono=True, fill=TENUE)
    # frecce
    yb = 190
    def box(cx, testo1, testo2, st, fi, w=210):
        s.rect(cx - w / 2, yb, w, 48, fill=fi, stroke=st)
        s.text(cx, yb + 20, testo1, 12.5, fill=st, weight=700)
        s.text(cx, yb + 38, testo2, 11, fill=TESTO, mono=True)
    cx1 = x0 + 1.5 * b
    cx2 = x0 + 16.5 * b
    cx3 = x0 + 31 * b
    s.line(cx1, y + h + 22, 120, yb - 2, stroke=VIOLA, arrow=True)
    box(120, "P2 · nel CS", "CS = BA31*·BA30·BA29*·BEi", VIOLA, VIOLA_C, 220)
    s.line(cx2, y + h + 22, cx2, yb - 2, stroke=BLU, arrow=True)
    box(cx2, "P3 · ai piedini del banco", "A[26..0] ← BA[28..2]", BLU, BLU_C, 230)
    s.line(cx3, y + h + 22, 650, yb - 2, stroke=ARANCIO, arrow=True)
    box(650, "non escono dal DLX", "al loro posto BE0..BE3", ARANCIO, ARANCIO_C, 200)
    s.text(20, 168, "3 + 27 + 2 = 32 fili: se il conto non torna, un bit è finito nel campo sbagliato.",
           12, anchor="start", fill=TESTO)
    s.save("campi_indirizzo.svg")


# ---------------------------------------------------------------- 6. il banco, quattro lati
def banco():
    s = Svg(780, 330)
    s.text(20, 26, "P3 · un banco di memoria: i quattro lati da collegare, sempre uguali", 13,
           anchor="start", weight=700)
    cx, cy, cw, ch = 300, 50, 200, 180
    s.rect(cx, cy, cw, ch, fill=GRIGIO_C, stroke=TESTO, sw=1.6, r=8)
    s.text(cx + cw / 2, cy + ch - 14, "banco i  (2^k byte)", 12, fill=TENUE, weight=600)
    pins = [("CS", "CS_X_i", VIOLA, "da P2: firma · BEi"),
            ("A[k−1..0]", "BA[k+1..2]", BLU, "si parte da BA2"),
            ("OE", "MEMRD", VERDE, "leggi"),
            ("WE", "MEMWR", ARANCIO, "scrivi · solo RAM")]
    for i, (pin, filo, col, nota) in enumerate(pins):
        y = cy + 30 + i * 36
        s.text(cx + 10, y + 5, pin, 13, anchor="start", mono=True, weight=700, fill=col)
        s.line(cx - 150, y, cx - 2, y, stroke=col, sw=2, arrow=True)
        s.text(cx - 155, y + 5, filo, 13, anchor="end", mono=True, weight=700, fill=col)
        s.text(cx - 76, y - 6, nota, 10.5, fill=TENUE)
    # dati
    yd = cy + 84
    s.text(cx + cw - 10, yd + 5, "D[7..0]", 13, anchor="end", mono=True, weight=700, fill=TESTO)
    s.line(cx + cw + 4, yd, cx + cw + 130, yd, stroke=TESTO, sw=2, arrow=True)
    s.line(cx + cw + 128, yd, cx + cw + 6, yd, stroke=TESTO, sw=2, arrow=True)
    s.text(cx + cw + 136, yd + 5, "BD[8i+7..8i]", 13, anchor="start", mono=True, weight=700)
    s.text(cx + cw + 67, yd - 8, "8 fili", 10.5, fill=TENUE)
    # bus dati
    yb = 262
    s.text(20, yb - 8, "Bus dati a 32 bit: ogni banco ha la sua fetta di 8 fili", 12, anchor="start", weight=600)
    fette = [("banco 3", "BD31..24"), ("banco 2", "BD23..16"), ("banco 1", "BD15..8"), ("banco 0", "BD7..0")]
    for i, (n, f) in enumerate(fette):
        x = 20 + i * 185
        s.rect(x, yb, 180, 50, fill=BLU_C if i % 2 else VERDE_C, stroke=BLU if i % 2 else VERDE)
        s.text(x + 90, yb + 21, n, 12.5, weight=700, fill=BLU if i % 2 else VERDE)
        s.text(x + 90, yb + 40, f, 12, mono=True)
    s.save("banco.svg")


# ---------------------------------------------------------------- 7. foglio in quattro riquadri
def foglio_4():
    s = Svg(780, 300)
    s.text(20, 26, "Il foglio d'esame in quattro riquadri", 13, anchor="start", weight=700)
    q = [("①  Dati", ["dal testo: taglie, porte, registri", "fissi DLX: 32 bit, 4 banchi,",
                      "BA1–0 → BE, EPROM solo lettura"], BLU, BLU_C),
         ("②  Linea degli indirizzi", ["16 tacche = prima cifra hex", "EPROM dal basso, RAM in alto,",
                                       "porte nel buco"], VERDE, VERDE_C),
         ("③  Tabella della risposta", ["una riga per blocco: taglia, inizio–fine,", "firma, CS, banco 2^k, piedini, WR?",
                                        "poi CS_…_i = CS · BEi"], VIOLA, VIOLA_C),
         ("④  Controlli", ["somme e 8 cifre", "bit che cambiano = esponente", "CS a coppie, repliche in zone libere"],
          ARANCIO, ARANCIO_C)]
    for i, (tit, righe, st, fi) in enumerate(q):
        x = 20 + (i % 2) * 375
        y = 40 + (i // 2) * 128
        s.rect(x, y, 365, 118, fill=fi, stroke=st, sw=1.5, r=8)
        s.text(x + 14, y + 26, tit, 14, anchor="start", weight=700, fill=st)
        for j, r in enumerate(righe):
            s.text(x + 14, y + 52 + j * 20, r, 12, anchor="start")
    s.save("foglio_4.svg")


# ---------------------------------------------------------------- 8. load e store
def load_store():
    s = Svg(780, 250)
    s.text(20, 26, "Load e store: tra parentesi c'è l'indirizzo base, prima della virgola il dato", 13,
           anchor="start", weight=700)

    def riga(y, istr, verso_load):
        s.text(20, y + 30, istr, 15, anchor="start", mono=True, weight=700, fill=BLU if verso_load else ARANCIO)
        # calcolo indirizzo
        s.rect(250, y + 8, 170, 36, fill=GRIGIO_C, stroke=LINEA)
        s.text(335, y + 31, "R20 + 0x0004", 13, mono=True)
        s.line(422, y + 26, 478, y + 26, stroke=TENUE, arrow=True)
        s.text(450, y + 18, "indirizzo", 10, fill=TENUE)
        # memoria
        s.rect(480, y, 120, 52, fill=VERDE_C, stroke=VERDE)
        s.text(540, y + 22, "memoria", 11, fill=VERDE, weight=600)
        s.text(540, y + 40, "60000004h", 12, mono=True)
        # registro
        s.rect(650, y + 8, 110, 36, fill=BLU_C if verso_load else ARANCIO_C, stroke=BLU if verso_load else ARANCIO)
        s.text(705, y + 31, "R21", 14, mono=True, weight=700)
        if verso_load:
            s.line(602, y + 26, 648, y + 26, stroke=BLU, sw=2.2, arrow=True)
        else:
            s.line(648, y + 26, 602, y + 26, stroke=ARANCIO, sw=2.2, arrow=True)

    riga(48, "LBU R21,0x0004(R20)", True)
    s.text(20, 122, "L = Load: dalla memoria al registro (R21 riceve)", 12, anchor="start", fill=BLU, weight=600)
    riga(140, "SB  R21,0x0004(R20)", False)
    s.text(20, 214, "S = Store: dal registro alla memoria (R21 dà)", 12, anchor="start", fill=ARANCIO, weight=600)
    s.text(20, 238, "Con R20 = 60000000h. «Valore o indirizzo» non è del registro: lo decide la posizione nell'istruzione.",
           11.5, anchor="start", fill=TENUE)
    s.save("load_store.svg")


# ---------------------------------------------------------------- 9. LB e LBU
def lb_lbu():
    s = Svg(780, 230)
    s.text(20, 26, "LBU e LB leggono lo stesso byte: cambia con cosa riempiono i 24 bit alti", 13,
           anchor="start", weight=700)

    def reg(x, y, byte_alti, col_alti, fi_alti):
        for i, v in enumerate(byte_alti + ["F0"]):
            ultimo = i == 3
            s.rect(x + i * 62, y, 58, 34, fill=GRIGIO_C if ultimo else fi_alti,
                   stroke=TESTO if ultimo else col_alti, r=3)
            s.text(x + i * 62 + 29, y + 23, v, 15, mono=True, weight=700, fill=TESTO if ultimo else col_alti)

    # byte in memoria
    s.rect(20, 70, 120, 60, fill=VERDE_C, stroke=VERDE)
    s.text(80, 92, "byte in memoria", 11, fill=VERDE, weight=600)
    s.text(80, 117, "F0", 18, mono=True, weight=700)
    s.text(80, 150, "1111 0000", 13, mono=True)
    s.rect(31, 137, 12, 18, fill="none", stroke=ARANCIO, sw=1.8, r=2)
    s.text(37, 170, "bit 7 = 1", 11, fill=ARANCIO, weight=700)
    s.line(142, 90, 238, 66, stroke=TENUE, arrow=True)
    s.line(142, 112, 238, 150, stroke=TENUE, arrow=True)
    s.text(248, 54, "LBU", 15, anchor="start", mono=True, weight=700, fill=BLU)
    reg(300, 40, ["00", "00", "00"], TENUE, "#ffffff")
    s.text(560, 62, "zeri: «unsigned»", 12, anchor="start", fill=BLU, weight=600)
    s.text(248, 160, "LB", 15, anchor="start", mono=True, weight=700, fill=ARANCIO)
    reg(300, 145, ["FF", "FF", "FF"], ARANCIO, ARANCIO_C)
    s.text(560, 160, "copie del bit 7: «signed»", 12, anchor="start", fill=ARANCIO, weight=600)
    s.text(560, 177, "bit 7 = 0 (byte 00..7F) → 00 come LBU", 11, anchor="start", fill=TENUE)
    s.text(20, 215, "F0 letto unsigned = 240; letto signed = −16. Il testo dice quale: «byte unsigned» → LBU, «byte signed» → LB.",
           11.5, anchor="start")
    s.save("lb_lbu.svg")


# ---------------------------------------------------------------- 10. LHI
def lhi():
    s = Svg(780, 170)
    s.text(20, 26, "LHI: il numero va nella metà alta, la metà bassa diventa 0 (sempre)", 13,
           anchor="start", weight=700)

    def reg(y, alta, bassa, nota, col_b):
        s.rect(260, y, 160, 36, fill=VIOLA_C, stroke=VIOLA, r=3)
        s.text(340, y + 24, alta, 16, mono=True, weight=700, fill=VIOLA)
        s.rect(424, y, 160, 36, fill="#fff" if bassa == "0000" else VERDE_C, stroke=col_b, r=3)
        s.text(504, y + 24, bassa, 16, mono=True, weight=700, fill=col_b)
        s.text(600, y + 23, nota, 11.5, anchor="start", fill=TENUE)

    s.text(20, 66, "LHI R20,0x8000", 14, anchor="start", mono=True, weight=700, fill=VIOLA)
    reg(42, "8000", "0000", "R20 = 80000000h", TENUE)
    s.text(340, 96, "metà alta (16 bit)", 10.5, fill=VIOLA)
    s.text(504, 96, "metà bassa", 10.5, fill=TENUE)
    s.text(20, 136, "ORI R20,R20,0x0010", 14, anchor="start", mono=True, weight=700, fill=VERDE)
    reg(112, "8000", "0010", "R20 = 80000010h", VERDE)
    s.text(20, 164, "Qualunque cosa ci fosse prima in R20, dopo LHI la metà bassa è 0000.", 11.5, anchor="start", fill=TENUE)
    s.save("lhi.svg")


# ---------------------------------------------------------------- 11. lo scheletro dell'handler
def handler():
    s = Svg(780, 330)
    s.text(20, 26, "P8 · lo scheletro dell'handler", 13, anchor="start", weight=700)

    def nodo(x, y, w, testo, nota="", col=BLU, fi=BLU_C, rombo=False):
        if rombo:
            cx, cy = x + w / 2, y + 26
            s.path(f"M{cx},{y} L{x + w},{cy} L{cx},{y + 52} L{x},{cy} Z", stroke=col, fill=fi, sw=1.4)
            s.text(cx, cy + 5, testo, 12.5, mono=True, weight=700, fill=col)
        else:
            s.rect(x, y, w, 40, fill=fi, stroke=col)
            s.text(x + w / 2, y + 25, testo, 12.5, mono=True, weight=700, fill=col)
        if nota:
            s.text(x + w + 10, y + 25, nota, 11, anchor="start", fill=TENUE)

    nodo(40, 44, 220, "interrupt", "il DLX salta all'handler", TESTO, GRIGIO_C)
    s.line(150, 86, 150, 100, arrow=True)
    nodo(40, 102, 220, "LHI R20,base", "base delle porte (metà alta)")
    s.line(150, 144, 150, 158, arrow=True)
    nodo(40, 160, 220, "LBU R21,stato(R20)", "chi ha chiamato?")
    s.line(150, 202, 150, 214, arrow=True)
    nodo(40, 216, 220, "BEQZ R21,RAMO_2", "", ARANCIO, ARANCIO_C, rombo=True)
    # rami
    s.line(150, 270, 150, 284, arrow=True)
    s.text(160, 281, "≠ 0", 11, anchor="start", fill=TENUE)
    nodo(40, 286, 220, "ramo 1 … RFE", "", VERDE, VERDE_C)
    s.path("M260,242 L420,242 L420,284", arrow=True)
    s.text(340, 236, "= 0 → salta", 11, fill=TENUE)
    nodo(310, 286, 220, "RAMO_2: … RFE", "", VERDE, VERDE_C)
    s.rect(560, 110, 200, 150, fill=GRIGIO_C, stroke=LINEA)
    s.text(575, 134, "Dentro ogni ramo", 12, anchor="start", weight=700)
    for j, r in enumerate(["L dalla porta → registro", "S registro → indirizzo", "     del testo",
                           "RFE alla fine: torna al", "     programma interrotto"]):
        s.text(575, 158 + j * 20, r, 11.5, anchor="start")
    s.save("handler.svg")


if __name__ == "__main__":
    for f in (cifre_bit, nastro_zero, riporto_prestito, mappa_blocchi, campi_indirizzo, banco,
              foglio_4, load_store, lb_lbu, lhi, handler):
        f()
