# Patterns Google ADK Python - scelta motivata

| Necessita | Pattern | Rischio/attenzione |
| --- | --- | --- |
| Singola richiesta e tool | `Agent` + function tool | Validare parametri e errori |
| Stato conversazionale | Runner + session service (versione corrente) | Isolamento sessione e dati PII |
| Decomposizione in specialisti | Parent agent e subagents | Handoff, costi e debugging |
| Passi deterministici dipendenti | Sequential workflow | Gestione errori e stato condiviso |
| Ricerca parallela indipendente | Parallel workflow | Fan-out, merge e costo token |
| Iterazione con stopping | Loop workflow | Condizione di uscita e budget |
| Misura qualitativa | Casi/rubric + ADK evaluation | Output non deterministici |

Distinzione essenziale: la skill di Antigravity e un'istruzione per IDE; il runtime ADK e un'app Python eseguita separatamente. Non confonderli.

Non promettere che una feature ADK esista in tutte le versioni; verifica classi e firme prima di generare una soluzione dipendente dalla release.

Fonti canoniche da verificare all'occorrenza:
- https://adk.dev/get-started/python/
- https://adk.dev/agents/llm-agents/
- https://adk.dev/tutorials/agent-team/
- https://adk.dev/evaluate/
- https://adk.dev/tutorials/coding-with-ai/
