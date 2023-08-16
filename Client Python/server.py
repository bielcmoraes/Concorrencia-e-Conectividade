import socket
import threading
from config import server_host, server_port

host = server_host
port = server_port
max_connections = 5  # Limite de conexões simultâneas

# Variável para rastrear as conexões ativas
active_connections = 0
connection_lock = threading.Lock()


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
            data = conn.recv(1024).decode('utf-8')
            print("Cliente: ", data)
            if not data:
                break
            # Processamento dos dados recebidos
            message = input("-> ")
            # client_socket.send(message.encode())
            conn.send(message.encode('utf-8'))
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
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
