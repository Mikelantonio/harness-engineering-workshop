---
name: workshop-demo-ops
description: Prepara ed esegue prove tecniche, preflight ambienti, runbook di demo live, fallback offline e troubleshooting di workshop Python/Google ADK/Gemini. Usa prima di eventi dal vivo, webinar, hackathon e in caso di errori di setup o API.
---

# Live demo operations

1. Prova la demo da un ambiente pulito e con la stessa rete/permessi che avra il relatore; non dichiarare riusciti passaggi non eseguiti.
2. Usa `python scripts/preflight.py` per controlli locali **senza leggere/stampare il valore delle chiavi**. Il check non e una prova di autenticazione o raggiungibilita API.
3. Crea un copione minuto per minuto: comando, output previsto, cosa spiega il relatore, errori probabili, punto di ripartenza.
4. Fissa un modello e versioni dipendenze alla data delle prove; mantieni un test minimale che isoli tool senza LLM.
5. Disponi di fallback: terminale preconfigurato, output JSON sintetico, screenshot/video registrati, repo di backup, hotspot, percorso senza rete.
6. Limita blast radius e costi: quote, timeouts, retries ragionati, API key separate per evento, niente produzione.
7. Tagga i rischi per severita e proprietario; per un evento bloccante comunica subito la soluzione alternativa.

Consulta [references/live-demo-runbook.md](references/live-demo-runbook.md). Lo script `scripts/preflight.py` funziona offline.
