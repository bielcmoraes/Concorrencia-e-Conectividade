import json
import socket
import threading
import apiFunctions

def Conection(socket):
    while True:
        client, address = socket.accept()
        print('Conectado a:', address)
        client_ip, client_port = client.getpeername()

        client_permission = apiFunctions.get_request("client/" + client_ip)

        error_exists = client_permission.get("error")
        lock_status = client_permission.get("blocked")

        if error_exists != None:
            client_info = {
                "ip": client_ip,
                "port": client_port,
                "blocked": False
            }
            apiFunctions.post_request(client_info, "http://localhost:8000/client") #Cadastro d eprimeira conexão
            threading.Thread(target = threaded, args = (client,)).start() #Inicio uma thread para o client caso ele não esteja cadastrado
        elif lock_status == False:
            threading.Thread(target = threaded, args = (client,)).start() #Inicio uma thread para o client caso ele não esteja bloqueado

def threaded(client):
    try:
        while True:
            data = client.recv(1024)
            if data:
                dataDecode = data.decode('utf-8')
                dataDict = json.loads(dataDecode)
                
                if type(dataDict) != int:
                    productsExists = dataDict.get("products")
                    if productsExists is not None:
                        responseApi = apiFunctions.post_request(dataDict, "http://localhost:8000/checkout");
                        client.send(str(responseApi).encode())

                else:
                    responseApi = apiFunctions.get_request(dataDecode)
                    responseApiEncode = json.dumps(responseApi).encode()
                    client.send(responseApiEncode)
        
    except:
        pass

def Main():
    host = socket.gethostname() #Pega o ip da máquina que será o server
    port = 3322
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Porta", port, "reservada")

    s.listen()
    print("Escutando na porta reservada")

    threading.Thread(target=Conection, args=(s,)).start()

if __name__ == '__main__':
    Main()
