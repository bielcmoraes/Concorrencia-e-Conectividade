import socket
import threading
import json
from config import server_host, server_port


host = server_host
port = server_port
max_connections = 5  # Limite de conexões simultâneas

# Variável para rastrear as conexões ativas
active_connections = 0
connection_lock = threading.Lock()

dados = {
    "1": {"nome": "Abacaxi", "preco": "10.99"},
    "2": {"nome": "Melancia", "preco": "8.99"},
    "3": {"nome": "Abobora", "preco": "4.99"}
}


# Função para lidar com cada conexão (cliente):
def handle_client(conn):

    global active_connections

    with connection_lock:
        if active_connections >= max_connections:
            print("Limite de conexões atingido. Recusando nova conexão.")
            conn.close()
            return

        active_connections += 1
        print("Adicionando uma conexão, total:", active_connections)

    try:
        # Lógica de tratamento da conexão
        while True:
            # Processamento dos dados recebidos
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            else:
                print("Data: ", data)
                objeto = dados.get(data)
                print("objeto: ", objeto)

                if objeto is not None:
                    conn.send(json.dumps(objeto).encode('utf-8'))
                else:
                    conn.send("Chave não encontrada.".encode('utf-8'))
    except Exception as e:
        print("Erro:", e)
    finally:
        conn.close()

        # Garante que apenas uma thread por vez possa acessar essa seção crítica de código:
        with connection_lock:
            active_connections -= 1
            print("Removendo uma conexão, total:", active_connections)


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(max_connections)

    print("Servidor ouvindo em", host, "porta", port)

    try:
        while True:

            conn, addr = server_socket.accept()
            print('Conexão estabelecida com', addr[0] + ':' + str(addr[1]))
            client_thread = threading.Thread(
                target=handle_client, args=(conn,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
