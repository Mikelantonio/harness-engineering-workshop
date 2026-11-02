# ADK hands-on starter (Python)

Questa cartella e **codice di esempio per un agent ADK**, distinto dall'agente Antigravity in `.agents/agents/`.

## Setup

Dal percorso di questa cartella (`.../examples/hello_adk/`):

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example hello_adk/.env # Windows: copy .env.example hello_adk\.env
# Modifica hello_adk/.env e inserisci una chiave valida.
pytest -q
adk run hello_adk
```

In alternativa, dalla **directory che contiene** il package `hello_adk/`:

```bash
adk web --port 8000
```

Prompt demo: `Prepara un lab per 24 persone con 6 step. Quale durata suggerisci?`

La funzione in `tools.py` usa un'**euristica didattica** ed e testabile senza rete. La conversazione con un LLM e il funzionamento di `adk run` richiedono `google-adk`, credenziali e rete. Il Web UI e solo per sviluppo.

**Nota:** Non committare `.env` e non usare dati personali reali nei workshop.
