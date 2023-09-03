import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import uuid
import threading


dados = {
    'E20000172211010218905459': {"nome": "Farinha", "preco": 10.99, "quantidade": 10},
    'E20000172211010118905454': {"nome": "Leite", "preco": 8.99, "quantidade": 5},
    'E20000172211011718905474': {"nome": "Arroz", "preco": 4.99, "quantidade": 23},
    'E2000017221101321890548C': {"nome": "Feijão", "preco": 2.49, "quantidade": 15},
    'E20000172211009418905449': {"nome": "Macarrão", "preco": 1.99, "quantidade": 30},
    'E20000172211012518905484': {"nome": "Óleo de Soja", "preco": 3.99, "quantidade": 12},
    'E20000172211011118905471': {"nome": "Pneu Aro 13", "preco": 278.93, "quantidade": 8},
    'E2000017221101241890547C': {"nome": "Cuscuz Flocão", "preco": 2.99, "quantidade": 18},
    'E2000017221100961890544A': {"nome": "Nutella", "preco": 6.99, "quantidade": 7},
    '1': {"nome": "Cuscuz", "preco": 1.99, "quantidade": 0},
    '2': {"nome": "Batata", "preco": 3.99, "quantidade": 10},
    '3': {"nome": "Arroz Integral", "preco": 5.99, "quantidade": 10},
    '4': {"nome": "Ovo", "preco": 2.99, "quantidade": 20},
    '5': {"nome": "Pasta de Amendoim", "preco": 6.99, "quantidade": 20}
}

clients_connected = {}

history_purchase = {}

lock = threading.Lock() #

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

        partes_url = self.path.split('/')
        ip = partes_url[1]

        client_exists = clients_connected.get(ip)

        if client_exists:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode('utf-8'))
            with lock:
                client_exists.get("shopping_cart").append(post_data)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = "Um produto foi adicionado ao carrinho do caixa " + client_exists.get("ip")
            print(clients_connected)
            self.wfile.write(json.dumps({"message": message}).encode('utf-8'))

        elif self.path == '/checkout':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode('utf-8'))
            
            for product in post_data["products"]: #Desconta os produtos comprados do estoque
                if product["id"] in dados:
                    with lock:
                        dados[product["id"]]["quantidade"] -= 1

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            id_purchase = uuid.uuid4()
            with lock:
                history_purchase[str(id_purchase)] = post_data
            self.wfile.write(json.dumps({"message": "Compra finalizada com sucesso"}).encode())

        elif self.path == '/client':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data.decode('utf-8'))
            post_data["shopping_cart"] = []
            ip_client = post_data.get("ip")
            with lock:
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
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode('utf-8'))

        partes_url = self.path.split('/')
        ip = partes_url[1]
        shopping_cart_exists = post_data.get("shopping_cart")

        if shopping_cart_exists != None:
            info_client = clients_connected.get(ip)
            if info_client != None:
                info_client["shopping_cart"] = post_data
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_data = json.dumps({"message": "Carronho de compras atualizado com sucesso"}).encode('utf-8')
                self.wfile.write(response_data)

        elif "client" in self.path:
            ip_client = partes_url[2]
            info_client = clients_connected.get(ip_client)

            if info_client != None:
                lock_status = info_client.get("blocked")

                if lock_status == True:
                    with lock:
                        clients_connected[ip_client]["blocked"] = False
                    # Responder com status OK e os dados atualizados
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    message = "Status do caixa alterado para desbloqueado"
                    response_data = json.dumps({"message": message}).encode('utf-8')
                    self.wfile.write(response_data)
                else:
                    with lock:
                        clients_connected[ip_client]["blocked"] = True
            
                    # Responder com status OK e os dados atualizados
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    message = "Status do caixa alterado para bloqueado"
                    response_data = json.dumps({"message": message}).encode('utf-8')
                    self.wfile.write(response_data)
            else:
                # Responder com status não encontrado
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Client não encontrado"}).encode())


def main():
    host = ""
    port = 8000
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()