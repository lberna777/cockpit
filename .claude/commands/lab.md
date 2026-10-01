---
description: "Genera la guida-lab operativa per un modulo dalle fonti del corso (passo 3 del flusso). Uso: /lab <CODICE> <ID>"
argument-hint: "<CODICE> <ID modulo> — es. LAS 3D, FI2 02x, FI2 LAB02"
---

<!-- generato da scripts/unicode_commands.py: non modificare a mano -->

Comando di studio lanciato da `~/cockpit`. La radice di UniCode è `Vault/UniCode`
(nel cloud anche `~/UniCode`): **tutti i percorsi relativi** dell'originale — `stato/`,
`corsi/`, `piano/`, `profilo/`, `log/`, `scripts/` — si risolvono rispetto a quella cartella,
e i comandi di shell che li usano vanno eseguiti da lì (`cd Vault/UniCode` o percorso completo).

1. Se in questa sessione non hai ancora letto `Vault/UniCode/CLAUDE.md`, leggilo per intero.
2. Leggi `Vault/UniCode/.claude/commands/lab.md` ed eseguilo alla lettera, con argomenti:
   `$ARGUMENTS`
3. Le trascrizioni delle sessioni lanciate da cockpit stanno sotto la cartella di progetto di
   cockpit in `~/.claude/projects/` (nel cloud: `-home-user-cockpit`), non sotto quella di
   UniCode: cercale in entrambe quando l'originale le chiede.
4. Nel cloud non c'è Eclipse: i progetti Java si consegnano a Lorenzo come zip importabile
   (*File → Import → Existing Projects into Workspace → Select archive file*) e si compilano
   qui con `javac` per verificarli.
