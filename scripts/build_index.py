#!/usr/bin/env python3
"""build_index.py — genera ~/cockpit/Vault/index.md

Indice compatto (path + titolo) di tutte le note .md del vault, raggruppate per
cartella di primo livello. NON usa LLM. È l'artefatto leggero che il SessionStart
hook inietta in contesto. Segue il symlink UniCode con profondità limitata.
"""
from __future__ import annotations
import os
from pathlib import Path
from datetime import date

VAULT = Path.home() / "cockpit" / "Vault"
INDEX = VAULT / "index.md"

# cartelle/segmenti da escludere ovunque nel path
EXCLUDE_DIRS = {".obsidian", "graphify-out", "_archive", "node_modules",
                ".git", "claudeAppunti_PDF", "SLIDE LAB", "SLIDE TEORIA"}
MAX_DEPTH = 4          # profondità massima sotto il vault (UniCode è grande)
MAX_ENTRIES = 800      # cap di sicurezza sul numero di note


def first_title(md: Path) -> str:
    """Titolo della nota: name/title del frontmatter, o prima riga '# ...',
    o primo testo non vuoto. Salta il blocco frontmatter YAML."""
    try:
        with md.open("r", encoding="utf-8", errors="ignore") as f:
            lines = [next(f, "") for _ in range(40)]
    except OSError:
        return md.stem.replace("_", " ")[:80]

    i = 0
    # salta frontmatter YAML (--- ... ---), catturando name/title se presenti
    if lines and lines[0].strip() == "---":
        fm_title = ""
        for j in range(1, len(lines)):
            s = lines[j].strip()
            if s == "---":
                i = j + 1
                break
            for key in ("title:", "name:"):
                if s.lower().startswith(key):
                    fm_title = s[len(key):].strip().strip('"\'')
        if fm_title:
            return fm_title[:80]
    for line in lines[i:]:
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()[:80]
        if s:
            return s[:80]
    return md.stem.replace("_", " ")[:80]


def walk_vault() -> dict[str, list[tuple[str, str]]]:
    """Ritorna {gruppo_primo_livello: [(relpath, titolo), ...]}."""
    groups: dict[str, list[tuple[str, str]]] = {}
    count = 0
    for root, dirs, files in os.walk(VAULT, followlinks=True):
        rootp = Path(root)
        rel = rootp.relative_to(VAULT)
        depth = len(rel.parts)
        if depth > MAX_DEPTH:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            if fn == "index.md" and rootp == VAULT:
                continue
            p = rootp / fn
            relpath = p.relative_to(VAULT).as_posix()
            group = rel.as_posix() if rel.parts else "(root)"
            groups.setdefault(group, []).append((relpath, first_title(p)))
            count += 1
            if count >= MAX_ENTRIES:
                return groups
    return groups


def main() -> None:
    groups = walk_vault()
    total = sum(len(v) for v in groups.values())
    lines = [
        f"# Vault Index — {date.today().isoformat()}",
        "",
        f"> Indice compatto generato da `build_index.py`. {total} note. "
        "Per il contenuto, apri la nota indicata.",
        "",
    ]
    for group in sorted(groups):
        entries = sorted(groups[group])
        lines.append(f"## {group}  ({len(entries)})")
        for relpath, title in entries:
            name = Path(relpath).name
            lines.append(f"- [[{relpath}|{name}]] — {title}")
        lines.append("")
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    size = INDEX.stat().st_size
    print(f"index.md scritto: {total} note, {size} byte ({size/1024:.1f} KB)")
    if size > 60_000:
        print("WARN: index.md > 60KB — valuta di alzare EXCLUDE_DIRS o abbassare MAX_DEPTH")


if __name__ == "__main__":
    main()
