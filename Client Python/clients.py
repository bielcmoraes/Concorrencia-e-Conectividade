import socket
from config import server_host, server_port
import shoppingTerminal

def newPurchase(client_socket):

    shoppingList = {"products": [], "amout": 0.00}
    try:
        while True:
            message = input("-> ")
            global data_recv

            if message.strip() == "":
                message = " "
                client_socket.send(message.encode())
                data_recv = client_socket.recv(1024).decode("utf-8")  
            else:
                client_socket.send(message.encode())
                data_recv = client_socket.recv(1024).decode("utf-8")
            
            product = shoppingTerminal.checkProducts(data_recv) # Converte o Json para dicionário
            shoppingTerminal.amountAndProducts(product, shoppingList) #Adiciona o produto à lista e soma o valor ao montante

            if message.lower().strip() == 'checkout':
                return shoppingList
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def main():
    host = server_host
    port = server_port

    client_socket = socket.socket()
    client_socket.connect((host, port))

    print("Connected to server on", host, "port", port)

    try:
        checkout = newPurchase(client_socket)
        print(checkout)
    except KeyboardInterrupt:
        print("Closing the client.")



if __name__ == "__main__":
    main()
