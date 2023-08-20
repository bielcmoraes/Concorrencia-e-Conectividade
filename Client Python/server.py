import json
import socket
import threading
import apiFunctions
import queue #Usada para criar filas de threads e facilitar a troca de informações entre elas

print_lock = threading.Lock()

def threaded(c):
    while True:
        data = c.recv(1024)
        if not data:
            print_lock.release()
            break
        
        dataDecode = data.decode('utf-8')
        dataDict = json.loads(dataDecode)
        
        if type(dataDict) != int:
            productsExists = dataDict.get("products")
            if productsExists is not None:
                result_queue = queue.Queue()
                threadSendApi = threading.Thread(target=apiFunctions.post_request, args=([dataDict, result_queue],))
                threadSendApi.start()
                threadSendApi.join()  # Espera a thread terminar

                responseApi = result_queue.get()  # Obtém o resultado da thread
                c.send(str(responseApi).encode())

        else:
            responseApi = apiFunctions.get_request(dataDecode)
            responseApiEncode = json.dumps(responseApi).encode()
            c.send(responseApiEncode)

    c.close()

def Main():
    host = ""
    port = 12345
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Porta", port, "reservada")

    s.listen(5)
    print("Escutando na porta reservada")

    while True:
        c, addr = s.accept()
        print_lock.acquire()
        print('Conectado a:', addr[0], ':', addr[1])
        threading.Thread(target=threaded, args=(c,)).start()

    s.close()

if __name__ == '__main__':
    Main()
