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

    def do_POST(self):
        if self.path == '/checkout':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode('utf-8'))
            
            for product in post_data["products"]: #Desconta os produtos comprados do estoque
                if product["id"] in dados:
                    dados[product["id"]]["quantidade"] -= 1

            print(dados)
            self.send_response(201)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Compra finalizada com sucesso')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Rota não encontrada')

def main():
    host = ""
    port = 8000
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
