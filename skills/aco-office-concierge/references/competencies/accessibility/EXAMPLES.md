# Accessibilità contestuale · Applicazioni commentate

Tutti i dati qui sotto sono sintetici. Le risposte sono esercizi dello stesso autore del metodo, non esiti di un valutatore indipendente.

### Caso 1

**Brief.** Registrazione sintetica con nome ed email; la versione iniziale indica errore solo con bordo rosso.

**Risposta insufficiente.** Aggiungere aria-label a ogni elemento e dichiarare WCAG superato.

**Applicazione ACO.** Il prototipo corretto usa label visibili, istruzioni email e riepilogo che collega gli errori ai campi. Dopo invio invalido il riepilogo riceve focus; il link porta al campo, con aria-invalid e descrizione dell’errore. Dopo dati validi un messaggio di stato conferma la registrazione simulata. Le prove browser incluse percorrono tutto con tastiera.

**Commento.** Si controlla un risultato d’uso, non una quantità di attributi. Il submit resta locale, senza account creati.

**Limiti.** Non è una certificazione WCAG; nessuna prova NVDA/VoiceOver o test con persone è stata eseguita.

### Caso 2

**Brief.** La stessa fotografia appare come immagine editoriale e come link senza testo alla scheda dell’opera.

**Risposta insufficiente.** Usare sempre «fotografia dell’opera» come alt.

**Applicazione ACO.** Nel testo editoriale descrivere il dettaglio pertinente alla lettura. Nel link isolato assegnare il nome utile a capire la destinazione: «Scheda dell’opera Campo, 2025». Se lo stesso link contiene già quel testo, rendere la foto decorativa per evitare duplicazioni.

**Commento.** La funzione cambia anche quando i pixel rimangono identici.

**Limiti.** Titolo e anno qui sono dati inventati per l’esercizio, non metadati di un’opera reale.
