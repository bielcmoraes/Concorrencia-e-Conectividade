import json
import socket
import threading
import requests
import os

socket_host = os.environ.get('HOST_SOCKET_SERVER', '127.0.0.1')
socket_port = int(os.environ.get('PORT_SOCKET_SERVER', 3322))

messages_log = {}
output_lock = threading.Lock()

def get_request(resource):
    
        url = "http://" + socket_host + ":8000/" + str(resource)
        url = url.replace('"', '')
        response = requests.get(url)
        try:
            json_data = response.json()
            return json_data
        except json.JSONDecodeError as e:
            print("\nErro no JSON:", e)

def post_request(data_post, url):
    
    headers = {
    "Content-Type": "application/json"  # Define o tipo de conteúdo como JSON
    }
    
    data_post = json.dumps(data_post) #Converte o dicionário pra json
    response = requests.post(url, data_post, headers=headers)
    try:
        json_data = response.json()
        return json_data
    except json.JSONDecodeError as e:
        print("\nErro no JSON:", e)

def patch_request(data_patch, url):

    response = requests.patch(url, json=data_patch)
    try:
        json_data = response.json()
        return json_data
    except json.JSONDecodeError as e:
        print("\nErro no JSON:", e)
    
def Conection(socket):

    while True:
        try:
            client, address = socket.accept()
            print('Caixa:', address, "conectou-se")
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
            
                post_request(client_info, "http://" + socket_host + ":8000/client") #Cadastro de primeira conexão
                threading.Thread(target = threaded, args = (client,)).start() #Inicio uma thread para o client caso ele não esteja cadastrado

                post_request(client_info, "http://localhost:8000/client") #Cadastro de primeira conexão
                threading.Thread(target = threaded, args = (client,)).start() #Inicio uma thread para o client caso ele não esteja cadastrado

            elif lock_status == False:
                threading.Thread(target = threaded, args = (client,)).start() #Inicio uma thread para o client caso ele não esteja bloqueado
            
            elif lock_status == True:
                message_blocked = json.dumps({"error": "Caixa bloqueado"})
                client.send(message_blocked.encode("utf-8"))
        except requests.exceptions.RequestException:
            client.close()
            print("\nConexão com " + client_ip + "cancelada. Servidor HTTP indisponível")

def threaded(client):
    client_ip, client_port = client.getpeername()
    
    messages_log[client_ip] = [] #Cria a lista de mensagens para o client conectado
    list_messages = None

    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            
            list_messages = messages_log.get(client_ip)

            if data:
                log_message = "Rcv from " + client_ip + " " + str(client_port) + ": " + data
                list_messages.append(log_message)
            
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
                    data_dict["ip"] = client_ip 
                    responseApi = post_request(data_dict, "http://" + socket_host + ":8000/checkout")
                    responseApiEncode = json.dumps(responseApi).encode("utf-8")
                    patch_request({"shopping_cart": []}, "http://" + socket_host + ":8000/" + client_ip)
                    client.sendall(responseApiEncode)

                    log_message = "Send from " + client_ip + " " + str(client_port) +": " + str(responseApiEncode)
                    list_messages.append(log_message)

                elif id_exists is not None:
                    responseApi = get_request(id_exists)
                    responseApiEncode = json.dumps(responseApi).encode("utf-8")
                    response_api_decode = responseApiEncode.decode("utf-8")
                    post_request(response_api_decode , "http://" + socket_host + ":8000/" + client_ip)
                    client.sendall(responseApiEncode)

                    log_message = "Send from " + client_ip + " " + str(client_port) +": " + str(responseApiEncode)
                    list_messages.append(log_message)

                elif message_exists is not None and message_exists == "lock status":
                    client_permission = get_request("client/" + client_ip)
                    message_error = json.dumps(client_permission)
                    client.sendall(message_error.encode("utf-8"))

                    log_message = "Send from " + client_ip + " " + str(client_port) + ": " + str(responseApiEncode)
                    list_messages.append(log_message)
                
                elif message_exists is not None and message_exists == "disconnect":
                    patch_request({"shopping_cart": []}, "http://" + socket_host + ":8000/" + client_ip)
                    print("O caixa", client_ip, str(client_port), "desconectou-se")

                    log_message = "O caixa", client_ip, str(client_port), "desconectou-se"
                    list_messages.append(log_message)
            else:
                message_blocked = json.dumps({"error": "Caixa bloqueado"})
                client.sendall(message_blocked.encode("utf-8"))

                log_message = "Send from " + client_ip + " " + str(client_port) + ": " + str(message_blocked)
                list_messages.append(log_message)

    except ConnectionResetError:
        patch_request({"shopping_cart": []}, "http://" + socket_host + ":8000/" + client_ip)
        print("O caixa", client_ip, str(client_port), "desconectou-se de maneira abrupta")

        log_message = "O caixa", client_ip, str(client_port), "desconectou-se de maneira abrupta"
        list_messages.append(log_message)
        
def block_cashier(client_ip):
    response = patch_request({}, "http://" + socket_host + ":8000/client/" + client_ip)
    print(response)

def log_all():
    print("\nMensagens do servidor não visualizadas")
    for client_ip, message_list in messages_log.items():
        with output_lock: #Bloqueia a thread
            for message in message_list:
                print(message)
    messages_log[client_ip] = []

def log_one(client_ip):
    
    with output_lock:
        if client_ip in messages_log:
            print("\nMensagens não visualizadas do client " + client_ip)
            for message in messages_log[client_ip]:
                print(message)
        else:
            print(f"\nO cliente com IP {client_ip} não tem mensagens.")
    
def Main():
    host = socket_host
    port = socket_port
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Server", host, "on na porta", port)

    s.listen()
    print("Escutando na porta reservada")

    threading.Thread(target=Conection, args=(s,)).start()
    
    while True:
        print("\n----Administrar servidor----")
        print("\n1. Bloquear um caixa")
        print("2. Mensagens não lidas de todos os caixas")
        print("3. Mensagens não lidas de um caixa em específico")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção: ")

        if choice == "1":
            client_ip = input("\nDigite o IP do caixa a ser bloqueado: ")
            block_cashier(client_ip)
        elif choice == "2":
            # Crie uma thread para monitorar todas as mensagens em tempo real
            monitor_thread = threading.Thread(target=log_all)
            monitor_thread.daemon = True  # Define a thread como daemon para que ela seja encerrada quando o programa principal encerrar
            monitor_thread.start()
            monitor_thread.join() #Aguarda termino da thread de visualizar mensagens
        elif choice == "3":
            client_ip = input("\nDigite o IP do caixa a ser monitorado: ")
            # Crie uma thread para monitorar as mensagens em tempo real
            monitor_thread = threading.Thread(target=log_one, args = (client_ip,))
            monitor_thread.daemon = True  # Define a thread como daemon para que ela seja encerrada quando o programa principal encerrar
            monitor_thread.start()
            monitor_thread.join() #Aguarda termino da thread de visualizar mensagens
        elif choice == "4":
            print("\nEncerrando o servidor...")
            s.close()
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == '__main__':
    Main()
