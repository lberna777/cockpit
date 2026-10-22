#!/usr/bin/env python3
"""Controllo giornaliero della salute degli hook e del lavoro non inviato (cockpit).

Lo lancia ogni mattina l'attività programmata «Salute degli hook» in una sessione cloud nuova;
la sessione scrive il risultato nel documento `claude/salute` della Plancia, che la sezione
Claude mostra. Si può lanciare anche a mano: `python3 scripts/salute_hook.py`.

Non esegue gli hook che scrivono (autosave, avvio, fine sessione): ne controlla solo la presenza
e la sintassi. Esegue davvero solo i due hook senza effetti (titolo della chat e handoff), con
un ingresso finto. Stampa un JSON: {data, controlli: [{nome, esito, dettaglio}], non_inviato}.
Esito: ok · avviso · errore.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
controlli = []


def esito(nome, stato, dettaglio=""):
    controlli.append({"nome": nome, "esito": stato, "dettaglio": dettaglio})


def git(*args):
    r = subprocess.run(["git", "-C", RADICE, *args], capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout.strip()


def script_degli_hook():
    with open(os.path.join(RADICE, ".claude", "settings.json"), encoding="utf-8") as fh:
        impostazioni = json.load(fh)
    trovati = {}
    for evento, gruppi in impostazioni.get("hooks", {}).items():
        for gruppo in gruppi:
            for hook in gruppo.get("hooks", []):
                for rel in re.findall(r"\$\{CLAUDE_PROJECT_DIR\}/([\w./-]+)", hook.get("command", "")):
                    trovati.setdefault(rel, set()).add(evento)
    return trovati


def controlla_script():
    try:
        trovati = script_degli_hook()
    except (OSError, ValueError) as e:
        esito("Impostazioni degli hook", "errore", f".claude/settings.json illeggibile: {e}")
        return
    mancanti, rotti = [], []
    for rel in sorted(trovati):
        percorso = os.path.join(RADICE, rel)
        if not os.path.isfile(percorso):
            mancanti.append(rel)
            continue
        if rel.endswith(".sh"):
            r = subprocess.run(["bash", "-n", percorso], capture_output=True, text=True)
            if r.returncode:
                rotti.append(f"{rel}: {r.stderr.strip()[:120]}")
        elif rel.endswith(".py"):
            try:
                with open(percorso, encoding="utf-8") as fh:
                    compile(fh.read(), percorso, "exec")
            except SyntaxError as e:
                rotti.append(f"{rel}: riga {e.lineno}: {e.msg}")
    if mancanti:
        esito("Script degli hook", "errore", "mancano: " + ", ".join(mancanti))
    elif rotti:
        esito("Script degli hook", "errore", "; ".join(rotti))
    else:
        esito("Script degli hook", "ok", f"{len(trovati)} script presenti e senza errori di sintassi")


def prova_hook(nome, rel, ingresso):
    percorso = os.path.join(RADICE, rel)
    if not os.path.isfile(percorso):
        return
    try:
        r = subprocess.run([sys.executable, percorso], input=json.dumps(ingresso), capture_output=True,
                           text=True, timeout=20, cwd=RADICE,
                           env={**os.environ, "CLAUDE_PROJECT_DIR": RADICE})
    except subprocess.TimeoutExpired:
        esito(nome, "errore", "non risponde entro 20 secondi")
        return
    if r.returncode:
        esito(nome, "errore", f"esce con codice {r.returncode}: {r.stderr.strip()[:160]}")
        return
    if r.stdout.strip():
        try:
            json.loads(r.stdout)
        except ValueError:
            esito(nome, "avviso", "risponde, ma non in JSON")
            return
    esito(nome, "ok", "provato con un ingresso finto")


def controlla_master():
    # il clone del cloud è parziale: senza la storia intera ogni ramo vecchio sembra «avanti»
    _, parziale = git("rev-parse", "--is-shallow-repository")
    if parziale == "true":
        git("fetch", "-q", "--unshallow", "origin")
    codice, _ = git("fetch", "-q", "origin", "master",
                    "+refs/heads/claude/*:refs/remotes/origin/claude/*")
    if codice:
        esito("Collegamento a GitHub", "errore", "git fetch non riuscito")
        return []
    _, quando = git("log", "-1", "--format=%cI", "origin/master")
    try:
        giorni = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(quando)).days
    except ValueError:
        giorni = None
    if giorni is None:
        esito("Ultimo invio su master", "avviso", "data non leggibile")
    else:
        esito("Ultimo invio su master", "ok" if giorni <= 3 else "avviso",
              f"{giorni} giorni fa" if giorni else "oggi")

    non_inviato = []
    proprio = os.environ.get("RAMO_DA_IGNORARE", "")
    _, rami = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/claude/")
    for ramo in filter(None, rami.splitlines()):
        nome = ramo.removeprefix("origin/")
        if nome == proprio:
            continue
        codice, avanti = git("rev-list", "--count", f"origin/master..{ramo}")
        if codice or not avanti.isdigit():
            non_inviato.append({"repo": "cockpit", "ramo": nome, "avanti": None,
                                "nota": "storia troppo corta per contare i commit"})
        elif int(avanti) > 0:
            _, ultimo = git("log", "-1", "--format=%cs · %s", ramo)
            non_inviato.append({"repo": "cockpit", "ramo": nome, "avanti": int(avanti), "nota": ultimo[:120]})
    esito("Rami claude/* di cockpit", "ok" if not non_inviato else "avviso",
          "tutti uniti in master" if not non_inviato else f"{len(non_inviato)} con commit non in master")
    return non_inviato


def controlla_marcatori():
    # 2026-10-22: il 19, 20 e 21/10 l'autosave ha portato su master marcatori di conflitto.
    # .obsidian/ escluso: il plugin obsidian-git li contiene nel suo codice.
    codice, righe = git("grep", "-n", "-E", "^(<<<<<<<|>>>>>>>)( |$)", "origin/master", "--",
                        ".", ":(exclude)*/.obsidian/*")
    if codice not in (0, 1):
        esito("Marcatori di conflitto su master", "avviso", "git grep non riuscito")
        return
    file = sorted({r.split(":")[1] for r in righe.splitlines() if r})
    esito("Marcatori di conflitto su master", "errore" if file else "ok",
          ("in " + ", ".join(file)) if file else "nessuno")
    # il pre-commit che li rifiuta va attivato in ogni clone (nel cloud lo fa cloud_bootstrap.sh)
    _, percorso = git("config", "--get", "core.hooksPath")
    esito("Pre-commit contro i marcatori", "ok" if percorso == ".githooks" else "avviso",
          "attivo" if percorso == ".githooks" else "core.hooksPath non è .githooks in questo clone")


def controlla_consolidamento():
    percorso = os.path.join(RADICE, "Vault", "UniCode", "log", "giornate.md")
    try:
        with open(percorso, encoding="utf-8") as fh:
            date = re.findall(r"\*\*(\d{4}-\d{2}-\d{2})\*\*", fh.read())
    except OSError:
        esito("Consolidamento dello studio", "errore", "log/giornate.md non trovato")
        return
    if not date:
        esito("Consolidamento dello studio", "avviso", "nessuna giornata in log/giornate.md")
        return
    ultima = max(date)
    giorni = (dt.date.today() - dt.date.fromisoformat(ultima)).days
    esito("Consolidamento dello studio", "ok" if giorni <= 2 else "avviso",
          f"ultima giornata consolidata: {ultima}" + ("" if giorni <= 2 else " (il timer del laptop è fermo?)"))


def main():
    controlla_script()
    prova_hook("Hook del titolo della chat", ".claude/hooks/titolo_chat.py",
               {"session_id": "prova-salute", "prompt": "prova", "hook_event_name": "UserPromptSubmit"})
    prova_hook("Hook del passaggio di consegne", ".claude/hooks/context_handoff.py",
               {"session_id": "prova-salute", "transcript_path": "", "stop_hook_active": False})
    non_inviato = controlla_master()
    controlla_marcatori()
    controlla_consolidamento()
    print(json.dumps({"data": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                      "controlli": controlli, "non_inviato": non_inviato}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
