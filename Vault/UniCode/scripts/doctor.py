#!/usr/bin/env python3
"""
Diagnostica dell'ambiente UniCode.

Non modifica niente. Ispeziona l'albero reale e stampa un referto compatto, pensato
per essere incollato in chat: dice dove si trova la radice, cosa c'è, cosa manca,
cosa è rimasto della struttura precedente e se gli automatismi sono agganciati.

    python3 scripts/doctor.py

Serve esattamente quando la struttura del laptop è cambiata e va riallineata.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

ROOT = paths.root()

ATTESI_DIR = ["profilo", "stato", "log", "corsi", "piano", "plans/handoffs", "scripts"]
ATTESI_FILE = [
    "CLAUDE.md",
    "profilo/studente.md",
    "profilo/errori.md",
    "stato/corrente.md",
    "stato/giornata.md",
    "stato/tracker.md",
    "piano/codici.txt",
    "scripts/paths.py",
    "scripts/briefing.py",
    "scripts/giornata.py",
    "scripts/session_start.sh",
    "scripts/session_end.sh",
]
GENERATI = ["stato/briefing.md"]

# Residui della struttura precedente → destinazione suggerita.
LEGACY = {
    "stato/errori_frequenti.md": "confluito in profilo/errori.md → archiviare in log/",
    "stato/tracker_ripasso.md": "sostituito da stato/tracker.md → archiviare in log/",
    "stato/log_sessioni.md": "diventa log/AAAA-MM.md",
    "stato/percorso.md": "da spezzare in corsi/<CODICE>/percorso.md",
    "master_map_studio.md": "legacy dichiarato obsoleto già nella versione precedente",
    "metodo_studio_esami_pratici.md": "confluito in CLAUDE.md §7.2-7.3 → archiviare",
    "claudeLezioni": "diventa corsi/<CODICE>/lezioni/",
    "claudeAppunti": "diventa corsi/<CODICE>/appunti/",
    "APPUNTI GREZZI": "diventa corsi/<CODICE>/grezzi/",
    "SLIDE TEORIA": "diventa corsi/<CODICE>/materiali/",
    "SLIDE LAB": "diventa corsi/<CODICE>/materiali/",
    "SIMULAZIONI ESAMI": "diventa corsi/<CODICE>/prove/",
    "RIPASSO DIRITTO": "diventa corsi/<CODICE>/appunti/ (corso chiuso: archiviare)",
    "esercizi": "diventa corsi/<CODICE>/prove/ o /materiali/",
    "ESAMI SCELTI.md": "sostituito da piano/piano_laurea.md",
}

# Percorsi che i comandi non dovrebbero più citare.
PATTERN_VECCHI = [
    "stato/errori_frequenti",
    "stato/tracker_ripasso",
    "stato/log_sessioni",
    "claudeLezioni",
    "claudeAppunti",
    "APPUNTI GREZZI",
    "SLIDE TEORIA",
    "SLIDE LAB",
    "SIMULAZIONI ESAMI",
    "master_map_studio",
    "corrente.md",
]

OK, KO, WARN = "  ok  ", " MANCA", " NOTA "


def riga(stato: str, testo: str, nota: str = "") -> str:
    return f"[{stato}] {testo}" + (f"  — {nota}" if nota else "")


def origine_radice() -> str:
    if os.environ.get("UNICODE_ROOT"):
        return "variabile d'ambiente UNICODE_ROOT"
    if os.path.exists(paths.CONFIG):
        return f"file di configurazione {paths.CONFIG}"
    qui = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.abspath(ROOT) == os.path.abspath(qui):
        return "risalita dalla posizione dello script"
    return "candidato noto o ultima spiaggia"


def sezione(titolo: str) -> None:
    print(f"\n## {titolo}")


def main() -> int:
    print("# Referto ambiente UniCode")
    print(f"\nRadice: `{ROOT}`")
    print(f"Risolta per: {origine_radice()}")
    print(f"Python: {sys.version.split()[0]}")
    if not os.path.isdir(ROOT):
        print("\n**La radice non esiste.** Tutto il resto è privo di senso finché non la si indica:")
        print("  mkdir -p ~/.config/unicode && echo '<percorso reale>' > ~/.config/unicode/root")
        return 1

    sezione("Struttura attesa")
    mancanti = 0
    for d in ATTESI_DIR:
        esiste = os.path.isdir(os.path.join(ROOT, d))
        mancanti += 0 if esiste else 1
        print(riga(OK if esiste else KO, f"{d}/"))
    for f in ATTESI_FILE:
        esiste = os.path.isfile(os.path.join(ROOT, f))
        mancanti += 0 if esiste else 1
        print(riga(OK if esiste else KO, f))
    for f in GENERATI:
        esiste = os.path.isfile(os.path.join(ROOT, f))
        print(riga(OK if esiste else WARN, f, "" if esiste else "generato al primo avvio"))

    sezione("Residui della struttura precedente")
    trovati = False
    for nome, dest in LEGACY.items():
        if os.path.exists(os.path.join(ROOT, nome)):
            trovati = True
            print(riga(WARN, nome, dest))
    if not trovati:
        print("Nessuno. La migrazione risulta completata.")

    sezione("Voci di primo livello non previste")
    previsti = {d.split("/")[0] for d in ATTESI_DIR} | {".claude", ".git", ".gitignore", "README.md"}
    previsti |= {n.split("/")[0] for n in ATTESI_FILE} | set(LEGACY)
    extra = sorted(
        n for n in os.listdir(ROOT)
        if n not in previsti and not n.startswith(".")
    )
    print("\n".join(f"  - {n}" for n in extra) if extra else "Nessuna.")

    sezione("Automatismi")
    settings = os.path.join(ROOT, ".claude", "settings.json")
    if os.path.isfile(settings):
        testo = open(settings, encoding="utf-8", errors="replace").read()
        print(riga(OK if "SessionStart" in testo else KO, "hook SessionStart in .claude/settings.json"))
        print(riga(OK if "SessionEnd" in testo else KO, "hook SessionEnd in .claude/settings.json"))
    else:
        print(riga(KO, ".claude/settings.json assente"))

    try:
        crontab = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5).stdout
    except Exception:
        crontab = ""
    ha_cron = "giornata.py" in crontab
    timer = os.path.expanduser("~/.config/systemd/user/unicode-giornata.timer")
    ha_timer = os.path.exists(timer)
    if ha_cron or ha_timer:
        print(riga(OK, "consolidamento serale", "cron" if ha_cron else "timer systemd"))
    else:
        print(riga(KO, "consolidamento serale", "né cron né timer systemd: il tracker non avanzerà"))

    sezione("Comandi che citano percorsi superati")
    cmd_dir = os.path.join(ROOT, ".claude", "commands")
    if not os.path.isdir(cmd_dir):
        print("Cartella .claude/commands assente.")
    else:
        sporchi = []
        for nome in sorted(os.listdir(cmd_dir)):
            if not nome.endswith(".md"):
                continue
            testo = open(os.path.join(cmd_dir, nome), encoding="utf-8", errors="replace").read()
            hit = sorted({p for p in PATTERN_VECCHI if p in testo})
            if hit:
                sporchi.append((nome, hit))
        if not sporchi:
            print("Nessuno.")
        for nome, hit in sporchi:
            print(riga(WARN, f".claude/commands/{nome}", ", ".join(hit)))

    sezione("Codici corso attivi")
    print(", ".join(paths.codici()))

    sezione("Verdetto")
    if mancanti == 0 and not trovati:
        print("Ambiente allineato.")
    else:
        print(f"{mancanti} elementi attesi mancanti; residui da migrare: {'sì' if trovati else 'no'}.")
    print("\n_Incolla questo referto in chat per il riallineamento._")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
