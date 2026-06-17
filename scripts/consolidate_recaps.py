#!/usr/bin/env python3
"""consolidate_recaps.py — fonde e pota i recap giornalieri (anti-deriva).

Legge i recap giornalieri di un periodo, fonde i blocchi FATTI (verbatim, senza
ulteriore compressione LLM dei fatti), produce un recap consolidato di periodo con
una sintesi Ollama, e archivia i giornalieri consolidati in recap/_archive/.

Uso:
  consolidate_recaps.py --week        # ultimi 7 giorni
  consolidate_recaps.py --month       # ultimi 30 giorni
  consolidate_recaps.py --days 14
  consolidate_recaps.py --week --no-archive
"""
from __future__ import annotations
import argparse
import re
import subprocess
from datetime import date, timedelta
from pathlib import Path

HOME = Path.home()
RECAP_DIR = HOME / "cockpit" / "Vault" / "recap"
ARCHIVE = RECAP_DIR / "_archive"
OLLAMA_MODEL = "llama3.2:3b"
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
DAILY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


def daily_files(since: date, until: date) -> list[Path]:
    out = []
    for p in sorted(RECAP_DIR.glob("20*.md")):
        if not DAILY_RE.match(p.name):
            continue
        d = date.fromisoformat(p.stem)
        if since <= d <= until:
            out.append(p)
    return out


def extract_facts(md: Path) -> str:
    """Estrae il blocco FATTI da un recap giornaliero."""
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"## FATTI.*?\n(.*?)(?=\n## SINTESI|\Z)", text, re.DOTALL)
    return (m.group(1).strip() if m else text.strip())


def ollama_summary(facts: str, period_label: str) -> str:
    prompt = (
        f"Questi sono i fatti grezzi di lavoro del periodo {period_label}. "
        "Scrivi una sintesi in italiano (5-8 bullet) dei temi e risultati principali. "
        "Attieniti ai fatti, non inventare.\n\n" + facts
    )
    try:
        r = subprocess.run(["ollama", "run", OLLAMA_MODEL], input=prompt,
                           capture_output=True, text=True, timeout=180)
        s = ANSI_RE.sub("", r.stdout).strip()
        return s if s else "_(sintesi non disponibile)_"
    except (subprocess.SubprocessError, OSError):
        return "_(ollama non disponibile)_"


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--week", action="store_true")
    g.add_argument("--month", action="store_true")
    g.add_argument("--days", type=int)
    ap.add_argument("--no-archive", action="store_true")
    args = ap.parse_args()

    n = 7 if args.week else 30 if args.month else (args.days or 7)
    until = date.today()
    since = until - timedelta(days=n)
    label = f"{since.isoformat()} → {until.isoformat()}"

    files = daily_files(since, until)
    if not files:
        print(f"nessun recap giornaliero nel periodo {label}")
        return

    merged_facts = "\n\n".join(f"#### {f.stem}\n{extract_facts(f)}" for f in files)
    summary = ollama_summary(merged_facts, label)

    out = RECAP_DIR / f"_consolidato_{since.isoformat()}_{until.isoformat()}.md"
    out.write_text(
        f"# Consolidato {label}\n\n"
        f"> Fonde {len(files)} recap giornalieri. Anti-deriva: i FATTI restano verbatim.\n\n"
        f"## SINTESI PERIODO <!-- ollama -->\n\n{summary}\n\n"
        f"## FATTI AGGREGATI (verbatim)\n\n{merged_facts}\n",
        encoding="utf-8",
    )
    print(f"consolidato scritto: {out} ({len(files)} giornalieri)")

    if not args.no_archive:
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        for f in files:
            f.rename(ARCHIVE / f.name)
        print(f"archiviati {len(files)} giornalieri in {ARCHIVE}")


if __name__ == "__main__":
    main()
