import json
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
                if message.lower().strip() == 'checkout': #Envia a lista para debitar do estoque
                    shoppingListJson = json.dumps(shoppingList)
                    client_socket.sendall(shoppingListJson.encode("utf-8"))
                    data_recv = client_socket.recv(1024).decode("utf-8")
                    if data_recv == "201":
                        print("Compra finalizada com sucesso!!!")

                else: #Envia id do produto, recebe a resposta e adiciona na lista
                    client_socket.send(message.encode())
                    data_recv = client_socket.recv(1024).decode("utf-8")
                    product = shoppingTerminal.checkProducts(data_recv) # Converte o Json para dicionário
                    shoppingTerminal.amountAndProducts(message, product, shoppingList) #Adiciona o produto à lista e soma o valor ao montante

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
