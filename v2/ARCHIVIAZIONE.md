# Archivio completo esterno e riepilogo via email

Il nuovo flusso conserva tutti i risultati fuori dal server di calcolo, su un bucket privato compatibile S3. L'email contiene soltanto un piccolo ZIP riepilogativo e un link temporaneo per scaricare l'archivio completo. Non viene creato automaticamente un bucket, non vengono impostate policy pubbliche e non viene acquistato spazio.

## 1. Creare lo spazio esterno una volta

Poiché il server di calcolo è su Hetzner, una possibilità è Hetzner Object Storage. Sono compatibili anche AWS S3 e altri provider S3 con endpoint HTTPS.

Nella Console Hetzner:

1. Aprire il progetto e **Object Storage → Create Bucket**.
2. Scegliere un nome univoco, una località e visibilità **private**. La creazione attiva un servizio a pagamento: verificare i prezzi mostrati dalla Console.
3. In **Security → S3 Credentials → Generate credentials**, generare access key e secret key del progetto del bucket. Salvare la chiave segreta localmente: non sarà nuovamente visualizzabile.
4. Annotare nome del bucket, endpoint e regione. Un esempio per fsn1 è `https://fsn1.your-objectstorage.com`, regione `fsn1`; usare i valori del proprio bucket.

Guide ufficiali: [creare il bucket](https://docs.hetzner.com/storage/object-storage/getting-started/creating-a-bucket/), [generare chiavi S3](https://docs.hetzner.com/storage/object-storage/getting-started/generating-s3-keys/), [panoramica e prezzi](https://www.hetzner.com/storage/object-storage/).

Le chiavi S3 sono distinte dal token API usato per cancellare il server. I permessi necessari sono accesso al bucket per `HeadBucket`, scrittura oggetti/multipart, lettura e metadati degli oggetti. Con versionamento servono anche i permessi di lettura delle versioni. Il programma non richiede la cancellazione degli oggetti né modifica la visibilità. Conservare il bucket dopo aver eliminato il server; non eliminare l'intero progetto o le credenziali mentre servono i link firmati.

## 2. Configurare il server

Dalla cartella `v2`, nell'ambiente Python della simulazione:

```bash
python -m pip install -r requirements-archive.txt
# Solo se archive.env non esiste già:
cp -n archive.env.example archive.env
chmod 600 archive.env
```

Modificare **localmente sul server** `archive.env`, mai nella chat:

```bash
QOC_ARCHIVE_BUCKET="nome-del-bucket"
QOC_ARCHIVE_ENDPOINT="https://fsn1.your-objectstorage.com"
AWS_DEFAULT_REGION="fsn1"
AWS_ACCESS_KEY_ID="chiave-del-proprio-bucket"
AWS_SECRET_ACCESS_KEY="segreto-del-proprio-bucket"
EMAIL_TO="destinatario"
SMTP_USER="mittente"
SMTP_PASSWORD="password-app-smtp"
QOC_PYTHON="/root/stage_env/bin/python"
DELETE_SERVER_AFTER_DELIVERY="false"
```

L'esempio completo include host SMTP, porta, prefisso oggetti, durata del link e scelta della configurazione scientifica. Per AWS S3 lasciare `QOC_ARCHIVE_ENDPOINT` vuoto e specificare la regione AWS. Sono supportati anche i profili/ruoli riconosciuti da boto3: in quel caso non impostare chiavi vuote che sostituiscano quelle del proprio ambiente.

`archive.env` è ignorato da Git e non viene incluso nei bundle dei risultati. Le impostazioni preesistenti SMTP/cloud del vecchio script sono state trasferite, nella copia locale di lavoro, in questo file privato; quando si aggiorna il server occorre configurarvi il suo file. Non copiare le credenziali nel file `.example`.

Per i comandi Python manuali, esportare prima le variabili:

```bash
set -a
source archive.env
set +a
python publish_results.py --check-storage
```

Questo controllo è di sola lettura: verifica accesso al bucket, non i permessi di scrittura né la consegna SMTP. Per un collaudo reale del trasferimento usare un run piccolo già completato con `--upload-only`, come sotto. `auto_v2.sh` carica automaticamente `archive.env`.

## 3. Nuove simulazioni

```bash
bash auto_v2.sh
```

Per impostazione predefinita avvia `configurazione_campagna.jsonc` attraverso `run_and_archive.py`. Il runner verifica che storage e parametri SMTP siano configurati prima di iniziare il calcolo; poi usa **la cartella esatta restituita dalla simulazione**, non l'ultima directory trovata per data.

La sequenza è:

1. Completare la simulazione/campagna.
2. Creare un archivio ZIP64 completo e un riepilogo leggero.
3. Caricare l'archivio su S3 (multipart per file grandi).
4. Rileggere integralmente l'oggetto remoto in streaming e confrontare dimensione e SHA-256 con l'archivio locale.
5. Generare un URL privato firmato e inviare il riepilogo con il link tramite SMTP/TLS.
6. Scrivere una ricevuta `delivery.json` con esito, percorso remoto, versione se disponibile e checksum.
7. Solo se richiesto esplicitamente nella configurazione, cancellare il server.

Il link dura al massimo sette giorni per impostazione predefinita; le credenziali temporanee possono abbreviarne la validità. La scadenza del link non elimina i dati dal bucket. Chiunque possieda il link può scaricare il file fino alla scadenza: il link viene inserito nell'email, non nei normali log o nella ricevuta pubblicabile.

La verifica completa richiede di ritrasferire l'intero archivio dallo storage al server: usa rete e tempo e può generare traffico fatturabile secondo il provider. L'ETag di un multipart o un campo metadata `sha256` impostato dall'uploader non sostituiscono questa verifica.

Per un singolo esperimento, impostare `QOC_RUN_MODE="single"` e `QOC_CONFIG` con il percorso della configurazione normale. Per riprendere una campagna compatibile usare `QOC_RESUME` con la sua directory. Una campagna fermata al solo pilot o con stato `pilot_failed` non è considerata completa e non abilita la cancellazione.

## 4. Risultati già disponibili sul server

Non occorre rifare le simulazioni:

```bash
python publish_results.py --run results/NOME_ESATTO_RUN
```

Per preparare soltanto i file in locale (nessuna connessione, nessun invio):

```bash
python publish_results.py --run results/NOME_ESATTO_RUN --prepare-only
```

Per verificare soltanto caricamento e integrità, senza email:

```bash
python publish_results.py --run results/NOME_ESATTO_RUN --upload-only
```

Le esportazioni predefinite sono `results/exports/NOME_ESATTO_RUN/`. L'output deve stare fuori dalla run sorgente, per evitare archivi ricorsivi. È possibile scegliere `--output /percorso/esterno` e `--receipt /percorso/ricevuta.json`. `--upload-only` non abilita la cancellazione del server. `publish_results.py` non cancella mai server o dati, indipendentemente dalle opzioni.

Se SMTP fallisce dopo un caricamento riuscito, ripetere lo stesso comando: il bundle locale viene riutilizzato se non è cambiato e l'oggetto remoto esistente viene **riverificato integralmente** prima di riprovare la mail. La chiave dell'oggetto include SHA-256 e nome run, per non sovrascrivere altri risultati. In caso di corruzione remota si interrompe, senza accettare il precedente esito o cancellare i dati locali.

Il file `bundle.json` conserva l'inventario locale. Dentro lo ZIP, `ARCHIVE_MANIFEST.json` elenca dimensione e hash di ciascun file. Sono inclusi tutti i file della run/campagna e gli snapshot sorgente, tranne cache Python rigenerabili. Le directory esterne, il file delle credenziali e l'intero repository non vengono aggiunti indiscriminatamente. I link simbolici nella run sono rifiutati.

## 5. Cancellazione automatica e gestione degli errori

Il nuovo default è **conservare il server**:

```bash
DELETE_SERVER_AFTER_DELIVERY="false"
```

Per ripristinare la cancellazione automatica dopo la consegna completa:

```bash
DELETE_SERVER_AFTER_DELIVERY="true"
HCLOUD_TOKEN="token-api-hetzner"
```

`auto_v2.sh` esegue la cancellazione solo dopo il successo del processo corrente e una ricevuta che confermi sia verifica SHA-256 remota sia accettazione del messaggio da parte del server SMTP. Usa una ricevuta nuova per ciascun avvio. L'accettazione SMTP non garantisce l'arrivo nella posta in entrata, ma i risultati sono già fuori dal server e recuperabili dal bucket.

Se simulazione, upload, verifica o email falliscono, lo script termina con errore e **conserva server e dati**. Non esegue più un `poweroff` automatico né dichiara che lo spegnimento azzeri i costi del server. Una richiesta DELETE HTTP fallita viene segnalata come errore; non viene presentata come cancellazione riuscita.

## 6. Recuperare i dati dopo la scadenza del link

Il percorso persistente `s3://bucket/chiave` e lo SHA-256 sono indicati nell'email e in `delivery.json`. Scaricare l'oggetto dalla Console oppure rigenerare un link usando la ricevuta e credenziali S3 valide:

```bash
python publish_results.py --refresh-link /percorso/delivery.json --link-file /percorso/link-privato.json
```

Il comando riverifica l'oggetto remoto e salva l'URL in un file con permessi privati, senza stamparlo sul terminale. Dopo il download, confrontare lo SHA-256 dell'archivio con quello riportato nell'email/ricevuta.

## Riepilogo allegato e limiti email

Il riepilogo contiene un report HTML autonomo, statistiche CSV e configurazione. Non ha link a figure omesse; gli array, i grafici e i metadati dettagliati restano nell'archivio completo. I file opzionali troppo grandi vengono esclusi e nominati nel README interno al riepilogo. Il budget del riepilogo è 10 MiB; il mittente limita gli allegati a 15 MiB e controlla anche la dimensione MIME codificata e l'eventuale limite SIZE annunciato dal server SMTP.

Prova locale sul run Fock n10 t20 esistente: archivio completo circa 70 MiB, riepilogo circa 3.3 KB. I test automatici usano uno storage simulato e SMTP simulato: nessun trasferimento verso un provider reale o invio email è stato effettuato durante l'implementazione. Il collegamento reale va collaudato dopo aver creato il bucket e configurato le chiavi.
