import json

def checkProducts (responseApi):
    responseApi = json.loads(responseApi)
    return responseApi

def amountAndProducts(id, product, shoppingList):
    try:
        product = json.loads(product)
        product_name = product.get("nome")

        if product_name is not None:
            shoppingList["products"].append({"id": id, "nome": product_name})
            shoppingList["amout"] += product.get("preco", 0.0)
    except json.JSONDecodeError as e:
        pass
    except Exception as e:
        print("Other error:", e)