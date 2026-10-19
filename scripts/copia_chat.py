#!/usr/bin/env python3
"""Riduce l'uscita di `list_sessions` (Claude Code Remote) alla copia delle chat della Plancia.

La sezione Claude della Plancia legge le chat dal vivo con il connettore; quando il connettore
non è disponibile usa il documento `claude/chat`, scritto da Claude con questa copia (controllo
del mattino, /manager, /handoff). Uso:

    python3 scripts/copia_chat.py <file con l'uscita di list_sessions> > copia.json

Il file può contenere testo attorno al JSON (come lo salva Claude Code): si prende il primo
oggetto. Stampa {data, sessioni: [...]} con i soli campi che la pagina usa.
"""
import datetime as dt
import json
import sys


def primo_oggetto(testo):
    inizio = testo.index("{")
    oggetto, _ = json.JSONDecoder().raw_decode(testo[inizio:])
    return oggetto


def riduci(s):
    sorgente = (((s.get("session_context") or {}).get("sources") or [{}])[0].get("git_repository") or {})
    repo = (sorgente.get("url") or "").rstrip("/").split("/")[-1].removesuffix(".git")
    rami = ((s.get("external_metadata") or {}).get("current_branches") or {}).values()
    return {
        "id": s.get("id"), "title": s.get("title"),
        "tags": [t for t in s.get("tags") or [] if not t.startswith("config:")],
        "status_bucket": s.get("status_bucket"), "session_status": s.get("session_status"),
        "created_at": s.get("created_at"), "updated_at": s.get("updated_at"),
        "unread": bool(s.get("unread")), "environment_id": s.get("environment_id"),
        "repo": repo, "ramo": next((r for r in rami if r), ""),
    }


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        dati = primo_oggetto(fh.read())
    elenco = (dati.get("ccr") or dati).get("data") or []
    print(json.dumps({"data": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                      "sessioni": [riduci(s) for s in elenco]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
