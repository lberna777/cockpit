#!/usr/bin/env python3
"""link_modules.py — collega le note di studio per chiave-modulo (wikilink Obsidian).

Raggruppa le rappresentazioni parallele dello stesso modulo (lezione / appunti /
speedreview / grezzi) e inserisce in ognuna un blocco "Collegati" con i wikilink
ai fratelli + agli hub della materia.

- Deterministico, nessun costo LLM, nessuna dipendenza.
- Idempotente: il blocco è delimitato da marker AUTO-LINKS e viene rigenerato a ogni run.
- Reversibile: rimuovere i blocchi = una regex sui marker (vedi --strip).

Uso:
    python3 link_modules.py            # DRY-RUN: stampa cosa farebbe, non scrive
    python3 link_modules.py --apply    # scrive i blocchi nelle note
    python3 link_modules.py --strip    # rimuove tutti i blocchi AUTO-LINKS
"""
import re
import sys
from pathlib import Path

VAULT = Path.home() / "cockpit" / "Vault" / "UniCode"
START = "<!-- AUTO-LINKS:START -->"
END = "<!-- AUTO-LINKS:END -->"

# hub per materia (basename senza .md; Obsidian risolve per basename)
HUBS = {
    "Diritto": ["master_map_studio", "glossario_diritto", "concept_maps"],
    "SysAdm": ["master_map_studio", "glossario_sysadm", "concept_maps", "troubleshooting_vm", "metodo_studio_esami_pratici"],
    "Security": ["master_map_studio", "concept_maps", "metodo_studio_esami_pratici"],
}


def classify(path: Path):
    """Ritorna (materia, codice_modulo) oppure None se la nota non è un modulo."""
    p = str(path).lower()
    name = path.stem.lower()
    if "diritto" in p:
        m = re.search(r"modulo[_ ]?d0*(\d+)", name) or re.search(r"speedreview_d0*(\d+)", name)
        if m:
            return ("Diritto", f"D{int(m.group(1))}")
    if "sysadm" in p:
        m = re.search(r"modulo[_ ]?(\d[a-d])", name)
        if m:
            return ("SysAdm", m.group(1).upper())
    if "security" in p:
        m = re.search(r"modulo[_ ]?s0*(\d+)", name)
        if m:
            return ("Security", f"S{int(m.group(1))}")
    return None


def strip_block(text: str) -> str:
    return re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n*", "", text, flags=re.DOTALL).rstrip() + "\n"


def build_block(self_stem, siblings, hubs):
    lines = [START, "## 🔗 Collegati", ""]
    for s in siblings:
        lines.append(f"- [[{s}]]")
    if hubs:
        lines.append("")
        lines.append("**Hub:** " + " · ".join(f"[[{h}]]" for h in hubs))
    lines.append(END)
    return "\n".join(lines)


def main():
    apply = "--apply" in sys.argv
    strip = "--strip" in sys.argv

    notes = [f for f in VAULT.rglob("*.md")
             if "/.backups/" not in str(f) and "/.obsidian/" not in str(f) and "/.git/" not in str(f)]

    if strip:
        n = 0
        for f in notes:
            t = f.read_text(encoding="utf-8")
            if START in t:
                f.write_text(strip_block(t), encoding="utf-8")
                n += 1
        print(f"Rimossi blocchi AUTO-LINKS da {n} note.")
        return

    # raggruppa per (materia, codice)
    groups = {}
    for f in notes:
        c = classify(f)
        if c:
            groups.setdefault(c, []).append(f)

    total_links = 0
    for (materia, code), files in sorted(groups.items()):
        stems = sorted(f.stem for f in files)
        print(f"\n### {materia} · modulo {code}  ({len(files)} note)")
        for f in files:
            siblings = [s for s in stems if s != f.stem]
            hubs = HUBS[materia]
            total_links += len(siblings) + len(hubs)
            print(f"  {f.relative_to(VAULT)}")
            for s in siblings:
                print(f"      -> [[{s}]]")
            if apply:
                t = f.read_text(encoding="utf-8")
                t = strip_block(t) if START in t else t.rstrip() + "\n"
                t = t.rstrip() + "\n\n" + build_block(f.stem, siblings, hubs) + "\n"
                f.write_text(t, encoding="utf-8")

    print(f"\n{'APPLICATO' if apply else 'DRY-RUN'}: {len(groups)} moduli, "
          f"{sum(len(v) for v in groups.values())} note, ~{total_links} archi.")
    if not apply:
        print("Per scrivere davvero: python3 link_modules.py --apply")


if __name__ == "__main__":
    main()
