import requests
from flask import Flask, request, jsonify
# from config import *
class Api:
    def __init__(self,url="http://127.0.0.1:5556"):
        self.url = url  
        self.Estado=None     
    def ConsultaApi(self,clave):
        response = requests.get(self.url+clave) 
        self.Estado=response.status_code
        return  response.text
    def PostApi(self,clave,datos):
        response = requests.post(self.url+clave, json=datos)  
        return response.status_code   
# print("********",apidb,"************")
Consul=Api()
# print(Consul.ConsultaApi('/p') )  
data={
    "ACTIVIDAD":"TESTING",
    "DNIA":12345,
    "DNII":5678,
}
print(Consul.PostApi('/act',data))

# url = "http://127.0.0.1:5556/p"
# response = requests.get(url)

# print("Código de estado:", response.status_code)
# print("Respuesta:", response.text)


