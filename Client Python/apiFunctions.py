import requests
import json

def get_request(resource):
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

def post_request(data_post, url):
    
    headers = {
    "Content-Type": "application/json"  # Define o tipo de conteúdo como JSON
    }
    
    data_post = json.dumps(data_post) #Converte o dicionário pra json

    response = requests.post(url, data_post, headers=headers)

    if response.status_code == 201:
        return {"response": response.text}
    else:
        return {"error": response.text}