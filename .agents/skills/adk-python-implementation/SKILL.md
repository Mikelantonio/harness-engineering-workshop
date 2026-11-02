---
name: adk-python-implementation
description: Implementa, spiega e revisiona agenti AI in Python con Google Agent Development Kit (ADK), Gemini, function tools, runner, sessioni e pattern multi-agent. Usa per codice eseguibile, architettura, scaffold, migrazioni e troubleshooting di Google ADK.
---

# Google ADK Python implementation

## Regole tecniche

1. Ispeziona codice e versione installata prima di modificare un progetto. Controlla la reference ufficiale all'indirizzo https://adk.dev/get-started/python/ e la compatibilita della versione effettiva.
2. Per l'esempio base crea un package Python con `__init__.py`, `agent.py` e `root_agent`; usa `from google.adk.agents import Agent` (oppure l'import documentato dalla versione presente).
3. Usa `Agent(name=..., model=..., description=..., instruction=..., tools=[...])`. Per i tools privilegia funzioni pure, tipizzate, con docstring, validazione dell'input e output JSON-serializzabile.
4. Gestisci auth tramite `.env.example`; mai chiavi hardcoded, mai stamparle. Se manca la key, spiega come impostarla e mantieni test offline funzionanti.
5. Fornisci comandi da directory corretta: `python -m venv .venv`, `pip install google-adk`, `adk run <package>` o `adk web` nella directory padre del package.
6. Quando richiedono multi-agent, giustifica e usa gli strumenti ADK appropriati verificando le API correnti; non introdurre `SequentialAgent`, `ParallelAgent`, `LoopAgent` o trasferimenti se un agent semplice basta.
7. Insegna sicurezza: azioni esterne devono prevedere permesso, tools con privilegi minimi, output trattati come dati, non come istruzioni fidate.
8. Testa localmente tool puri e sintassi; test reali del modello solo con chiavi e quote disponibili. Indica esplicitamente l'esito dei test.

## Asset da copiare

Prendi come starter [examples/hello_adk](examples/hello_adk): agent minimo, tool deterministico, test pytest, env example e README. Consulta [references/adk-patterns.md](references/adk-patterns.md) per il criterio di scelta dei pattern.
