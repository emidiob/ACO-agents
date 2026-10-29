# Motion design delle interfacce · Applicazioni commentate

Tutti i dati qui sotto sono sintetici. Le risposte sono esercizi dello stesso autore del metodo, non esiti di un valutatore indipendente.

### Caso 1

**Brief.** Aprire un dettaglio a partire da una card, in tre registri sintetici.

**Risposta insufficiente.** Cambiare soltanto la velocità di uno stesso effetto spettacolare.

**Applicazione ACO.** Discreto: opacità 160 ms senza traslazione; editoriale: traslazione verticale 12 px e opacità 280 ms; espressivo: scala 0,96→1 e opacità 420 ms. Sono scelte progettuali dell’esercizio. Tutte mantengono il pulsante chiudi, una destinazione stabile e lo stesso testo. Con movimento ridotto la transizione è immediata.

**Commento.** Le differenze riguardano proprietà e ampiezza, oltre alla durata. Il file browser dimostra la meccanica, non una preferenza universale.

**Limiti.** Il prototipo usa CSS originale: non certifica un’integrazione Motion o GSAP.

### Caso 2

**Brief.** Un pannello di stato si muove in parallasse ma contains una conferma importante.

**Risposta insufficiente.** Disattivare l’intero pannello quando l’utente riduce il movimento.

**Applicazione ACO.** Conservare pannello e conferma; eliminare la parallasse, assicurando un cambiamento visivo statico e un annuncio di stato quando pertinente. Rimuovere gli ascoltatori o gli effetti obsoleti al cambio delle condizioni.

**Commento.** L’accessibilità cambia la modalità, non sottrae l’informazione.

**Limiti.** L’effettiva percezione assistiva richiede una prova sul prodotto finale.
