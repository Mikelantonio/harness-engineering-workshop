---
name: adk-lab-authoring
description: Scrive hands-on labs e codelab progressivi per Google ADK con Python, inclusi setup, codice starter, istruzioni step-by-step, checkpoint, hint, challenge avanzate, soluzioni e troubleshooting. Usa quando bisogna costruire esercitazioni tecniche per workshop AI agents.
---

# Hands-on lab authoring

1. Usa un singolo obiettivo verificabile per ciascun lab (es. agent tool calling, tool design, routing, evaluation).
2. Prepara un bundle con `README.md`, codice starter, expected output, test automatici, hint e soluzione separata; scrivi i comandi da una working directory esplicita.
3. Definisci prerequisiti, durata, verifica di successo in meno di 3 minuti e il percorso per chi resta indietro.
4. Metti almeno un checkpoint dopo il primo step e una mini-challenge dopo l'esercizio base.
5. Non dipendere da Google Cloud se l'obiettivo formativo e realizzabile con Gemini API; spiega eventuali limitazioni.
6. Aggiungi un piano offline: test sui tool senza LLM + log/output campione chiaramente etichettati come mock.
7. Mantieni istruzioni idempotenti e non distruttive; non richiedere chiavi direttamente nei notebook o nel codice versionato.
8. Prepara `solutions/` solo su esplicita richiesta o se l'output e destinato al formatore; separa il materiale degli allievi.

Usa [assets/lab-template.md](assets/lab-template.md) per la struttura e [references/lab-rubric.md](references/lab-rubric.md) per valutare il lab. Per lo starter funzionante consulta `adk-python-implementation/examples/hello_adk`.
