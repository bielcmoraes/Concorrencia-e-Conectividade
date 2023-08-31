import json
from http.server import BaseHTTPRequestHandler, HTTPServer

dados = {
    "1": {"nome": "Abacaxi", "preco": 10.99, "quantidade": 10},
    "2": {"nome": "Melancia", "preco": 8.99, "quantidade": 5},
    "3": {"nome": "Abobora", "preco": 4.99, "quantidade": 23}
}

clients_connected = {

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
        
        elif "client" in self.path: #Rota /client/127.192.1
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            ip_client = partes_url[2]
            client_exists = clients_connected.get(ip_client)
            
            if client_exists == None:
                self.wfile.write(json.dumps({"error": "Cliente ainda não cadastrado"}).encode())
            
            else:
                lock_status = clients_connected.get(ip_client).get("blocked")
                self.wfile.write(json.dumps({"blocked": lock_status}).encode())
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

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Compra finalizada com sucesso"}).encode())

        elif self.path == '/client':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode('utf-8'))
            
            ip_client = post_data.get("ip")
            clients_connected[ip_client] = post_data

            print(clients_connected)
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Cliente cadastrado com sucesso"}).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Rota não encontrada"}).encode())

    def do_PATCH(self):
        # content_length = int(self.headers.get('Content-Length', 0))
        # data_bytes = self.rfile.read(content_length)
        # data_str = data_bytes.decode('utf-8')
        # patch_data = json.loads(data_str)

        partes_url = self.path.split('/')

        if "client" in self.path:
            ip_client = partes_url[2]
            
            lock_status = clients_connected.get(ip_client).get("blocked")

            if lock_status == True:
                clients_connected[ip_client]["blocked"] = False
            
            clients_connected[ip_client]["blocked"] = True

        # Responder com status OK e os dados atualizados
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = json.dumps({"Message": "Status do caixa alterado"}).encode('utf-8')
        self.wfile.write(response_data)


def main():
    host = ""
    port = 8000
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
