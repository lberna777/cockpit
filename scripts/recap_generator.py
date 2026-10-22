#!/usr/bin/env python3
"""recap_generator.py — genera recap/YYYY-MM-DD.md solo da fatti verificabili.

Rifatto il 2026-10-22 (decisione di Lorenzo: «memoria automatica piccola»). Prima il recap
elencava decine di merge e salvataggi automatici e aggiungeva una sintesi di Ollama
(llama3.2:3b) che inventava; leggeva anche Vault/attivita_oggi.md, che nessuno scriveva più.
Ora contiene solo:
  - lo studio del giorno, da Vault/UniCode/log/giornate_dettaglio/<giorno>.md
    (eventi per corso e moduli chiusi, contati: niente testo generato);
  - i commit che dicono qualcosa, per repo: esclusi merge, salvataggi automatici, tracce e
    consolidamenti, al massimo MAX_COMMIT per repo.

Idempotente: un giorno già scritto non si riscrive (salvo --force), un giorno senza fatti non
produce file. Lo lanciano il timer serale del laptop (giornata_laptop.sh, alle 23) e l'attività
programmata «Memoria notturna» nel cloud (recap_cloud.sh, alle 23:50, anche a laptop spento):
entrambi fanno pull prima e committano dopo, e chi arriva secondo trova il file e lo salta.

Uso:
  recap_generator.py               # recap di OGGI
  recap_generator.py 2026-06-16    # recap di un giorno specifico
  recap_generator.py --backfill 7  # recap mancanti degli ultimi 7 giorni (oggi escluso)
  recap_generator.py --force ...   # riscrive anche se il file esiste
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

HOME = Path.home()
# Il Vault è quello della copia di cockpit che contiene lo script (così da un
# worktree si scrive nel worktree, da ~/cockpit nel Vault vero).
COCKPIT = Path(__file__).resolve().parent.parent
VAULT = COCKPIT / "Vault"
RECAP_DIR = VAULT / "recap"
DETTAGLIO = VAULT / "UniCode" / "log" / "giornate_dettaglio"
# Struttura dal riordino del 2026-09-01: il codice sta in ~/Sviluppo/<categoria>/<repo>,
# lo studio nel Vault di cockpit. Repo singole fuori da ~/Sviluppo elencate a parte.
REPO_DIRS = [COCKPIT, HOME / "Developing", HOME / "lberna777", HOME / "lberna777.github.io"]
REPO_BASES = [HOME / "Sviluppo" / c for c in ("app", "audio", "giochi", "tools", "appunti")]
MAX_COMMIT = 8
# Commit di servizio: non dicono cosa è stato fatto.
RUMORE_RE = re.compile(
    r"^Merge |salvataggio automatico|lavoro in corso|traccia di sessione|consolidamento serale"
    r"|^Consolidamento della giornata|^Log di sessione|^Recap ", re.I)
EVENTO_RE = re.compile(r"^\d\d:\d\d · ([A-Z0-9]+) · (.*)$")
CHIUSO_RE = re.compile(r"\bCHIUSO ([A-Z0-9]+) ([\w-]+)")


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 30) -> str:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return ""


def git_repos() -> list[Path]:
    """Repo da esplorare; quelle che su questa macchina non ci sono si saltano in silenzio.

    RECAP_REPOS (percorsi separati da «:») sostituisce le cartelle del laptop: lo usa
    recap_cloud.sh, che le clona da GitHub nella sessione notturna. cockpit c'è sempre."""
    if os.environ.get("RECAP_REPOS"):
        extra = [Path(d) for d in os.environ["RECAP_REPOS"].split(os.pathsep) if d]
        return [COCKPIT] + [d for d in extra if d.resolve() != COCKPIT
                            and ((d / "HEAD").exists() or (d / ".git").exists())]
    repos = [d for d in REPO_DIRS if (d / ".git").exists()]
    for base in REPO_BASES:
        if base.is_dir():
            repos.extend(sorted(p for p in base.iterdir() if p.is_dir() and (p / ".git").exists()))
    return repos


def collect_studio(day: date) -> list[str]:
    """Eventi di studio per corso e moduli chiusi, dal dettaglio consolidato della giornata."""
    path = DETTAGLIO / f"{day.isoformat()}.md"
    if not path.exists():
        return []
    per_corso: Counter[str] = Counter()
    chiusi: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = EVENTO_RE.match(line.strip())
        if not m:
            continue
        per_corso[m.group(1)] += 1
        chiusi += [f"{c} {mod}" for c, mod in CHIUSO_RE.findall(m.group(2))]
    if not per_corso:
        return []
    out = ["- eventi: " + ", ".join(f"{c} {n}" for c, n in per_corso.most_common())]
    if chiusi:
        out.append("- chiusi: " + ", ".join(dict.fromkeys(chiusi)))
    return out


def collect_git(day: date) -> list[str]:
    since, until = day.isoformat(), (day + timedelta(days=1)).isoformat()
    out: list[str] = []
    for repo in git_repos():
        log = run(["git", "log", "--all", "--no-merges", f"--since={since} 00:00",
                   f"--until={until} 00:00", "--pretty=format:%s"], cwd=repo)
        utili = list(dict.fromkeys(l for l in log.splitlines() if l and not RUMORE_RE.search(l)))
        if not utili:
            continue
        name = "cockpit" if repo == COCKPIT else repo.name.removesuffix(".git")
        out.append(f"- **{name}**: " + " · ".join(utili[:MAX_COMMIT])
                   + (f" · (+{len(utili) - MAX_COMMIT})" if len(utili) > MAX_COMMIT else ""))
    return out


def generate(day: date, force: bool = False) -> str | None:
    RECAP_DIR.mkdir(parents=True, exist_ok=True)
    target = RECAP_DIR / f"{day.isoformat()}.md"
    if target.exists() and not force:
        return None
    studio, commit = collect_studio(day), collect_git(day)
    if not studio and not commit:
        return None
    parti = [f"# Recap {day.isoformat()}"]
    if studio:
        parti.append("## Studio\n" + "\n".join(studio))
    if commit:
        parti.append("## Commit\n" + "\n".join(commit))
    target.write_text("\n\n".join(parti) + "\n", encoding="utf-8")
    return str(target)


def main() -> None:
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    if args and args[0] == "--backfill":
        n = int(args[1]) if len(args) > 1 else 7
        made = [r for i in range(1, n + 1) if (r := generate(date.today() - timedelta(days=i), force))]
        print(f"backfill: {len(made)} recap generati")
        for m in made:
            print(f"  {m}")
        return
    day = datetime.strptime(args[0], "%Y-%m-%d").date() if args else date.today()
    res = generate(day, force)
    print(f"recap scritto: {res}" if res else f"recap {day.isoformat()}: già presente o nessun fatto")


if __name__ == "__main__":
    main()
