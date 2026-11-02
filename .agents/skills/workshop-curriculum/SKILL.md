---
name: workshop-curriculum
description: Disegna curriculum didattici e agende al minuto per workshop tecnici su Google ADK Python e AI agents, con Bloom, obiettivi misurabili, demo, esercizi, pause, checkpoint e varianti per livello. Usa per pianificare workshop, bootcamp o sessioni formative.
---

# Curriculum design

1. Leggi il brief prodotto da `workshop-discovery`; in assenza di informazioni usa assunzioni esplicite.
2. Organizza i moduli secondo la dipendenza dei concetti: agent vs workflow -> prompt e tools -> runner e sessione -> orchestrazione -> evaluation, sicurezza e produzione.
3. Applica "spiega 10-15 min -> demo -> pratica -> feedback". Riserva idealmente almeno il 45% dei minuti netti a pratica e debugging; adatta il target al livello.
4. Per ogni blocco definisci durata, prerequisito, obiettivo misurabile, artefatto del partecipante, verifica e variante avanzata.
5. Crea `agenda.json` con blocchi `kind` tra `theory`, `demo`, `lab`, `review`, `break`, `qa`; valida somma e quota hands-on con `python scripts/validate_agenda.py agenda.json --expected-minutes 210 --minimum-practice-ratio 0.40`.
6. Distingui durata lorda (incluse le pause) e durata netta; non sottrarre lo stesso intervallo due volte.
7. Per un workshop di 3 ore o piu proponi un buffer di 10-15 minuti per imprevisti.

Leggi [references/learning-design.md](references/learning-design.md) per criteri di qualita; prendi come base [assets/agenda-example.json](assets/agenda-example.json). Usa le altre skill per implementare codice e lab.
