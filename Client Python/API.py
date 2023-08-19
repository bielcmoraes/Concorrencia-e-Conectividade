import json
from http.server import BaseHTTPRequestHandler, HTTPServer

dados = {
    "1": {"nome": "Abacaxi", "preco": 10.99, "quantidade": 10},
    "2": {"nome": "Melancia", "preco": 8.99, "quantidade": 5},
    "3": {"nome": "Abobora", "preco": 4.99, "quantidade": 23}
}

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        partes_url = self.path.split('/')

        id = partes_url[1]
        idExists = dados.get(id)
        
        if self.path == "/%20":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dados).encode())

        elif idExists != None:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dados[id]).encode())
        
        else:
            self.send_response(204)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Fruta nao encontrada"}).encode())

def main():
    host = ""
    port = 8000
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
