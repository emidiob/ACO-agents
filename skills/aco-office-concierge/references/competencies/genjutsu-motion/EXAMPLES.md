# Genjutsu: osservazione e trasferimento del movimento · Applicazioni commentate

Tutti i dati qui sotto sono sintetici. Le risposte sono esercizi dello stesso autore del metodo, non esiti di un valutatore indipendente.

### Caso 1

**Brief.** Fixture originale di 2 secondi: un cursore a pinza si avvicina a un disco, lo afferra, lo sposta, lo lascia e si allontana; camera fissa.

**Risposta insufficiente.** Una pinza prende un disco e lo sposta con movimento fluido.

**Applicazione ACO.** 0–0,40 s: avvicinamento senza contatto. 0,40–0,80: contatto e sollevamento. 0,80–1,40: trasporto verso destra con disco vincolato alla pinza. 1,40–1,60: abbassamento e rilascio. 1,60–2,00: pinza si allontana, disco fermo. Camera statica per tutto l’intervallo. La variante negativa omette il rilascio: il disco continua con la pinza, quindi fallisce lo stato finale.

**Commento.** La fixture è generata da noi e dichiarata sintetica; permette un controllo reale di tempi e oggetti senza fingere una prova su un video commerciale o un provider AI.

**Limiti.** Il generatore fornisce ground truth: questo test non dimostra riconoscimento automatico di movimenti in video sconosciuti.

### Caso 2

**Brief.** Reference ipotetica: una mano ruota una chiave, poi la chiave scompare dietro una scatola. Destinazione proposta: un soggetto senza mani.

**Risposta insufficiente.** Attribuire la rotazione a una mano invisibile e ricostruire anche il tratto nascosto.

**Applicazione ACO.** Segnalare due problemi distinti: manipolatore incompatibile e traiettoria non osservata. Conservare la rotazione solo con un meccanismo alternativo esplicitamente approvato; per il tratto occultato chiedere evidenza aggiuntiva o non promettere fedeltà.

**Commento.** La trasformazione non può mascherare incompatibilità fisiche con una descrizione generica.

**Limiti.** Nessuna reference reale è stata analizzata in questo secondo esempio.
