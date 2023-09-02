import json
import socket
from config import server_host, server_port

def read_products(rfid_socket):
    try:
        while True:
            id_list = rfid_socket.recv(1024).decode()
            if id_list:
                return id_list
    except:
        pass

def shipping_with_confirmation(client_socket, json_message):
    json_message = json.dumps(json_message)
    client_socket.sendall(json_message.encode("utf-8"))
    data_recv = client_socket.recv(1024).decode()
    data_recv_decode = json.loads(data_recv)
    return data_recv_decode

def new_purchase(client_socket, message, shoppingList):
    # Lógica para processar a compra aqui
    pass

def handle_conection(host, port):
    conection_socket = socket.socket()
    conection_socket.connect((host, port))
    print("Conectado ao servidor em", host, "porta", port)
    return conection_socket

def menu_supermercado():
    client_socket = handle_conection("10.182.0.2", server_port)
    
    while True:
        print("\nMenu do Supermercado:")
        print("1. Iniciar uma compra")
        print("2. Sair")

        escolha_menu_principal = input("Digite 1 para iniciar uma compra ou 2 para sair: ")

        if escolha_menu_principal == "1":
            shoppingList = {"products": [], "amout": 0.00}

            while True:
                print("\nOpções de Compra:")
                print("1. Digitar o ID manualmente")
                print("2. Pegar do leitor RFID")
                print("3. Finalizar compra e retornar ao menu anterior")

                escolha_opcoes_compra = input("Escolha uma opção de compra (1/2/3): ")

                if escolha_opcoes_compra == "1":
                    product_id = input("Id: ")
                    product = shipping_with_confirmation(client_socket, {"id": product_id})

                    product_not_exists = product.get("error")
                    if product_not_exists is not None:
                        print(product_not_exists)
                    else:
                        product_name = product.get("nome")
                        shoppingList["products"].append({"id": product_id, "nome": product_name})
                        shoppingList["amout"] += product.get("preco", 0.0)
                        print(product)
                    pass

                elif escolha_opcoes_compra == "2":

                    try:
                        rfid_socket = handle_conection('172.16.103.0', 1234)
                        ids_list = read_products(rfid_socket)
                        try:
                            for id in ids_list:
                                product_add = new_purchase(client_socket, id, shoppingList)
                                print("Produto adicionado:", product_add)
                        except Exception as e:
                            print("Error: ", e)
                        rfid_socket.close()
                        pass
                    except TimeoutError:
                        print("Leitor RFID indisponível")
                        pass

                elif escolha_opcoes_compra == "3":
                    purchase_confirmation = shipping_with_confirmation(client_socket, shoppingList)
                    print(purchase_confirmation)
                    break

                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")

        elif escolha_menu_principal == "2":
            print("Saindo do Supermercado. Até logo!")
            client_socket.close()
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    menu_supermercado()