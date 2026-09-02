#!/usr/bin/env python3
"""
Consolidamento serale — eseguito dal cron alle 23:00, indipendentemente dalle sessioni.

  1. legge stato/giornata.md (il buffer riempito durante il giorno)
  2. fa avanzare stato/tracker.md secondo i marcatori CHIUSO / RIPASSO trovati
  3. appende una riga a log/giornate.md — anche per i giorni vuoti
  4. archivia il buffer e lo azzera
  5. rigenera stato/briefing.md

Gira anche quando non è stata aperta nessuna sessione: un giorno senza studio è un
dato, non un buco. Il piano prevede che una settimana vuota vada compensata entro le
due successive, e questo è il file che lo rende verificabile.

Marcatori riconosciuti dentro stato/giornata.md (case-insensitive):
    CHIUSO <CODICE> <modulo>            → entra nel tracker al primo gradino
    RIPASSO <CODICE> <modulo> ok        → avanza di un gradino
    RIPASSO <CODICE> <modulo> debole    → arretra di un gradino (non azzera)
"""

from __future__ import annotations

import datetime as dt
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402  — risoluzione della radice, unico punto che conosce i percorsi

ROOT = paths.root()

GIORNATA = os.path.join(ROOT, "stato", "giornata.md")
TRACKER = os.path.join(ROOT, "stato", "tracker.md")
GIORNATE = os.path.join(ROOT, "log", "giornate.md")
ARCHIVIO = os.path.join(ROOT, "log", "giornate_dettaglio")

GRADINI = [3, 7, 14, 30, 90]

TODAY = dt.date.today()

HEADER = (
    "# Tracker ripasso\n\n"
    "> Mantenuto da `scripts/giornata.py`. Intervalli: 3 → 7 → 14 → 30 → 90 giorni.\n"
    "> Se lo stato diverge dalla realtà, vince la realtà: correggi e annota in `stato/giornata.md`.\n\n"
    "| Codice | Modulo | Chiuso | Ultimo ripasso | Gradino | Prossimo |\n"
    "|---|---|---|---|---|---|\n"
)

RE_CHIUSO = re.compile(r"\bCHIUSO\s+([A-Z0-9]{2,6})\s+(\S+)", re.IGNORECASE)
RE_RIPASSO = re.compile(r"\bRIPASSO\s+([A-Z0-9]{2,6})\s+(\S+)\s+(ok|debole)\b", re.IGNORECASE)


def read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def load_tracker() -> dict[tuple[str, str], dict]:
    rows: dict[tuple[str, str], dict] = {}
    for line in read(TRACKER).splitlines():
        line = line.strip()
        if not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6 or cells[0].lower() in ("codice", "code"):
            continue
        try:
            gradino = int(cells[4])
        except ValueError:
            gradino = GRADINI[0]
        rows[(cells[0].upper(), cells[1])] = {
            "codice": cells[0].upper(),
            "modulo": cells[1],
            "chiuso": cells[2],
            "ultimo": cells[3],
            "gradino": gradino,
            "prossimo": cells[5],
        }
    return rows


def next_step(current: int, direction: str) -> int:
    try:
        idx = GRADINI.index(current)
    except ValueError:
        idx = 0
    if direction == "avanti":
        idx = min(idx + 1, len(GRADINI) - 1)
    else:
        idx = max(idx - 1, 0)
    return GRADINI[idx]


def write_tracker(rows: dict[tuple[str, str], dict]) -> None:
    ordered = sorted(rows.values(), key=lambda r: (r["prossimo"], r["codice"], r["modulo"]))
    body = "".join(
        "| {codice} | {modulo} | {chiuso} | {ultimo} | {gradino} | {prossimo} |\n".format(**r)
        for r in ordered
    )
    os.makedirs(os.path.dirname(TRACKER), exist_ok=True)
    with open(TRACKER, "w", encoding="utf-8") as fh:
        fh.write(HEADER + body)


def apply_markers(buffer_text: str, rows: dict[tuple[str, str], dict]) -> list[str]:
    """Applica CHIUSO e RIPASSO al tracker. Ritorna le note per il log giornaliero."""
    note: list[str] = []

    for codice, modulo in RE_CHIUSO.findall(buffer_text):
        key = (codice.upper(), modulo)
        prossimo = TODAY + dt.timedelta(days=GRADINI[0])
        rows[key] = {
            "codice": codice.upper(),
            "modulo": modulo,
            "chiuso": TODAY.isoformat(),
            "ultimo": "—",
            "gradino": GRADINI[0],
            "prossimo": prossimo.isoformat(),
        }
        note.append(f"chiuso {codice.upper()} {modulo}")

    for codice, modulo, esito in RE_RIPASSO.findall(buffer_text):
        key = (codice.upper(), modulo)
        row = rows.get(key)
        if row is None:
            # Ripasso di un modulo mai registrato come chiuso: lo si accoglie comunque,
            # perché rifiutarlo silenziosamente è il modo migliore per perdere il dato.
            row = {
                "codice": codice.upper(),
                "modulo": modulo,
                "chiuso": "—",
                "ultimo": "—",
                "gradino": GRADINI[0],
                "prossimo": "",
            }
            rows[key] = row
        direction = "avanti" if esito.lower() == "ok" else "indietro"
        row["gradino"] = next_step(row["gradino"], direction)
        row["ultimo"] = TODAY.isoformat()
        row["prossimo"] = (TODAY + dt.timedelta(days=row["gradino"])).isoformat()
        note.append(f"ripasso {codice.upper()} {modulo} ({esito.lower()})")

    return note


def scaduti(rows: dict[tuple[str, str], dict]) -> int:
    count = 0
    for row in rows.values():
        try:
            if dt.date.fromisoformat(row["prossimo"]) < TODAY:
                count += 1
        except (ValueError, TypeError):
            continue
    return count


def append_giornate(eventi: int, note: list[str], arretrati: int) -> None:
    os.makedirs(os.path.dirname(GIORNATE), exist_ok=True)
    if not os.path.exists(GIORNATE):
        with open(GIORNATE, "w", encoding="utf-8") as fh:
            fh.write("# Giornate\n\n> Una riga per giorno, giorni vuoti inclusi. Append-only.\n\n")

    esistente = read(GIORNATE)
    if f"- **{TODAY.isoformat()}**" in esistente:
        return  # già consolidata: il cron non deve duplicare

    if eventi == 0 and not note:
        riga = f"- **{TODAY.isoformat()}** · nessuna attività registrata"
    else:
        pezzi = [f"{eventi} eventi"]
        if note:
            pezzi.append("; ".join(note[:4]))
        riga = f"- **{TODAY.isoformat()}** · " + " · ".join(pezzi)

    if arretrati:
        riga += f" · ripassi arretrati: {arretrati}"

    with open(GIORNATE, "a", encoding="utf-8") as fh:
        fh.write(riga + "\n")


def archive_and_clear(buffer_text: str) -> None:
    if buffer_text.strip():
        os.makedirs(ARCHIVIO, exist_ok=True)
        dest = os.path.join(ARCHIVIO, f"{TODAY.isoformat()}.md")
        with open(dest, "a", encoding="utf-8") as fh:
            fh.write(buffer_text.rstrip() + "\n")
    os.makedirs(os.path.dirname(GIORNATA), exist_ok=True)
    with open(GIORNATA, "w", encoding="utf-8") as fh:
        fh.write(
            f"# Giornata {(TODAY + dt.timedelta(days=1)).isoformat()}\n\n"
            "<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.\n"
            "     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->\n\n"
        )


def main() -> int:
    buffer_text = read(GIORNATA)
    eventi = len(re.findall(r"^\d{2}:\d{2}", buffer_text, re.MULTILINE))

    rows = load_tracker()
    note = apply_markers(buffer_text, rows)
    write_tracker(rows)

    append_giornate(eventi, note, scaduti(rows))
    archive_and_clear(buffer_text)

    briefing = os.path.join(ROOT, "scripts", "briefing.py")
    if os.path.exists(briefing):
        subprocess.run(
            [sys.executable, briefing],
            env={**os.environ, "UNICODE_ROOT": ROOT},
            check=False,
            capture_output=True,
        )

    print(f"giornata {TODAY}: {eventi} eventi, {len(note)} movimenti sul tracker", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
