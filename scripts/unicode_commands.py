#!/usr/bin/env python3
"""
Espone in cockpit/.claude/commands i comandi di studio di UniCode (/lab, /chiudi, …).

Ogni comando generato è un rimando, non una copia: dice a Claude di leggere l'originale in
Vault/UniCode/.claude/commands/ e di eseguirlo risolvendo i percorsi relativi rispetto a
Vault/UniCode. Così la fonte resta una sola e modificare un comando non richiede di
rigenerare nulla; serve rilanciare questo script solo quando un comando viene aggiunto,
rinominato o tolto, o ne cambiano description / argument-hint.

Uso:  python3 scripts/unicode_commands.py
"""

from __future__ import annotations

import os
import re

COCKPIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORGENTE = os.path.join(COCKPIT, "Vault", "UniCode", ".claude", "commands")
DESTINAZIONE = os.path.join(COCKPIT, ".claude", "commands")
MARCATORE = "<!-- generato da scripts/unicode_commands.py: non modificare a mano -->"

RE_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

CORPO = """{marcatore}

Comando di studio lanciato da `~/cockpit`. La radice di UniCode è `Vault/UniCode`
(nel cloud anche `~/UniCode`): **tutti i percorsi relativi** dell'originale — `stato/`,
`corsi/`, `piano/`, `profilo/`, `log/`, `scripts/` — si risolvono rispetto a quella cartella,
e i comandi di shell che li usano vanno eseguiti da lì (`cd Vault/UniCode` o percorso completo).

1. Se in questa sessione non hai ancora letto `Vault/UniCode/CLAUDE.md`, leggilo per intero.
2. Leggi `Vault/UniCode/.claude/commands/{nome}.md` ed eseguilo alla lettera, con argomenti:
   `$ARGUMENTS`
3. Le trascrizioni delle sessioni lanciate da cockpit stanno sotto la cartella di progetto di
   cockpit in `~/.claude/projects/` (nel cloud: `-home-user-cockpit`), non sotto quella di
   UniCode: cercale in entrambe quando l'originale le chiede.
4. Nel cloud non c'è Eclipse: i progetti Java si consegnano a Lorenzo come zip importabile
   (*File → Import → Existing Projects into Workspace → Select archive file*) e si compilano
   qui con `javac` per verificarli.
"""


def main() -> int:
    os.makedirs(DESTINAZIONE, exist_ok=True)
    generati = set()
    for nome_file in sorted(os.listdir(SORGENTE)):
        if not nome_file.endswith(".md"):
            continue
        nome = nome_file[:-3]
        with open(os.path.join(SORGENTE, nome_file), encoding="utf-8") as fh:
            testo = fh.read()
        m = RE_FRONTMATTER.match(testo)
        frontmatter = f"---\n{m.group(1)}\n---\n\n" if m else ""
        destinazione = os.path.join(DESTINAZIONE, nome_file)
        if os.path.exists(destinazione):
            with open(destinazione, encoding="utf-8") as fh:
                if MARCATORE not in fh.read():
                    print(f"saltato {nome_file}: esiste già in cockpit e non è generato")
                    continue
        with open(destinazione, "w", encoding="utf-8") as fh:
            fh.write(frontmatter + CORPO.format(marcatore=MARCATORE, nome=nome))
        generati.add(nome_file)
        print(f"/{nome}")

    # Comandi tolti da UniCode: si rimuove il rimando, solo se generato da qui.
    for nome_file in os.listdir(DESTINAZIONE):
        percorso = os.path.join(DESTINAZIONE, nome_file)
        if nome_file.endswith(".md") and nome_file not in generati:
            with open(percorso, encoding="utf-8") as fh:
                if MARCATORE in fh.read():
                    os.remove(percorso)
                    print(f"rimosso {nome_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
