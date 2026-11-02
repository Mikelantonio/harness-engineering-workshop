---
name: adk-agent-evaluation
description: Progetta test e valutazioni di agenti AI implementati con Google ADK Python, inclusi scenari, tool calling, regressioni, robustezza, prompt injection, costi, latenza e rubric per workshop. Usa per quality gate, review e benchmark pre-demo o post-lab.
---

# Evaluation & quality gates

1. Definisci confini: unit test deterministici dei tools (offline) vs integration test ADK con API vs evaluation probabilistica LLM.
2. Costruisci un set di almeno 6 scenari: happy path, input malformato, out-of-scope, tool failure, prompt injection, cost/latency. Non inventare il punteggio di test non eseguiti.
3. Scegli per ogni scenario: input, atteso, metrica, soglia, evidence/log minimizzato, severita.
4. Verifica anche credenziali, PII, privilegi tools, risposta ad output non attendibile e human-in-the-loop per azioni esterne.
5. Quando e disponibile una API evaluation di ADK valida nella versione target, adotta il formato ufficiale dopo consultazione di https://adk.dev/evaluate/; **non spacciare** il JSON di esempio sotto per formato nativo ADK.
6. Usa `python scripts/check_scenarios.py assets/scenarios.json` per lint del dataset offline; esegui anche pytest dei tools e una smoke run reale solo se esistono credenziali autorizzate.
7. Rendi i risultati come PASS/FAIL/NOT RUN con evidenze e azioni prioritarie, mai come successi impliciti.

Leggi [references/quality-rubric.md](references/quality-rubric.md) e personalizza [assets/scenarios.json](assets/scenarios.json).
