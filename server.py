import socket
import os
import datetime
import mimetypes
import threading
import logging

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)

class HTTPServer:
    def __init__(self, host='localhost', port=8080, www_dir='www'):
        self.host = host
        self.port = port
        self.www_dir = www_dir
        self.socket = None
        
        # Assicuriamoci che la directory www esista
        if not os.path.exists(self.www_dir):
            os.makedirs(self.www_dir)
            logging.info(f"Creata directory {self.www_dir}")
        
        # Inizializza il dizionario dei MIME types
        mimetypes.init()
    
    def start(self):
        """Avvia il server HTTP"""
        try:
            # Crea un socket TCP/IP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Collega il socket alla porta
            self.socket.bind((self.host, self.port))
            
            # Ascolta connessioni in entrata
            self.socket.listen(5)
            logging.info(f"Server in ascolto su http://{self.host}:{self.port}")
            
            while True:
                # Attendi una connessione
                client, address = self.socket.accept()
                
                # Avvia un thread per gestire la richiesta
                client_thread = threading.Thread(target=self.handle_client, args=(client, address))
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            logging.info("Server interrotto manualmente")
        except Exception as e:
            logging.error(f"Errore durante l'esecuzione del server: {e}")
        finally:
            if self.socket:
                self.socket.close()
            logging.info("Server chiuso")
    
    def handle_client(self, client_socket, address):
        """Gestisce una connessione client"""
        try:
            # Ricevi dati dal client
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                return
            
            # Estrai la prima riga della richiesta
            request_lines = request_data.split('\n')
            first_line = request_lines[0].strip()
            
            # Log della richiesta
            logging.info(f"{address[0]}:{address[1]} - {first_line}")
            
            # Analizza la richiesta
            try:
                method, path, version = first_line.split()
            except ValueError:
                # Richiesta malformata
                self.send_response(client_socket, 400, "Bad Request")
                return
            
            # Gestisci solo le richieste GET
            if method != 'GET':
                self.send_response(client_socket, 405, "Method Not Allowed")
                return
            
            # Normalizza il percorso
            if path == '/':
                path = '/index.html'  # Pagina predefinita
            
            # Costruisci il percorso completo del file
            file_path = os.path.join(self.www_dir, path.lstrip('/'))
            
            # Verifica se il file esiste
            if not os.path.isfile(file_path):
                self.send_404(client_socket)
                return
            
            # Leggi il contenuto del file
            with open(file_path, 'rb') as file:
                content = file.read()
            
            # Determina il MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'  # MIME type di default
            
            # Invia la risposta
            self.send_response(client_socket, 200, "OK", content, mime_type)
            
        except Exception as e:
            logging.error(f"Errore nella gestione della richiesta: {e}")
        finally:
            client_socket.close()
    
    def send_response(self, client_socket, status_code, status_text, content=b'', content_type='text/html'):
        """Invia una risposta HTTP al client"""
        # Prepara l'header della risposta
        header = f"HTTP/1.1 {status_code} {status_text}\r\n"
        header += f"Date: {self.get_date()}\r\n"
        header += f"Server: PythonSimpleHTTP/1.0\r\n"
        header += f"Content-Type: {content_type}\r\n"
        header += f"Content-Length: {len(content)}\r\n"
        header += "Connection: close\r\n\r\n"
        
        # Invia l'header e il contenuto
        response = header.encode('utf-8') + content
        client_socket.sendall(response)
    
    def send_404(self, client_socket):
        """Invia una risposta 404 Not Found"""
        html_content = """
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>404 - Pagina non trovata</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: #e74c3c;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>404 - Pagina non trovata</h1>
                <p>La pagina che stai cercando non esiste o è stata spostata.</p>
                <p><a href="/">Torna alla home page</a></p>
            </div>
        </body>
        </html>
        """
        self.send_response(client_socket, 404, "Not Found", html_content.encode('utf-8'), 'text/html')
    
    def get_date(self):
        """Restituisce la data corrente nel formato HTTP"""
        return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

if __name__ == "__main__":
    server = HTTPServer()
    server.start()