# Video, montaggio e narrazione temporale · Applicazioni commentate

Tutti i dati qui sotto sono sintetici. Le risposte sono esercizi dello stesso autore del metodo, non esiti di un valutatore indipendente.

### Caso 1

**Brief.** Film sintetico per una biblioteca di oggetti riparabili: messaggio «riparare prima di sostituire», prova apertura e sostituzione di una parte.

**Risposta insufficiente.** Ridurre a un quarto la velocità di lettura nel cut da 15 secondi mantenendo tutto il testo.

**Applicazione ACO.** 15 s: problema 0–3, apertura/riparazione 3–10, risultato 10–12, invito 12–15. 30 s: problema 0–5, diagnosi 5–10, riparazione 10–21, risultato 21–26, invito 26–30. 60 s: contesto 0–8, problema 8–16, diagnosi 16–26, riparazione 26–43, confronto 43–53, invito 53–60. A 25 fps sono rispettivamente 375, 750 e 1500 frame.

**Commento.** Le varianti conservano l’azione dimostrativa, non solo uno slogan. I JSON verificabili nel pacchetto mantengono gli intervalli esatti.

**Limiti.** Questo esercizio genera scalette, non tre film montati con materiale reale.

### Caso 2

**Brief.** Una clip parte al frame 90 dentro una sezione che parte al frame 50. Il montatore annota inizio globale 90.

**Risposta insufficiente.** Accettare il valore perché entrambe le voci parlano di frame.

**Applicazione ACO.** Se 90 è un offset locale, l’inizio globale è 140. Registrare la base temporale di ogni numero prima del conform; non modificare il media in finché non è chiaro se il valore indica timeline o trim del sorgente.

**Commento.** Il bug è un’ambiguità di coordinate, non una preferenza di montaggio.

**Limiti.** Le API del motore effettivamente usato devono essere controllate alla sua versione.
