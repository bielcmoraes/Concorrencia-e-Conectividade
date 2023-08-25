import json
import socket
import threading
import apiFunctions
import queue #Usada para criar filas de threads e facilitar a troca de informações entre elas

def Conection(socket):
    while True:
        client, address = socket.accept()
        print('Conectado a:', address)
        threading.Thread(target=threaded, args=(client,)).start()

def threaded(c):
    try:
        while True:
            data = c.recv(1024)
            if data:
                dataDecode = data.decode('utf-8')
                dataDict = json.loads(dataDecode)
                
                if type(dataDict) != int:
                    productsExists = dataDict.get("products")
                    if productsExists is not None:
                        result_queue = queue.Queue()
                        threadSendApi = threading.Thread(target=apiFunctions.post_request, args=([dataDict, result_queue],))
                        threadSendApi.start()
                        #threadSendApi.join()  # Espera a thread terminar

                        responseApi = result_queue.get()  # Obtém o resultado da thread
                        c.send(str(responseApi).encode())

                else:
                    responseApi = apiFunctions.get_request(dataDecode)
                    responseApiEncode = json.dumps(responseApi).encode()
                    c.send(responseApiEncode)
    except:
        pass

def Main():
    host = "192.168.43.198"
    port = 3322
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Porta", port, "reservada")

    s.listen()
    print("Escutando na porta reservada")

    threading.Thread(target=Conection, args=(s,)).start()

if __name__ == '__main__':
    Main()
