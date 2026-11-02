# Live Demo Runbook & Fallback Offline

> **Guida operativa per lo speaker durante la presentazione live sul palco della DevFest**

---

## 💻 Checklist Preflight (15 minuti prima del talk)

- [ ] Portatile collegato all'alimentatore (evitare throttling della CPU su batteria)
- [ ] Risoluzione schermo impostata a 1920x1080, font terminale impostato a 18pt
- [ ] Terminale aperto con due tab:
  - Tab 1: Directory principale del progetto con virtualenv attivo (`source .venv/bin/activate`)
  - Tab 2: Pronto per l'avvio della Web UI ADK (`adk web src/harness` o monitor log)
- [ ] Esecuzione test di preflight rapido:
  ```bash
  python3 -m unittest discover tests
  ```
  *(Deve restituire `Ran 29 tests ... OK` in < 0.05s)*

---

## 🎯 Script della Live Demo (Comandi da Eseguire)

### 1. Mostrare il fallimento dell'agente senza Harness (2 min)
```bash
python3 -m unittest tests/test_00_no_harness.py -v
```
*Cosa dire:*  
"Notate come l'agente non protetto approva un rimborso arbitrario non deterministico e cerca di spedire verso un magazzino inventato. Senza harness, questo va dritto in produzione."

### 2. Eseguire l'applicazione completa con i due casi d'uso (3 min)
```bash
python3 src/harness/app.py
```
*Cosa mostrare a schermo:*
1. **Caso 1 (Standard):**
   - Action: `REFUND`
   - Amount: `€180.00`
   - Gate Triggered: `False`
   - Cache Hit: `100.0%`
2. **Caso 2 (Lusso > 500 €):**
   - Action: `HITL_ESCALATION`
   - Amount Requested: `€850.00`
   - HITL Blocked: `True`
   - Supervisor Ticket: `HITL-VAL-XXXXXX`
   - Reason: *"Requested refund amount €850.00 exceeds the autonomous threshold of €500.00"*

### 3. Mostrare la Web UI di ADK (3 min)
```bash
adk web src/harness
```
Aprire il browser su `http://localhost:8000`:
- Mostrare i tool registrati (`calculate_depreciated_refund`, `generate_wms_return_label`).
- Inserire il prompt di prova:  
  *"Voglio fare il reso della mia giacca in pelle acquistata 10 giorni fa per 180 euro con cucitura scucita."*
- Mostrare l'esecuzione del tool deterministico e la generazione dell'etichetta.

---

## 🚨 Piano B: Gestione Imprevisti (Offline Fallback)

| Imprevisto | Causa | Azione Immediata / Soluzione |
| :--- | :--- | :--- |
| **Wi-Fi della conferenza bloccato o instabile** | Quota o captive portal | I test e `src/harness/app.py` sono **100% offline-ready** grazie alla simulazione deterministica incorporata. Non serve connessione. |
| **Quota Gemini API Key esaurita o scaduta** | Rate limit o key errata | Cambiare in `.env`: `MODEL_PROVIDER=gemma` con Ollama locale (`ollama run gemma2:9b`), oppure usare il runner deterministico locale. |
| **Un partecipante resta indietro col codice** | Errore di sintassi o git conflict | Far eseguire: `git stash && git checkout step-7-complete` per allinearsi istantaneamente all'ultimo stato funzionante. |
| **Porta 8000 già occupata per ADK Web** | Altro servizio in ascolto | Lanciare su porta alternativa: `adk web src/harness --port 8080`. |

