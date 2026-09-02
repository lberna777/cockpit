#!/usr/bin/env python3
"""
Costruisce stato/briefing.md — l'unico contesto caricato d'ufficio a ogni avvio.

Composizione:
  1. nucleo stabile  — profilo di studio + errori ricorrenti in testa
  2. esame attivo    — stato/corrente.md, troncato
  3. ripassi dovuti  — da stato/tracker.md, calcolati su oggi
  4. ultime giornate — da log/giornate.md, giorni vuoti inclusi

Nessuna dipendenza esterna. Ogni sezione degrada da sola se il file manca.
Invocato da session_end.sh, da giornata.sh e a mano con:  python3 scripts/briefing.py
"""

from __future__ import annotations

import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402  — risoluzione della radice, unico punto che conosce i percorsi

ROOT = paths.root()

PROFILO = os.path.join(ROOT, "profilo", "studente.md")
ERRORI = os.path.join(ROOT, "profilo", "errori.md")
CORRENTE = os.path.join(ROOT, "stato", "corrente.md")
TRACKER = os.path.join(ROOT, "stato", "tracker.md")
GIORNATE = os.path.join(ROOT, "log", "giornate.md")
OUT = os.path.join(ROOT, "stato", "briefing.md")

# Tetti in caratteri: il costo in context window deve restare prevedibile.
CAP_PROFILO = 1800
CAP_ERRORI = 1400
CAP_CORRENTE = 2200
MAX_RIPASSI = 12
MAX_GIORNATE = 3

TODAY = dt.date.today()


def read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def strip_headings(text: str) -> str:
    """Toglie il titolo di primo livello e le righe vuote in eccesso."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    lines = [ln for ln in lines if not ln.startswith("# ")]
    out, blank = [], False
    for ln in lines:
        if not ln.strip():
            if blank:
                continue
            blank = True
        else:
            blank = False
        out.append(ln)
    return "\n".join(out).strip()


def cap(text: str, limit: int) -> str:
    """Tronca su confine di riga, segnalando il troncamento."""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    nl = cut.rfind("\n")
    if nl > limit * 0.6:
        cut = cut[:nl]
    return cut.rstrip() + "\n\n_(troncato — apri il file per il resto)_"


def parse_date(value: str) -> dt.date | None:
    value = value.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def parse_tracker(text: str) -> list[dict]:
    """
    Legge le righe della tabella di stato/tracker.md.
    Colonne attese: Codice | Modulo | Chiuso | Ultimo ripasso | Gradino | Prossimo
    Le righe che non rispettano il formato vengono ignorate senza errore.
    """
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|--") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6:
            continue
        if cells[0].lower() in ("codice", "code"):
            continue
        prossimo = parse_date(cells[5])
        if prossimo is None:
            continue
        rows.append(
            {
                "codice": cells[0],
                "modulo": cells[1],
                "chiuso": cells[2],
                "ultimo": cells[3],
                "gradino": cells[4],
                "prossimo": prossimo,
            }
        )
    return rows


def classify(row: dict) -> tuple[str, int]:
    delta = (row["prossimo"] - TODAY).days
    if delta < 0:
        return "SCADUTO", delta
    if delta <= 3:
        return "DOVUTO", delta
    return "OK", delta


def sezione_ripassi() -> str:
    text = read(TRACKER)
    if not text:
        return "_Nessun tracker: `stato/tracker.md` non esiste ancora._"

    rows = parse_tracker(text)
    if not rows:
        return "_Tracker presente ma vuoto: nessun modulo chiuso finora._"

    dovuti = []
    for row in rows:
        stato, delta = classify(row)
        if stato != "OK":
            dovuti.append((stato, delta, row))

    if not dovuti:
        prossimo = min(rows, key=lambda r: r["prossimo"])
        giorni = (prossimo["prossimo"] - TODAY).days
        return (
            f"Nessun ripasso dovuto. Il prossimo è **{prossimo['codice']} "
            f"{prossimo['modulo']}** fra {giorni} giorni ({prossimo['prossimo']})."
        )

    dovuti.sort(key=lambda item: item[1])
    lines = [f"**{len(dovuti)} ripassi da fare** su {len(rows)} moduli tracciati.", ""]
    lines.append("| Stato | Corso | Modulo | Scadenza |")
    lines.append("|---|---|---|---|")
    for stato, delta, row in dovuti[:MAX_RIPASSI]:
        if delta < 0:
            quando = f"{-delta} gg di ritardo"
        elif delta == 0:
            quando = "oggi"
        else:
            quando = f"fra {delta} gg"
        lines.append(f"| {stato} | {row['codice']} | {row['modulo']} | {quando} |")
    if len(dovuti) > MAX_RIPASSI:
        lines.append(f"\n_...e altri {len(dovuti) - MAX_RIPASSI}. Esegui `/piano` per il quadro completo._")
    return "\n".join(lines)


def sezione_giornate() -> str:
    text = read(GIORNATE)
    if not text:
        return "_Nessuno storico giornaliero._"
    righe = [ln.rstrip() for ln in text.splitlines() if ln.strip().startswith("- ")]
    if not righe:
        return "_Nessuno storico giornaliero._"
    ultime = righe[-MAX_GIORNATE:]
    return "\n".join(ultime)


def sezione(titolo: str, corpo: str) -> str:
    corpo = corpo.strip() or "_(vuoto)_"
    return f"## {titolo}\n\n{corpo}\n"


def build() -> str:
    profilo = cap(strip_headings(read(PROFILO)), CAP_PROFILO)
    errori = cap(strip_headings(read(ERRORI)), CAP_ERRORI)
    corrente = cap(strip_headings(read(CORRENTE)), CAP_CORRENTE)

    parts = [
        f"# Briefing — {TODAY.isoformat()}",
        "",
        "> Generato da `scripts/briefing.py`. **Non modificare a mano**: viene sovrascritto.",
        "> È l'unico contesto caricato d'ufficio. Tutto il resto si carica su necessità.",
        "",
        sezione("Come studia Lorenzo", profilo or "_Profilo non ancora compilato._"),
        sezione("Errori ricorrenti da intercettare", errori or "_Nessun pattern registrato._"),
        sezione("Esame attivo", corrente or "_Nessun esame attivo dichiarato._"),
        sezione("Ripassi dovuti", sezione_ripassi()),
        sezione("Ultime giornate", sezione_giornate()),
    ]
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    content = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"briefing aggiornato: {OUT} ({len(content)} caratteri)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
