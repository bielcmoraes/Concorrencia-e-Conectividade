import json
import socket
from _thread import *
import threading
import apiFunctions

print_lock = threading.Lock()

def threaded(c):
    while True:
        data = c.recv(1024)
        if not data:
            print_lock.release()
            break
        
        data_decode = data.decode('utf-8')

        responseApi = apiFunctions.get_request(data_decode)
        
        #Fazer a lógica para caso o client mande checkout finalize a compra
        # retirando as quantidades do estoque
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
        start_new_thread(threaded, (c,))

    s.close()

if __name__ == '__main__':
    Main()