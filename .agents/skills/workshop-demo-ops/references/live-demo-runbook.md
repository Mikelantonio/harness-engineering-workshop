# Runbook live (T-7 giorni -> T+1 giorno)

- **T-7**: account, policy API e billing confermati; partecipanti ricevono prerequisiti e starter repo.
- **T-2**: creare env pulito, verificare import di google.adk, ripetere lab, controllare quota e timeouts.
- **T-1**: rete della venue, proiettore, font minimo 18pt, tema terminale, schermo condiviso, key e token temporanei.
- **T-30 min**: test via `preflight.py` e 1 chiamata reale al modello **solo se autorizzata**; log senza PII.
- **Durante**: ogni demo ha una checkpoint slide; se errore di rete oltre 2 min, passare a output sintetico salvato.
- **T+1**: eliminare chiavi temporanee, raccogliere feedback, aprire issue per problemi replicati.

## Playbook errori

| Sintomo | Azione primaria | Fallback |
|---|---|---|
| `ModuleNotFoundError: google.adk` | controlla interprete e `pip install google-adk` | registra demo pre-eseguita |
| API key mancante | correggere `.env` locale non versionato | test tool offline |
| Quota, 429, billing | ridurre concorrenza e controllare quota | output campione dichiarato |
| Modello non disponibile | verificare modello/region/versione | modello compatibile provato prima |
| Wi-Fi non affidabile | hotspot previsto | demo video/offline |
