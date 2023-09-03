import socket
import sys
from datetime import datetime
import mercury
import json

def comunicacao_socket(rfid_client_socket):
    try:
        ultimo_tempo_leitura = {}
        while True:
            enviarId(rfid_client_socket, ultimo_tempo_leitura)
    except socket.error as e:
        print("Erro de soquete:", e)
    except KeyboardInterrupt:
        print("RFID interrompido pelo usuário.")
    finally:
        print("Comunicação fechada")
        rfid_client_socket.close()

def enviarId(rfid_client_socket, ultimo_tempo_leitura):   
    param = 2300

    if len(sys.argv) > 1:
            param = int(sys.argv[1])

    # configura a leitura na porta serial onde esta o sensor
    reader = mercury.Reader("tmr:///dev/ttyUSB0")

    # para funcionar use sempre a regiao "NA2" (Americas)
    reader.set_region("NA2")

    # nao altere a potencia do sinal para nao prejudicar a placa
    reader.set_read_plan([1], "GEN2", read_power=param)

    epcs = map(lambda tag: tag, reader.read())
    print(epcs)
    id_list = []
    for tag in epcs:
        id = (tag.epc).decode()
        print(id)
        # tempo_atual = time.time()
        # if ((id not in ultimo_tempo_leitura) or (tempo_atual - ultimo_tempo_leitura[id]) > 5.0):
        #     ultimo_tempo_leitura[id] = tempo_atual
        id_list.append(id)

    lid_list = json.dumps(id_list).encode()
    rfid_client_socket.send(lid_list)
    confirmacao = rfid_client_socket.recv(1024).decode('utf-8')
    print(confirmacao)
   
def main():
    host = '172.16.103.0' #Host do leitor RFID
    port = 1234

    try:
        # Cria um socket TCP
        rfid_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Liga o socket ao endereço e porta desejados
        rfid_client_socket.bind((host, port))
        
        # Escuta por conexões entrantes, permitindo até 5 conexões pendentes
        rfid_client_socket.listen(1)
        
        print(f"Leitor RFID ouvindo via socket em {host}:{port}")

        while True:
            socket_rfid_client, address = rfid_client_socket.accept()
            print('Conectado a:', address)

            if socket_rfid_client:
                comunicacao_socket(socket_rfid_client)
    except socket.error as e:
        print("Erro de conexão:", e)
    finally:
        rfid_client_socket.close()

if __name__ == "__main__":
    main()