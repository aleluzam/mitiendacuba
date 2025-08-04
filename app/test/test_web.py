import requests

ENDPOINT = "https://mitienda-cuba.com"

# response = requests.get(ENDPOINT)
# print (response)
# print(response.json())

# test que verifica la primera llamada a la api
def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    
def test_can_create_user():
    payload = {"username": "testting",
            "name": "Testting",
            "last_name": "Probando",
            "mobile": "53011238",
            "mail": "alzzla@gmail.com",
            "password": "53011238"}
    
    response = requests.post(ENDPOINT + "/auth/register", json=payload)
    assert response.status_code == 201    
    
    if response.status_code == 201:
        data = response.json()
        print(data)
    

    
