# GLOBAL FASHION REVERSE LOGISTICS POLICY (v4.2 - 2026)
*Documento Regolamentare per Operatori e Sistemi Autonomi di Reso*

---

## 1. AMBITO E REQUISITI GENERALI

1.1. **Finestra di Reso Standard:**
Ogni cliente ha diritto di richiedere il reso entro **30 giorni solari** dalla data di consegna tracciata dal corriere. Richieste pervenute tra il 31° e il 45° giorno richiedono autorizzazione straordinaria con deprezzamento forfettario del 20%. Oltre i 45 giorni, il reso è categoricamente rifiutato.

1.2. **Condizioni del Capo:**
- **Integrità del Sigillo di Garanzia:** Capi intimi, costumi da bagno e calzature devono conservare il sigillo di sicurezza originale intatto per motivi igienici. Capi senza sigillo non sono rimborsabili.
- **Segni di Usura e Utilizzo:** Capi indossati (odore di profumo, pieghe da utilizzo prolungato, etichette rimosse) subiscono deprezzamento deterministico dal 30% all'80%.

---

## 2. ECCEZIONI DOGANALI E NORMATIVE INTERNAZIONALI

2.1. **Unione Europea (Area Schengen - Hub Principale WMS-MIL-01 / WMS-PAR-04):**
- IVA e dazi non richiedono documentazione doganale supplementare.
- Reso gratuito se il difetto è imputabile a difetto di fabbrica (es. cucitura strappata, zip difettosa).

2.2. **Regno Unito (Extra-UE - Hub Dedicato WMS-LON-03):**
- Richiede dichiarazione doganale CN22/CN23 per "Merci Rese in Regime di Ritorno" (Returned Goods Relief).
- Non è consentito il rimborso diretto delle tasse doganali pagate all'importazione dal cliente: solo il valore imponibile del bene è rimborsabile.

2.3. **Svizzera e Paesi EFTA (Hub di Transito WMS-FRA-02):**
- Resi soggetti a controllo transfrontaliero: il codice doganale TARIC deve essere allegato all'autorizzazione al reso.

2.4. **Stati Uniti e Canada:**
- Resi ammessi solo tramite corriere convenzionato WMS-US. Capi con valore superiore a 800 USD richiedono sdoganamento formale CBP.

---

## 3. DEPREZZAMENTO DETERMINISTICO PER USURA O DIFETTO

Qualora il capo presenti difetti derivanti da uso improprio o usura parziale (non difetto d'origine):
- **Cucitura o cerniera riparabile:** rimborso pari al 100% con buono acquisto oppure 85% su metodo di pagamento originale.
- **Macchie permanenti o strappo del tessuto:** deprezzamento deterministico del 40% sul valore di acquisto.
- **Capo gravemente alterato o manomesso:** rimborso 0% (restituzione a carico del cliente).

---

## 4. REGOLAMENTO FRODE E SOGLIE DI APPROVAZIONE UMANA (HITL)

4.1. **Soglia di Valore Straordinario:**
Qualsiasi indennizzo, rimborso o combinazione di rimborso + buono che superi l'importo totale di **500,00 €** (cinquecento euro) non può essere finalizzato autonomamente da nessun agente AI. Il sistema deve generare un token di sospensione e inoltrare la pratica alla coda `HITL_SUPERVISOR_QUEUE`.

4.2. **Indicatori di Rischio Frode (Fraud Risk Score > 70):**
Un cliente con contrassegno di rischio frode (es. account con frequenza resi > 65%, o reclami multipli per "pacco vuoto" negli ultimi 90 giorni) deve essere SEMPRE bloccato per verifica umana immediata, indipendentemente dal valore del capo.

---

## 5. CODICI MAGAZZINO LOGISTICA DI RESO (WMS HUBS)

I resi devono essere instradati tassativamente verso uno dei seguenti magazzini autorizzati:
- `WMS-MIL-01`: Fashion Hub Sud Europa (Calzature, Borse, Capi in Pelle)
- `WMS-PAR-04`: Luxury & Ready-to-Wear (Haute Couture, Abiti da Sera)
- `WMS-FRA-02`: Central Logistics & Rest of World (Maglieria, Denim, Capi tecnici)
- `WMS-LON-03`: UK Dedicated Cross-Border Hub (Tutti i resi provenienti da UK)

