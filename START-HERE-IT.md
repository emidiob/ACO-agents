# ACO — Inizia qui

**Versione 0.3.0. Non è un plugin.** È una libreria di istruzioni e strumenti che puoi usare in ChatGPT e Codex. Gli agenti sono generici; i tuoi dati rimangono nel tuo Drive o in una cartella privata locale.

## Scegli il percorso

**Solo ChatGPT:** non devi installare Python o copiare agenti sul Mac. Devi poter leggere il repository con uno strumento GitHub/file disponibile nella tua chat. Collega Drive separatamente soltanto se vuoi conservare contesti e cronologia. Copia nelle istruzioni di un progetto ChatGPT il contenuto di `docs/CHATGPT-PROJECT-INSTRUCTIONS.txt`, aggiungendo privatamente il collegamento alla cartella autorizzata.

Scrivi:

> Usa ACO dal repository `emidiob/ACO-agents`. Leggi prima `CHATGPT.md`. Voglio pianificare i prossimi tre mesi della mia pratica artistica.

**Codex/VS Code:** estrai lo ZIP, apri `Install ACO.command`, verifica cosa propone e autorizza l'installazione. Serve Python 3.11+. Scegli se installare soltanto le nove skill o anche i 246 profili nativi opzionali. Riavvia Codex. Se il tuo ambiente non riconosce automaticamente le skill, chiedigli di leggere il relativo SKILL.md esplicitamente: non inventare che sia stato caricato.

## Il primo setup Drive

> Usa ACO. Inizializza la knowledge in questa cartella Drive autorizzata. Crea soltanto ciò che manca, non sovrascrivere documenti esistenti, verifica ogni creazione e mostrami l'indice finale.

ACO può eseguire il setup quando la chat espone davvero strumenti Drive di scrittura. La prima autorizzazione degli account resta tua. In sola lettura, ACO deve dichiarare che non può salvare: non basta avere Drive collegato.

La struttura di base contiene un indice, `00-System`, `Personal`, `Organizations` e `Archive`. I contesti, la cronologia e gli handoff di ogni attività vengono creati quando servono. Non devi preparare decine di cartelle a mano.

## Più aziende, attività e clienti

> Aggiungi una seconda azienda. Al suo interno voglio attività di design e publishing. Crea un cliente e un progetto editoriale che coinvolge entrambe.

Un progetto ha una sola cartella, collegata alle attività interessate. Due clienti con lo stesso nome possono avere ID diversi. ACO deve chiedere soltanto se non è chiaro a quale ti riferisci. La pratica artistica personale non diventa automaticamente un cliente della tua azienda.

## Quando lavori

> Continua il progetto del cliente X dal suo ultimo handoff verificato.

> Prepara proposta e preventivo per il cliente Y. Non inviare nulla.

> Chiudi questa sessione, registra cosa è stato fatto, le decisioni confermate e ciò che è ancora aperto. Dimmi se il salvataggio è locale o verificato su Drive.

“Locale verificato” non significa “salvato su Drive”. Se manca la conferma remota, deve risultare “in attesa”. Non c'è un processo sempre acceso a monitorare tutto.

## Aggiornare il GitHub attuale senza perdere nulla

Non cancellare il repository, `.git/` o i file privati. Estrai il nuovo ZIP **fuori** dalla vecchia cartella ACO. Dai a Codex il file `docs/CODEX-MIGRATION-PROMPT.txt`: farà un'anteprima, creerà un ramo di backup e un ramo di lavoro, sostituirà solo i file ACO riconosciuti, eseguirà test e controlli e poi potrà fare commit/push secondo la tua autorizzazione. Drive non viene cancellato o modificato dallo script Git.

## Problemi comuni

- Python mancante/vecchio: `python3 --version`; installa Python 3.11+ dal sito ufficiale o dal tuo gestore approvato.
- macOS blocca il file scaricato: ispeziona lo script e usa il normale flusso di autorizzazione del sistema; non disattivare le protezioni globali.
- File già esistente: l'installer si ferma per proteggerlo. Non forzare la copia alla cieca.
- Installazione interrotta: `python3 scripts/aco_cli.py install-recover` usando la stessa destinazione.
- Drive non scrivibile: continua con un pacchetto locale/in chat chiaramente non sincronizzato.
- Clienti o cartelle duplicati: verifica l'ID nell'indice, non crearne un'altra.

Il manuale completo è nel README. I test locali non equivalgono a un collaudo di tutte le versioni di ChatGPT, Codex, VS Code e delle autorizzazioni del tuo account.
