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

La data di riferimento non è il giorno in cui lo script gira, ma quella scritta
nell'intestazione del buffer (`# Giornata AAAA-MM-GG`): il portatile alle 23:00 può
essere spento, e il recupero arriva giorni dopo. Se il consolidamento è in ritardo,
i giorni interposti vengono riempiti come vuoti — che è esattamente il dato che
servirebbe perdere di meno.

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

# Tetto al riempimento retroattivo: oltre questo, il consolidamento non è in ritardo,
# è stato spento. Riempire trecento righe non informa nessuno.
MAX_GIORNI_VUOTI = 45

# Ora prima della quale la giornata di oggi non si chiude. Il recupero di un giorno
# arretrato parte all'accensione, a qualsiasi ora: senza questa soglia chiuderebbe
# anche la giornata in corso, e gli eventi scritti nel pomeriggio troverebbero la riga
# di oggi già presente in log/giornate.md e andrebbero persi. Si scavalca con --force.
ORA_CHIUSURA = 22

HEADER = (
    "# Tracker ripasso\n\n"
    "> Mantenuto da `scripts/giornata.py`. Intervalli: 3 → 7 → 14 → 30 → 90 giorni.\n"
    "> Se lo stato diverge dalla realtà, vince la realtà: correggi e annota in `stato/giornata.md`.\n\n"
    "| Codice | Modulo | Chiuso | Ultimo ripasso | Gradino | Prossimo |\n"
    "|---|---|---|---|---|---|\n"
)

RE_CHIUSO = re.compile(r"\bCHIUSO\s+([A-Z0-9]{2,6})\s+(\S+)", re.IGNORECASE)
RE_RIPASSO = re.compile(r"\bRIPASSO\s+([A-Z0-9]{2,6})\s+(\S+)\s+(ok|debole)\b", re.IGNORECASE)
RE_INTESTAZIONE = re.compile(r"^#\s*Giornata\s+(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def giorno_del_buffer(text: str) -> dt.date:
    """
    La giornata che il buffer sta raccogliendo, letta dalla sua intestazione.

    Ricadute previste, tutte verso una data che esiste davvero:
      - intestazione assente o illeggibile → oggi;
      - intestazione nel futuro (buffer aperto ieri sera per oggi, oppure residuo
        della versione che scriveva domani) → oggi, perché una giornata futura non
        si può consolidare.
    """
    m = RE_INTESTAZIONE.search(text)
    if not m:
        return TODAY
    try:
        giorno = dt.date.fromisoformat(m.group(1))
    except ValueError:
        return TODAY
    return min(giorno, TODAY)


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


def apply_markers(buffer_text: str, rows: dict[tuple[str, str], dict], giorno: dt.date) -> list[str]:
    """
    Applica CHIUSO e RIPASSO al tracker. Ritorna le note per il log giornaliero.

    Le scadenze si calcolano dal giorno in cui il modulo è stato effettivamente
    chiuso o ripassato, non dal giorno in cui il consolidamento gira: un ripasso
    fatto il 2 e consolidato il 14 scade tre giorni dopo il 2.
    """
    note: list[str] = []

    for codice, modulo in RE_CHIUSO.findall(buffer_text):
        key = (codice.upper(), modulo)
        prossimo = giorno + dt.timedelta(days=GRADINI[0])
        rows[key] = {
            "codice": codice.upper(),
            "modulo": modulo,
            "chiuso": giorno.isoformat(),
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
        row["ultimo"] = giorno.isoformat()
        row["prossimo"] = (giorno + dt.timedelta(days=row["gradino"])).isoformat()
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


def _assicura_giornate() -> None:
    os.makedirs(os.path.dirname(GIORNATE), exist_ok=True)
    if not os.path.exists(GIORNATE):
        with open(GIORNATE, "w", encoding="utf-8") as fh:
            fh.write("# Giornate\n\n> Una riga per giorno, giorni vuoti inclusi. Append-only.\n\n")


def append_giornate(giorno: dt.date, eventi: int, note: list[str], arretrati: int) -> None:
    _assicura_giornate()

    if f"- **{giorno.isoformat()}**" in read(GIORNATE):
        return  # già consolidata: il recupero non deve duplicare

    if eventi == 0 and not note:
        riga = f"- **{giorno.isoformat()}** · nessuna attività registrata"
    else:
        pezzi = [f"{eventi} eventi"]
        if note:
            pezzi.append("; ".join(note[:4]))
        riga = f"- **{giorno.isoformat()}** · " + " · ".join(pezzi)

    if arretrati:
        riga += f" · ripassi arretrati: {arretrati}"

    with open(GIORNATE, "a", encoding="utf-8") as fh:
        fh.write(riga + "\n")


def colma_vuoti(dal_giorno: dt.date) -> int:
    """
    Riempie i giorni fra quello consolidato e ieri: sono giorni in cui il
    consolidamento non è girato, non giorni in cui non è successo niente — ma ai fini
    del piano la differenza non conta, e la riga mancante sì.

    Oggi resta fuori: è ancora in corso, e lo chiuderà il consolidamento di stasera.
    """
    _assicura_giornate()
    esistente = read(GIORNATE)
    righe: list[str] = []
    giorno = dal_giorno + dt.timedelta(days=1)
    while giorno < TODAY and len(righe) < MAX_GIORNI_VUOTI:
        if f"- **{giorno.isoformat()}**" not in esistente:
            righe.append(f"- **{giorno.isoformat()}** · nessuna attività registrata")
        giorno += dt.timedelta(days=1)
    if righe:
        with open(GIORNATE, "a", encoding="utf-8") as fh:
            fh.write("\n".join(righe) + "\n")
    return len(righe)


def archive_and_clear(buffer_text: str, giorno: dt.date, nuovo_giorno: dt.date) -> None:
    if buffer_text.strip():
        os.makedirs(ARCHIVIO, exist_ok=True)
        dest = os.path.join(ARCHIVIO, f"{giorno.isoformat()}.md")
        with open(dest, "a", encoding="utf-8") as fh:
            fh.write(buffer_text.rstrip() + "\n")
    os.makedirs(os.path.dirname(GIORNATA), exist_ok=True)
    with open(GIORNATA, "w", encoding="utf-8") as fh:
        fh.write(
            f"# Giornata {nuovo_giorno.isoformat()}\n\n"
            "<!-- Claude appende qui, una riga per fatto: HH:MM · CODICE · fatto.\n"
            "     Marcatori: CHIUSO <cod> <mod> · RIPASSO <cod> <mod> ok|debole -->\n\n"
        )


def rigenera_briefing() -> None:
    briefing = os.path.join(ROOT, "scripts", "briefing.py")
    if not os.path.exists(briefing):
        return
    subprocess.run(
        [sys.executable, briefing],
        env={**os.environ, "UNICODE_ROOT": ROOT},
        check=False,
        capture_output=True,
    )


def main() -> int:
    forza = "--force" in sys.argv[1:]
    buffer_text = read(GIORNATA)
    giorno = giorno_del_buffer(buffer_text)
    eventi = len(re.findall(r"^\d{2}:\d{2}", buffer_text, re.MULTILINE))

    if giorno == TODAY and dt.datetime.now().hour < ORA_CHIUSURA and not forza:
        rigenera_briefing()
        print(
            f"giornata {giorno} ancora in corso: niente da consolidare "
            f"(chiusura dalle {ORA_CHIUSURA}:00, oppure --force)",
            file=sys.stderr,
        )
        return 0

    rows = load_tracker()
    note = apply_markers(buffer_text, rows, giorno)
    write_tracker(rows)

    append_giornate(giorno, eventi, note, scaduti(rows))
    vuoti = colma_vuoti(giorno)

    # Chiuso il giorno corrente si apre il buffer di domani; recuperato un giorno
    # arretrato si apre quello di oggi, che è ancora da vivere.
    nuovo_giorno = TODAY + dt.timedelta(days=1) if giorno == TODAY else TODAY
    archive_and_clear(buffer_text, giorno, nuovo_giorno)

    rigenera_briefing()

    ritardo = "" if giorno == TODAY else f" (recupero del {giorno}, {vuoti} giorni vuoti colmati)"
    print(
        f"giornata {giorno}: {eventi} eventi, {len(note)} movimenti sul tracker{ritardo}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
