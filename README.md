# Sotto il cofano degli AI agent: harness engineering in pratica

## Scopo del workshop
Stai creando un workshop da portare ad una DevFest. L'audience è composta da sviluppatori neofiti in AI che sono incuriositi dall'idea di costruire sistemi complessi basati su AI. Vuoi introdurli al mondo dell'Harness Engineering in modo pratico e stimolante. 

## Descrizione del Workshop
Il workshop dura 1h e 30 min.
Utilizzando ADK di Google (Framework + UI web) svilupperemo una harness essenziale da lanciare tutta in locale sul computer dei partecipanti  per spiegare i diversi elementi che la compongono. Deve essere chiaro come vengano implementati i diversi pezzi della harness: context builder, LLM, policy gate, tools / runtime, verify, constraint e observability.


## Caso d'uso
Il caso d'uso riguarda la gestione Resi e Sconti Straordinari (Reverse Logistics Fashion)
I diversi elementi della harness hanno i seguenti compiti:
- Context Builder: Carica le policy di reso internazionali e le eccezioni doganali per paese.
- LLM: Esamina le foto del capo difettoso caricate dall'utente e la descrizione del reclamo.
- Policy Gate (HITL): Se l'indennizzo supera i 500 € o l'utente è schedato come sospetto di frode, blocca e attende un operatore umano.
- Tools / Runtime: Aggiorna lo stato del reso sul WMS (Warehouse Management System) e genera l'etichetta di spedizione.
- Verify: Valida che lo schema JSON di autorizzazione al reso contenga codici magazzino esistenti.
- Constraints: Limite massimo di step decisionali concessi all'agente per pratica.
- Observability: Monitoraggio della cache del regolamento e dei costi di computazione per ticket.

## Vincoli

- Il codice deve essere ben strutturato e di semplice lettura
- Parti dal caso senza harness e costruisci pezzo per pezzo  tutti i componenti in maniera incrementale, mostrando come si relazionano tra loro e come è possibile testarli in locale. Per ogni pezzo che aggiungi, crea un test che dimostri la differenza rispetto alla sua mancanza.
- Ogni pezzo che aggiungi va messo dentro una commit git distinta. Di conseguenza, il repository deve essere "git clean" all'inizio del workshop.

## Specifiche tecniche

- usa ADK 2.13 per python
- L'interfaccia web è quella di default fornita da ADK
- Dai la possibilità di puntare il sistema a Gemini o Gemma.@g

## Struttura del workshop (1h e 30 min)

| Timing | Modulo / Attività | Cosa fanno i partecipanti (Codice) | Componente della Harness coperto |
| --- | --- | --- | --- |
| **00:00 - 00:10** | **Kickoff & Architecture Review** | Spiegazione rapida del flusso: dal reclamo del cliente alla policy di rimborso automatica o bloccata. | *Panoramica del sistema* |
| **00:10 - 00:25** | **Blocco 1: Context & LLM** | Scrivono il `ContextBuilder` per separare le regole di reso statiche (Stable Zone) dai dati del capo reso (Volatile Zone) e istanziano l'agente ADK. | **1. Context Builder**, **2. LLM** |
| **00:25 - 00:45** | **Blocco 2: Tools & Policy Gate** | Implementano il tool di calcolo rimborso e configurano il `confirmationHandler` che intercetta i rimborsi $> 500 €$ bloccandoli per l'operatore. | **3. Policy Gate (HITL)**, **4. Tools/Runtime** |
| **00:45 - 01:05** | **Blocco 3: Verifier & Constraints** | Scrivono il validatore JSON formale dell'autorizzazione al reso e impostano il contatore massimo di tentativi (loop di retry). | **5. Verify**, **6. Constraints** |
| **01:05 - 01:20** | **Blocco 4: Observability & Test** | Attivano i listener di telemetria per tracciare i token letti dalla cache e testano il fallimento di uno schema. | **7. Observability** |
| **01:20 - 01:30** | **Live Demo & Test Finale** | Test del caso limite: simulazione di un reso fraudolento o fuori policy e verifica del blocco dell'harness. | *Test di integrazione* |


## Come mappare i 7 Componenti nel codice del Workshop (Traccia Rapida)

1. **Context Builder:**
* *Cosa scrivono:* Una classe che concatena le 20 pagine di policy di reso globali in cima e appende i dettagli del capo (es. *"Giacca in pelle, cucitura strappata, costo 600€"*).

2. **LLM:**
* *Cosa scrivono:* L'inizializzazione dell'agente ADK associato a Gemini o Gemma.

3. **Policy Gate (HITL):**
* *Cosa scrivono:* La logica nel tool di rimborso.

4. **Tools / Runtime:**
* *Cosa scrivono:* La funzione matematica deterministica che calcola l'eventuale deprezzamento del capo per usura, evitando che l'LLM "inventi" il rimborso.

5. **Verify / Verifier:**
* *Cosa scrivono:* Un blocco di parsing che controlla se l'output dell'agente è un JSON valido con i codici magazzino corretti. Se fallisce, restituisce l'errore al loop.

6. **Constraints:**
* *Cosa scrivono:* Il vincolo rigido nel ciclo (`val maxRetries = 3`), impedendo all'agente di consumare token all'infinito se il modello non corregge l'errore.

7. **Observability:**
* *Cosa scrivono:* Una riga di log che stampa i metadati di utilizzo (`usageMetadata.cachedContentTokens` e `promptTokens`) per dimostrare il risparmio del prompt caching.
