import json
import socket
from config import server_host, server_port

def read_products(rfid_socket):
    try:
        while True:
            id = rfid_socket.recv(1024).decode()
            if id:
                return id
    except:
        pass

def checkout(client_socket, shoppingList):
    shoppingListJson = json.dumps(shoppingList)
    client_socket.sendall(shoppingListJson.encode())
    data_recv = client_socket.recv(1024).decode()
    return data_recv

def list_products(client_socket, message, shoppingList):
    client_socket.send(message.encode())
    data_recv = client_socket.recv(1024).decode()
    if data_recv == "Caixa bloqueado!!!":
        print("Achei crl")
    try:
        product = json.loads(data_recv)
        product_name = product.get("nome")
        if product_name is not None:
            shoppingList["products"].append({"id": id, "nome": product_name})
            shoppingList["amout"] += product.get("preco", 0.0)
        return shoppingList
    except json.JSONDecodeError as e:
        pass
    except Exception as e:
        print("Other error:", e)

def newPurchase(client_socket, id, shoppingList):
    try:
        message = id
        global data_recv
        if message.lower().strip() == 'checkout': #Envia a lista para debitar do estoque
            checkout(client_socket, shoppingList)
        shoppingList = list_products(client_socket, message, shoppingList)
        return shoppingList
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

def handle_conection(host, port):
    conection_socket = socket.socket()
    conection_socket.connect((host, port))
    print("Connected to server on", host, "port", port)
    return conection_socket

 
def main():

    # rfid_socket = handle_conection('172.16.103.0', 1234) #Recebe a host e a port do server RFID 
    client_socket = handle_conection(server_host, server_port)

    print("Digite [1] para iniciar uma nova compra!!!")
    print("Digite [2] para encerrar o caixa!!!")
    start = input("-->>")

    if start == "1":
        try:
            shoppingList = {"products": [], "amout": 0.00}
            while True:
                id = input()
                # id = read_products(rfid_socket)
                shoppingList = newPurchase(client_socket, id, shoppingList)
        except Exception as e:
            print("Error: ", e)
    
    elif start == "2":
        client_socket.close()



if __name__ == "__main__":
    main()
