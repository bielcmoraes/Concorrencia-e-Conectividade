import socket
import mercury
import time

import socket

def main():

    # Configuração do leitor
    reader = mercury.Reader("tmr:///COM1")  # Substitua "COM1" pela porta do seu leitor, "tmr://192.168.1.101"

    # Inicialização do leitor
    reader.connect()

    # Configurações do servidor
    host = '127.0.0.1' #Host do leitor RFID
    port = 12345
    
    # Cria um socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Liga o socket ao endereço e porta desejados
    server_socket.bind((host, port))
    
    # Escuta por conexões entrantes, permitindo até 5 conexões pendentes
    server_socket.listen(1)
    
    print(f"Leitor RFID ouvindo via socket em {host}:{port}")
    
    try:
        while True:
            # Aceita uma nova conexão
            client_socket, client_address = server_socket.accept()
            print("Conexão estabelecida com o caixa", client_address)
            
            # Leitura e envio das tags para o caixa
            tags = reader.read()  # Leitura de tags
            for tag in tags:
                tag_id = tag.epc #Pega o id da tag
                client_socket.send(tag_id.encode())
                response = client_socket.recv(1024)  # Aguarda resposta do destino
                print("Resposta do destino:", response.decode())
            
            # Fecha a conexão com o cliente
            client_socket.close()
    except:
        print("Conexão com o caixa", client_address, "encerrada")

if __name__ == "__main__":
    main()