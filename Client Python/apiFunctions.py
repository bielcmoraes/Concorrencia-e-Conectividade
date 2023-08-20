import requests
import json

def get_request (resource):
    try:
        url = "http://localhost:8000/" + str(resource)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                json_data = response.json()
                return json_data
            except json.JSONDecodeError as e:
                print("Erro no JSON:", e)
    except Exception as e:
        print("ERROR COM REQUEST: ", e)

def post_request(argsList):
    shopping_list, result_queue = argsList
    url = "http://localhost:8000/checkout"
    response = requests.post(url, json=shopping_list)
    result_queue.put(response.status_code) #Adiciona a thread a fila de threads