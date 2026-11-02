# Guida Hands-On Codelab: Sotto il cofano degli AI agent

> **Workshop DevFest (1h 30m)**  
> *Harness Engineering in Pratica con Google ADK (Agent Development Kit) e Python*

---

## 🧭 Introduzione al Caso d'Uso: Fashion Reverse Logistics

Sei a capo del team di automazione logistica di una prestigiosa piattaforma e-commerce di moda. I resi dei clienti contengono contestazioni, richieste di indennizzo per capi difettosi e documentazione doganale complessa.

Affidare un processo simile a un **LLM "nudo"** senza un'infrastruttura di controllo (*Harness*) porta a conseguenze disastrose:
* **Allucinazioni finanziarie:** l'LLM inventa percentuali di rimborso a caso.
* **Mancanza di controlli di rischio:** rimborsi da 1.200 € autorizzati senza approvazione umana.
* **Corruzione della supply chain:** instradamento verso magazzini inesistenti (es. `WMS-ROMA-99`).
* **Loop infiniti di token:** agenti che riprovano all'infinito consumando budget cloud.

In questo workshop costruirai pezzo per pezzo una **Harness a 7 componenti** basata su **Google ADK**.

---

## ⚙️ Setup Iniziale (Primi 10 minuti)

### 1. Clonazione e Branch
```bash
git clone <URL_REPO>
cd harness-engineering-workshop
```

### 2. Creazione dell'Ambiente Python
Se utilizzi `uv` (consigliato per velocità durante la conferenza):
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```
Oppure tramite `venv` standard:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurazione `.env`
Copia il file di template:
```bash
cp .env.example .env
```
Inserisci la tua API Key gratuita di [Google AI Studio](https://aistudio.google.com/):
```env
MODEL_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy...
```

Verifica il corretto funzionamento della suite iniziale:
```bash
pytest tests/test_00_no_harness.py
```

---

## 🧱 I 7 Blocchi dell'Harness (Percorso Didattico)

### Blocco 1: Context Builder (Stable Zone vs Volatile Zone)
* **Tag Git:** `step-1-context-builder`
* **File:** `src/harness/context.py`
* **Concetto:** Separare la documentazione normativa (immutabile, ~2.000 token) dai dati del ticket utente. Il prefisso fisso permette a Gemini di attivare il **Prompt Caching automatico**, riducendo i costi del 75% e la latenza del 50%.
* **Verifica:**
```bash
pytest tests/test_01_context.py
```

---

### Blocco 2: LLM & Multimodale
* **Tag Git:** `step-2-llm-multimodal`
* **File:** `src/harness/agent.py`
* **Concetto:** Inizializzazione dell'agente Google ADK con supporto a immagini e testo:
```python
from google.adk.agents import Agent

root_agent = Agent(
    name="reverse_logistics_agent",
    model="gemini-2.5-flash",
    description="Agente gestione resi fashion",
    instruction="...",
    tools=[calculate_depreciated_refund, generate_wms_return_label]
)
```
* **Verifica:**
```bash
pytest tests/test_02_llm_multimodal.py
```

---

### Blocco 3: Policy Gate (Human-In-The-Loop)
* **Tag Git:** `step-3-policy-gate`
* **File:** `src/harness/policy_gate.py`
* **Concetto:** Nessun agente deve avere autonomia finanziaria illimitata. Se l'indennizzo supera i **500 €** o il cliente ha un punteggio frode elevato, il gate intercetta la richiesta ed emette un ticket di escalation per il supervisore umano (`HITL_SUPERVISOR_QUEUE`).
* **Verifica:**
```bash
pytest tests/test_03_policy_gate.py
```

---

### Blocco 4: Tools Deterministici (Runtime)
* **Tag Git:** `step-4-tools-runtime`
* **File:** `src/harness/tools.py`
* **Concetto:** Non chiedere all'LLM di fare calcoli aritmetici o deprezzamenti. L'agente estrae i fatti (difetto riparabile, giorni trascorsi, cartellino presente) e delega il calcolo a funzioni matematiche pure e deterministiche.
* **Verifica:**
```bash
pytest tests/test_04_tools.py
```

---

### Blocco 5: Verifier (Validatore Formale di Schema)
* **Tag Git:** `step-5-verifier`
* **File:** `src/harness/verifier.py`
* **Concetto:** Validare l'output dell'agente prima di inviarlo al database WMS. Il verifier controlla che i codici magazzino (`WMS-MIL-01`, `WMS-LON-03`, ecc.) esistano realmente e che le spedizioni UK abbiano la dichiarazione doganale CN22.
* **Verifica:**
```bash
pytest tests/test_05_verifier.py
```

---

### Blocco 6: Constraints (Anti-Loop & Budget)
* **Tag Git:** `step-6-constraints`
* **File:** `src/harness/constraints.py`
* **Concetto:** Vincolo rigido sul numero di tentativi e step di decisione (`max_steps=3`). Se l'agente entra in un ciclo di indecisione, la harness forza l'interruzione con eccezione controllata salvaguardando il conto economico.
* **Verifica:**
```bash
pytest tests/test_06_constraints.py
```

---

### Blocco 7: Observability (Telemetria & Cache Token)
* **Tag Git:** `step-7-observability`
* **File:** `src/harness/observability.py`
* **Concetto:** Tracciare `cached_content_tokens`, latenza di risposta ed economia dell'agente.
* **Verifica:**
```bash
pytest tests/test_07_observability.py
```

---

## 🚀 Live Demo & Test Finale

Esegui l'applicazione completa end-to-end:
```bash
python3 src/harness/app.py
```

Per lanciare la Web UI nativa di Google ADK:
```bash
adk web src/harness
```

Lancia l'intera suite di integrazione:
```bash
pytest tests/test_e2e_integration.py -v
```

Se sei rimasto indietro durante la digitazione, puoi saltare direttamente a qualsiasi step tramite Git:
```bash
git checkout step-7-complete
```

