import json
import socket
import threading
import requests

def get_request(resource):
    try:
        url = "http://localhost:8000/" + str(resource)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                json_data = response.json()
                return json_data
            except json.JSONDecodeError as e:
                print("Erro no JSON:", e)
    except Exception as e:
        print("ERROR COM REQUEST: ", e)

def post_request(data_post, url):
    
    headers = {
    "Content-Type": "application/json"  # Define o tipo de conteúdo como JSON
    }
    
    data_post = json.dumps(data_post) #Converte o dicionário pra json

    response = requests.post(url, data_post, headers=headers)
    json_data = response.json()
    return json_data

def Conection(socket):

    while True:
        client, address = socket.accept()
        print('Conectado a:', address)
        client_ip, client_port = client.getpeername()

        client_permission = get_request("client/" + client_ip)
        error_exists = client_permission.get("error")
        lock_status = client_permission.get("blocked")

        if error_exists != None:
            client_info = {
                "ip": client_ip,
                "port": client_port,
                "blocked": False
            }

            post_request(client_info, "http://localhost:8000/client") #Cadastro de primeira conexão
            threading.Thread(target = threaded, args = (client,)).start() #Inicio uma thread para o client caso ele não esteja cadastrado

        elif lock_status == False:
            threading.Thread(target = threaded, args = (client,)).start() #Inicio uma thread para o client caso ele não esteja bloqueado
        
        elif lock_status == True:
            message_blocked = json.dumps({"error": "Caixa bloqueado"})
            client.send(message_blocked.encode("utf-8"))


def threaded(client):
    client_ip, client_port = client.getpeername()

    try:
        while True:
            data = client.recv(1024).decode('utf-8')

            client_permission = get_request("client/" + client_ip)
            lock_status = client_permission.get("blocked")

            if lock_status == False:

                if not data:
                    break  # Se não houver mais dados, encerre o loop

                data_dict = json.loads(data)
                products_exists = data_dict.get("products")
                message_exists = data_dict.get("message")
                id_exists = data_dict.get("id")

                if products_exists is not None:
                    responseApi = post_request(data_dict, "http://localhost:8000/checkout")
                    responseApiEncode = json.dumps(responseApi).encode("utf-8")
                    client.sendall(responseApiEncode)

                elif id_exists is not None:
                    responseApi = get_request(id_exists)
                    responseApiEncode = json.dumps(responseApi).encode("utf-8")
                    client.sendall(responseApiEncode)

                elif message_exists is not None and message_exists == "lock status":
                    client_permission = get_request("client/" + client_ip)
                    message_error = json.dumps(client_permission)
                    client.sendall(message_error.encode("utf-8"))
            else:
                message_blocked = json.dumps({"error": "Caixa bloqueado"})
                client.sendall(message_blocked.encode("utf-8"))
    except ConnectionResetError:
        print("O caixa", client_ip, "desconectou-se")
        


def Main():
    host = "10.182.0.2" #Pega o ip da máquina que será o server
    port = 3322
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Porta", port, "reservada")

    s.listen()
    print("Escutando na porta reservada")

    threading.Thread(target=Conection, args=(s,)).start()

if __name__ == '__main__':
    Main()
