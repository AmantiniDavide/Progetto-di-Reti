# Relazione Tecnica: Server HTTP Minimale in Python

## Introduzione

Il progetto consiste nella realizzazione di un **server HTTP minimale** implementato interamente in Python utilizzando la libreria `socket`, senza dipendere da framework web esterni. Il server è in grado di servire contenuti statici (HTML, CSS, immagini) e gestire le richieste HTTP secondo lo standard HTTP/1.1.

### Obiettivi del Progetto
- ✅ Comprendere il funzionamento di base del protocollo HTTP
- ✅ Implementare un server web da zero utilizzando socket TCP/IP
- ✅ Servire un sito web statico con multiple pagine
- ✅ Gestire correttamente i MIME types e le risposte di errore
- ✅ Implementare logging delle richieste per monitoraggio

### Specifiche Tecniche
- **Linguaggio**: Python 3.x
- **Protocollo**: HTTP/1.1
- **Architettura**: Multi-threaded server
- **Host**: localhost (127.0.0.1)
- **Porta**: 8080

---

## Architettura del Sistema

### Struttura del Progetto
```
progetto/
├── server.py          # Server HTTP principale
├── server.log         # File di log
└── www/               # Directory contenuti web
    ├── index.html     # Pagina principale (homepage)
    ├── chi-sono.html     # Pagina informativa (chi sono)
    ├── contatti.html   # Pagina contatti e dettagli tecnici
    └── style.css     # Foglio di stile CSS responsive
```

### Componenti Principali

#### 1. HTTPServer Class
La classe principale che gestisce tutte le operazioni del server:
- Inizializzazione e configurazione
- Gestione delle connessioni TCP/IP
- Parsing delle richieste HTTP
- Routing e servizio dei file
- Gestione degli errori

#### 2. Sistema di Threading
- **Thread principale**: Gestisce l'ascolto delle connessioni
- **Thread client**: Un thread dedicato per ogni connessione
- **Daemon threads**: Terminazione automatica alla chiusura del server

#### 3. Sistema di Logging
- **Dual output**: Console e file `server.log`
- **Timestamp**: Data e ora precise per ogni evento
- **Livelli**: INFO per operazioni normali, ERROR per eccezioni

---

## Implementazione del Server

### Configurazione di Base

```python
class HTTPServer:
    def __init__(self, host='localhost', port=8080, www_dir='www'):
        self.host = host          # Indirizzo del server
        self.port = port          # Porta di ascolto
        self.www_dir = www_dir    # Directory contenuti web
```

### Funzionalità Core

#### 1. Inizializzazione del Server
- **Socket Creation**: Creazione socket TCP/IP con `socket.AF_INET`
- **Socket Options**: `SO_REUSEADDR` per riutilizzo immediato della porta
- **Directory Setup**: Creazione automatica della directory `www/` se necessaria
- **MIME Types**: Inizializzazione del sistema di riconoscimento tipi file

#### 2. Gestione delle Connessioni
```python
def start(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.bind((self.host, self.port))
    self.socket.listen(5)  # Coda di max 5 connessioni
```

**Caratteristiche**:
- **Binding**: Collegamento del socket alla porta 8080
- **Listen Queue**: Massimo 5 connessioni in coda
- **Accept Loop**: Ciclo infinito per accettare connessioni
- **Threading**: Ogni client gestito in thread separato

#### 3. Parsing delle Richieste HTTP
Il server analizza le richieste seguendo il protocollo HTTP/1.1:

1. **Ricezione Dati**: Buffer di 4096 bytes per la richiesta
2. **Parsing Request Line**: Estrazione di metodo, path e versione
3. **Validazione**: Controllo formato e metodo supportato
4. **Path Normalization**: Gestione del path "/" → "/index.html"

```python
method, path, version = first_line.split()
if method != 'GET':
    self.send_response(client_socket, 405, "Method Not Allowed")
```

#### 4. Servizio dei File
**Processo di servizio**:
1. **Path Resolution**: Conversione path HTTP → filesystem path
2. **Security Check**: Prevenzione path traversal
3. **File Existence**: Verifica esistenza del file richiesto
4. **Content Reading**: Lettura in modalità binaria
5. **MIME Detection**: Rilevamento automatico del tipo di contenuto
6. **Response Generation**: Creazione risposta HTTP completa

#### 5. Gestione degli Errori

| Codice | Significato | Implementazione |
|--------|-------------|----------------|
| 200 | OK | File trovato e servito correttamente |
| 400 | Bad Request | Richiesta HTTP malformata |
| 404 | Not Found | File non esistente (pagina HTML personalizzata) |
| 405 | Method Not Allowed | Metodo diverso da GET |

#### 6. Sistema di Logging Avanzato
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
```

**Informazioni Registrate**:
- Avvio e spegnimento del server
- Ogni richiesta HTTP con IP, timestamp e request line
- Errori e eccezioni con stack trace
- Creazione automatica directory

---

## Sito Web Statico

### Struttura delle Pagine

#### Homepage (index.html)
**Sezioni principali**:
- **Header**: Navigazione con logo e menu responsive
- **Hero Section**: Presentazione accattivante con call-to-action
- **Features Grid**: Cards animate con caratteristiche del server
- **Footer**: Informazioni sul progetto

**Caratteristiche tecniche**:
- Semantic HTML5 con tag appropriati
- Meta tags per viewport responsive
- Struttura accessibile con heading hierarchy
- Links interni per navigazione fluida

#### Pagina Chi Sono (chi-sono.html)
**Contenuti**:
- **Descrizione Personale**: Siegazione dettagliata sulla mia persona e il mio perscorso formativo
- **Obbiettivi professionali**: Elenco degli obiettivi professionali che desidero raggiungere
- **Competenze**: Competenze che posseggo
- **Animazioni**: Animazioni in css


#### Pagina Contatti (contatti.html)
**Sezioni informative**:
- **Form di contatto**: Form di contatto per chiedere informazioni
- **Contatti**: Contatti e link dove e possibile scrivermi o visionare i miei lavori
- **Comandi Utili**: Guida pratica per utilizzo


### Design e User Experience

#### Caratteristiche del Design
- **Color Scheme**: Gradient da #667eea a #764ba2
- **Typography**: Font system stack per ottima leggibilità
- **Competenze tecniche**: Elenco delle competenze tecniche 


## Funzionalità Implementate

### Requisiti Minimi ✅

| Requisito | Stato | Implementazione |
|-----------|-------|----------------|
| Server HTTP | ✅ | HTTPServer class completa |
| localhost:8080 | ✅ | Configurazione in `__init__` |
| 3 Pagine HTML | ✅ | index.html, about.html, contact.html |
| Richieste GET | ✅ | Parsing e gestione completa |
| Codice 200 | ✅ | Risposta per file esistenti |
| Codice 404 | ✅ | Pagina HTML personalizzata |

### Estensioni Opzionali ✅

| Estensione | Stato | Dettagli |
|------------|-------|----------|
| MIME Types | ✅ | Riconoscimento automatico con `mimetypes` |
| Logging | ✅ | Sistema completo dual-output |
| Layout Responsive | ✅ | Media queries per tutti i dispositivi |
| Animazioni CSS | ✅ | Transizioni, hover effects, keyframes |

### Funzionalità Aggiuntive Implementate

#### Avanzate
- **Multi-threading**: Gestione connessioni simultanee
- **Graceful Shutdown**: Chiusura pulita con Ctrl+C
- **Error Recovery**: Gestione robusta delle eccezioni
- **Resource Management**: Cleanup automatico delle risorse

#### UI/UX
- **Glassmorphism**: Effetti di trasparenza moderna
- **Gradient Backgrounds**: Sfondi accattivanti
- **Micro-interactions**: Feedback visivo per ogni azione
- **Loading States**: Indicatori visivi per le transizioni

---
### Limitazioni Conosciute

#### Funzionalità Non Implementate
- **Solo GET**: Non supporta POST, PUT, DELETE, PATCH
- **No HTTPS**: Comunicazione in chiaro (non sicura)
- **No Authentication**: Nessun controllo accessi
- **No Sessions**: Nessuna gestione stato utente
- **No Cookies**: Nessun supporto per cookies
- **Static Only**: Solo contenuti statici, no PHP/Python server-side

#### Limitazioni Tecniche
- **Buffer Size**: Richieste limitate a 4096 bytes
- **File Size**: Nessun limite implementato (rischio memoria)
- **Concurrent Connections**: Limitato dalla disponibilità thread del sistema
- **Error Recovery**: Restart manuale necessario per errori critici

#### Limitazioni di Sicurezza
- **No Rate Limiting**: Vulnerabile a DoS attacks
- **No Input Sanitization**: Minimal per path HTTP
- **No Logging Rotation**: File di log può crescere indefinitamente
- **No Access Control**: Tutti i file in www/ sono pubblici

## Conclusioni

### Risultati Raggiunti

Il progetto ha **superato tutti gli obiettivi prefissati** con successo, riuscendo nelle implementazioni pratiche di tutte le richieste.

#### Obiettivi Tecnici ✅
- **Server HTTP Completo**: Implementazione robusta da 200+ righe di codice
- **Protocollo HTTP/1.1**: Gestione corretta di richieste e risposte
- **Multi-threading**: Architettura scalabile per connessioni simultanee
- **Error Handling**: Gestione professionale di tutti i casi edge
- **Logging Sistema**: Monitoraggio completo delle operazioni

#### Obiettivi di Design ✅
- **Sito Web Professionale**: 3 pagine HTML complete e funzionali
- **Design Moderno**: Utilizzo di CSS avanzato con animazioni
- **Responsive Layout**: Adattabilità a tutti i dispositivi
- **User Experience**: Navigazione intuitiva e feedback visivo
- **Performance**: Caricamento rapido e fluido









---

*Server HTTP Python - Progetto realizzato nel Giugno 2025*  
*Implementazione completa con socket, threading e web design moderno*

**Repository suggerita**: `python-http-server-project`  
**Linguaggi**: Python (server), HTML/CSS (frontend), Markdown (docs)  
**Keywords**: socket-programming, http-server, web-development, python, threading