import requests
from flask import Flask, request, jsonify

class Api:
    def __init__(self, url="http://127.0.0.1:5556"):
        self.url = url  
        self.Estado = None     

    def ConsultaApi(self, clave):
        try:
            response = requests.get(self.url + clave)
            self.Estado = response.status_code
            response.raise_for_status()  # Lanza excepción para errores HTTP
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[ERROR - GET] {e}")
            return None

    def PostApi(self, clave, datos):
        try:
            response = requests.post(self.url + clave, json=datos)
            self.Estado = response.status_code
            response.raise_for_status()
            return response.status_code
        except requests.exceptions.RequestException as e:
            print(f"[ERROR - POST] {e}")
            return None

Consul=Api()
# print(Consul.ConsultaApi('/p') )  
data={
    "ACTIVIDAD":"TESTING",
    "DNIA":12345,
    "DNII":5678,
    "FICHA":222
}
print(Consul.PostApi('/act',data))

# url = "http://127.0.0.1:5556/p"
# response = requests.get(url)

# print("Código de estado:", response.status_code)
# print("Respuesta:", response.text)


