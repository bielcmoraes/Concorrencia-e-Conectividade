import json
import socket
from config import server_host, server_port
global data_recv

def read_products(rfid_socket):
    try:
        while True:
            id_list = rfid_socket.recv(1024).decode()
            if id_list:
                return id_list
    except:
        pass

def checkout(client_socket, shoppingList):
    print("ZZZZZZZZ: ", shoppingList)
    shoppingListJson = json.dumps(shoppingList)
    client_socket.sendall(shoppingListJson.encode())
    data_recv = client_socket.recv(1024).decode()
    return data_recv

def handle_message(client_socket, message, shoppingList):
    client_socket.send(message.encode("utf-8"))
    data_recv = client_socket.recv(1024).decode()
    data_recv_decode = json.loads(data_recv)
    data_recv_error = data_recv_decode.get("error")
    if data_recv_error is not None:
        return data_recv_decode
    try:
        product_name = data_recv_decode.get("nome")
        if product_name is not None:
            shoppingList["products"].append({"id": message, "nome": product_name})
            shoppingList["amout"] += data_recv_decode.get("preco", 0.0)
        return shoppingList
    except json.JSONDecodeError as e:
        pass
    except Exception as e:
        print("Other error:", e)

def new_purchase(client_socket, message, shoppingList):
    try:
        if message.lower().strip() == 'checkout': #Envia a lista para debitar do estoque
            message_return = checkout(client_socket, shoppingList)
            return message_return
        new_message = handle_message(client_socket, message, shoppingList)
        return new_message
    except Exception as e:
        print("Error:", e)

def handle_conection(host, port):
    conection_socket = socket.socket()
    conection_socket.connect((host, port))
    print("Connected to server on", host, "port", port)
    return conection_socket

 
def main():
    
    client_socket = handle_conection(socket.gethostname(), server_port)

    while True:
        print("Digite o [1] para iniciar a compra")
        start = input("Digite o [2] para encerrar o caixa: ")
        
        if  start == "2":
            client_socket.close()
            break
        elif start == "1":
            buy_control = "1"

            while buy_control == "1":

                ids_list = ['E20000172211010218905459',
                            'E20000172211011718905474',
                            'E20000172211009418905449',
                            'E20000172211011118905471']
                # rfid_socket = handle_conection('172.16.103.0', 1234) #Recebe a host e a port do server RFID
                # ids_list = read_products(rfid_socket)
                shoppingList = {"products": [], "amout": 0.00}
                try:
                    for id in ids_list:
                        message_return = new_purchase(client_socket, id, shoppingList)
                    
                    print("Digite [1] para adicionar mais produtos")
                    buy_control = input("Digite [2] para finalizar a compra: ")
                    if buy_control == "2":
                        # rfid_socket.close()
                        message_return = checkout(client_socket, shoppingList)
                        print(message_return)
                except Exception as e:
                    print("Error: ", e)
            
if __name__ == "__main__":
    main()
