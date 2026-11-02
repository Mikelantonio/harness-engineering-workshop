# Speaker Notes & Facilitator Guide (90 Minuti)

> **Titolo Workshop:** Sotto il cofano degli AI agent: harness engineering in pratica  
> **Speaker Persona:** Google Developer Expert (GDE) in AI Agents & Google ADK  
> **Target:** Sviluppatori software neofiti in AI  
> **Setup Proiettore:** Risoluzione 1080p, font terminale ingrandito (18pt+)

---

## ⏱️ Timeline Minuto per Minuto

### 00:00 - 00:10 (10 min) | Accoglienza, Il "Perché" e il Caso d'Uso
* **Azione Speaker:**
  * Benvenuto alla DevFest. Chiedere per alzata di mano: *"Quanti di voi hanno già chiamato un'API di un LLM con una system prompt di 5 pagine sperando che non sbagliasse?"*
  * Spiegare il concetto cardine: **I modelli fondazionali sono motori stocastici, non sistemi software affidabili. La differenza tra un prototipo da hackathon e un sistema in produzione è la HARNESS.**
  * Mostrare la slide architetturale con i 7 componenti.
  * Presentare il caso studio: *Reverse Logistics Fashion (Resi & Rimborsi d'eccezione)*.
* **Checkpoint:** Tutti i partecipanti devono avere il repo clonato e l'ambiente attivo.

---

### 00:10 - 00:25 (15 min) | Blocco 1: Context Builder & LLM
* **Storytelling:**
  * *"Se inviate 20 pagine di PDF di policy a ogni messaggio utente, bruciate soldi e aumentate la latenza. Come fa Google con Gemini a riconoscere che il contesto è lo stesso?"*
  * Introdurre la **Stable Zone** (immutabile, posizionata rigorosamente in cima al prompt) vs **Volatile Zone** (i dati del singolo reclamo).
* **Live Coding / Esercizio:**
  * Mostrare `src/harness/context.py`.
  * Eseguire `pytest tests/test_01_context.py`.
* **Domanda all'aula:** *"Cosa succede se mettete il nome dell'utente prima della policy globale? Rompete l'hit del Prompt Caching."*

---

### 00:25 - 00:45 (20 min) | Blocco 2: Tools & Policy Gate (HITL)
* **Storytelling:**
  * *"Gli LLM sanno fare le moltiplicazioni? Mai fidarsi del calcolo stocastico del rimborso."*
  * Introdurre i Function Tools deterministici (`calculate_depreciated_refund`).
  * Poi sollevare il tema governance: *"Volete che l'agente possa rimborsare autonomamente 5.000 € sulla carta di credito del cliente?"*
  * Mostrare il **Policy Gate**: soglia rigida a 500 € e controllo antifrode. Se superata, intercetta e crea un ticket supervisore (`HITL_SUPERVISOR_QUEUE`).
* **Verifica in aula:**
  * Eseguire `pytest tests/test_03_policy_gate.py` e `pytest tests/test_04_tools.py`.

---

### 00:45 - 01:05 (20 min) | Blocco 3: Verifier & Constraints
* **Storytelling:**
  * *"Cosa succede se l'agente inventa un magazzino che non esiste nel vostro WMS? I corrieri lasciano i bancali in mezzo alla strada."*
  * Introdurre il **Verifier**: validazione Pydantic / Schema rigido. L'output deve contenere un codice magazzino autorizzato (`WMS-MIL-01`, `WMS-LON-03`).
  * Mostrare i **Constraints**: limite rigido a 3 step decisionali per evitare infinite retry loop quando il modello non riesce a correggere un errore.
* **Verifica in aula:**
  * Eseguire `pytest tests/test_05_verifier.py` e `pytest tests/test_06_constraints.py`.

---

### 01:05 - 01:20 (15 min) | Blocco 4: Observability & Telemetria
* **Storytelling:**
  * *"Come dimostrate al vostro CTO che la harness non è solo overhead, ma fa risparmiare budget reale?"*
  * Mostrare `src/harness/observability.py`: estrazione di `cached_content_tokens`, calcolo del cache hit rate (80%+) e risparmio economico in USD per ticket.
* **Verifica in aula:**
  * Eseguire `pytest tests/test_07_observability.py`.

---

### 01:20 - 01:30 (10 min) | Live Demo Finale, Q&A & Wrap-Up
* **Demo Live:**
  * Esecuzione di `python3 src/harness/app.py` o `adk web src/harness`.
  * Caso A: Reso conforme standard da 180 € (approvato autonomamente, 100% cache hit).
  * Caso B: Reso lusso da 850 € (bloccato dal Policy Gate per revisione umana).
* **Takeaways Finali per l'Audience:**
  1. Mai lasciare l'LLM da solo a interagire con database ed effetti esterni.
  2. Isolare Stable e Volatile Zone per sfruttare il Prompt Caching.
  3. Determinismo matematico nei Tool, non nel modello.
  4. Human-In-The-Loop obbligatorio sopra soglie di rischio prefissate.
  5. Il codice è pronto e riutilizzabile nei vostri progetti!

