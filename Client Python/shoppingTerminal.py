import json

def checkProducts (responseApi):
    responseApi = json.loads(responseApi)
    return responseApi

def amountAndProducts (id, product, shoppingList):

    if product != None:
        productExists = product.get("nome")
        if productExists != None:
            shoppingList["products"].append({"id": id, "nome": product["nome"]})
            shoppingList["amout"] += product["preco"]
