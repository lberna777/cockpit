#!/usr/bin/env python3
"""recap_generator.py — genera recap/YYYY-MM-DD.md a fatti grezzi + sintesi Ollama.

Lazy/idempotente: genera il recap di un giorno solo se ci sono attività e il file
non esiste già. Pensato per essere chiamato all'avvio (dall'app o da un wrapper),
NON da cron a orario fisso (che perderebbe i job a macchina spenta).

Uso:
  recap_generator.py            # recap di OGGI
  recap_generator.py 2026-06-16 # recap di un giorno specifico
  recap_generator.py --backfill 7  # genera i recap mancanti degli ultimi 7 giorni
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

HOME = Path.home()
VAULT = HOME / "cockpit" / "Vault"
RECAP_DIR = VAULT / "recap"
ATTIVITA = VAULT / "attivita_oggi.md"
IDEE = HOME / "Idee"
OLLAMA_MODEL = "llama3.2:3b"


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 30) -> str:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return ""


def git_repos(base: Path) -> list[Path]:
    return [p for p in base.iterdir() if p.is_dir() and (p / ".git").exists()]


def collect_git(day: date) -> list[str]:
    """Commit del giorno su tutti i repo in ~/Sviluppo."""
    since = day.isoformat()
    until = (day + timedelta(days=1)).isoformat()
    out: list[str] = []
    for repo in git_repos(IDEE):
        log = run(["git", "log", f"--since={since} 00:00",
                   f"--until={until} 00:00", "--pretty=format:%h %s"], cwd=repo)
        if log:
            out.append(f"**{repo.name}**:")
            out.extend(f"  - {line}" for line in log.splitlines())
    return out


def collect_usage(day: date) -> str:
    """Costo/token del giorno da ccusage --json."""
    raw = run(["ccusage", "daily", "--json"], timeout=60)
    if not raw:
        return ""
    try:
        data = json.loads(raw)
        for entry in data.get("daily", []):
            if entry.get("period") == day.isoformat():
                cost = entry.get("totalCost", "?")
                if isinstance(cost, (int, float)):
                    cost = f"{cost:.2f}"
                inp = entry.get("inputTokens", "?")
                out = entry.get("outputTokens", "?")
                return f"Claude usage: ${cost} · in {inp} tok · out {out} tok"
    except (json.JSONDecodeError, AttributeError, TypeError):
        pass
    return ""


def collect_attivita(day: date) -> list[str]:
    """Righe annotate a mano (solo per il giorno corrente)."""
    if day != date.today() or not ATTIVITA.exists():
        return []
    lines = []
    for line in ATTIVITA.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith(">"):
            lines.append(f"  - {s.lstrip('- ')}")
    return lines


def ollama_summary(facts: str) -> str:
    """Sintesi breve via Ollama. Fallback marcato se ollama assente/errore."""
    prompt = (
        "Riassumi in 2-4 bullet concisi in italiano la giornata di lavoro descritta "
        "da questi fatti grezzi. Non inventare nulla, attieniti ai fatti.\n\n" + facts
    )
    try:
        r = subprocess.run(["ollama", "run", OLLAMA_MODEL], input=prompt,
                           capture_output=True, text=True, timeout=120)
        s = ANSI_RE.sub("", r.stdout).strip()
        return s if s else "_(sintesi non disponibile)_"
    except (subprocess.SubprocessError, OSError):
        return "_(ollama non disponibile — solo fatti grezzi)_"


def generate(day: date, force: bool = False) -> str | None:
    RECAP_DIR.mkdir(parents=True, exist_ok=True)
    target = RECAP_DIR / f"{day.isoformat()}.md"
    if target.exists() and not force:
        return None  # idempotente

    git_facts = collect_git(day)
    usage = collect_usage(day)
    attivita = collect_attivita(day)

    if not git_facts and not usage and not attivita:
        return None  # nessuna attività → niente recap

    facts_blocks = []
    if git_facts:
        facts_blocks.append("### Commit\n" + "\n".join(git_facts))
    if attivita:
        facts_blocks.append("### Attività annotate\n" + "\n".join(attivita))
    if usage:
        facts_blocks.append("### Claude\n" + usage)
    facts = "\n\n".join(facts_blocks)

    summary = ollama_summary(facts)

    content = (
        f"# Recap {day.isoformat()}\n\n"
        f"## FATTI (verbatim)\n\n{facts}\n\n"
        f"## SINTESI <!-- ollama -->\n\n{summary}\n"
    )
    target.write_text(content, encoding="utf-8")

    # Resetta attivita_oggi.md per il giorno successivo
    if day == date.today() and ATTIVITA.exists():
        tomorrow = day + timedelta(days=1)
        ATTIVITA.write_text(
            f"# Attività — {tomorrow.isoformat()}\n\n"
            "> Annota qui durante il giorno cosa fai. Il recap notturno legge questo file.\n"
            "> Una riga per attività. Verrà archiviato dopo la generazione del recap.\n\n",
            encoding="utf-8",
        )

    return str(target)


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--backfill":
        n = int(args[1]) if len(args) > 1 else 7
        today = date.today()
        made = []
        for i in range(1, n + 1):
            res = generate(today - timedelta(days=i))
            if res:
                made.append(res)
        print(f"backfill: {len(made)} recap generati")
        for m in made:
            print(f"  {m}")
        return

    day = datetime.strptime(args[0], "%Y-%m-%d").date() if args else date.today()
    res = generate(day)
    if res:
        print(f"recap scritto: {res}")
    else:
        print(f"recap {day.isoformat()}: già presente o nessuna attività")


if __name__ == "__main__":
    main()
