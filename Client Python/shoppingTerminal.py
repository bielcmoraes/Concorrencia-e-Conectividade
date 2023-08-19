import json

def checkProducts (responseApi):
    responseApi = json.loads(responseApi)
    return responseApi

def amountAndProducts (product, shoppingList):

    if product != None:
        productExists = product.get("nome")
        if productExists != None:
            shoppingList["products"].append(product["nome"])
            shoppingList["amout"] += product["preco"]
