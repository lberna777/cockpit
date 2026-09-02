#!/usr/bin/env python3
"""
Risoluzione della radice UniCode e dei codici corso.

Esiste perché la struttura del laptop può cambiare — ed è cambiata almeno una volta.
Nessun altro script deve contenere un percorso assoluto: tutti passano di qui.

Ordine di risoluzione della radice, primo che vince:
  1. variabile d'ambiente  UNICODE_ROOT
  2. file di configurazione ~/.config/unicode/root   (una riga, il percorso)
  3. risalita dalla posizione di questo script (…/scripts/paths.py → …)
  4. candidati noti: ~/UniCode, ~/cockpit/Vault/UniCode, ~/Università/UniCode, ~/uni/UniCode
  5. ~/UniCode come ultima spiaggia

I codici corso si leggono da  piano/codici.txt  (una riga per corso: CODICE  Nome esteso).
Se il file manca si usa la lista di riserva, ma il file ha sempre la precedenza: è lì che
si aggiunge o si rinomina un corso senza toccare il codice degli script.
"""

from __future__ import annotations

import os

CONFIG = os.path.expanduser("~/.config/unicode/root")

CANDIDATI = [
    "~/UniCode",
    "~/cockpit/Vault/UniCode",
    "~/Università/UniCode",
    "~/Universita/UniCode",
    "~/uni/UniCode",
    "~/Documenti/UniCode",
]

# Riserva: usata solo se piano/codici.txt non esiste.
CODICI_RISERVA = [
    "FI2", "CALC", "MATAP", "LAS", "SO", "IDS",
    "TLC", "ELT", "CA", "RETI", "WEB", "ELN",
]

MARCATORI = ("CLAUDE.md", "stato", "profilo")


def _plausibile(path: str) -> bool:
    """Una radice è plausibile se contiene almeno uno dei marcatori attesi."""
    return os.path.isdir(path) and any(
        os.path.exists(os.path.join(path, m)) for m in MARCATORI
    )


def root() -> str:
    env = os.environ.get("UNICODE_ROOT")
    if env:
        return os.path.abspath(os.path.expanduser(env))

    try:
        with open(CONFIG, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    return os.path.abspath(os.path.expanduser(line))
    except OSError:
        pass

    qui = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _plausibile(qui):
        return qui

    for cand in CANDIDATI:
        expanded = os.path.abspath(os.path.expanduser(cand))
        if _plausibile(expanded):
            return expanded

    return os.path.abspath(os.path.expanduser("~/UniCode"))


def p(*parts: str) -> str:
    return os.path.join(root(), *parts)


def codici() -> list[str]:
    """Codici corso da piano/codici.txt, con riserva cablata."""
    path = p("piano", "codici.txt")
    out: list[str] = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                out.append(line.split()[0].upper())
    except OSError:
        return list(CODICI_RISERVA)
    return out or list(CODICI_RISERVA)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "codici":
        print("|".join(codici()))
    else:
        print(root())
