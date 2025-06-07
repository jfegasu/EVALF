import enum
from flask import Flask,redirect,jsonify
import requests
from playhouse.shortcuts import model_to_dict
import json
from database.models import *

apidb="http://127.0.0.1:5556"
class tipo_usuario(enum.Enum):
    APRENDIZ=1
    INSTRUCTOR=2
    ADMIN=3

class Usuario:
    def __init__(self,papidb="http://127.0.0.1:5556"):
         self.apidb=papidb
    def get_tipo_usuario(self,id):
        datos = requests.get(f'{self.apidb}/u/1/{id}').json()
        return datos
    def get_all_datos_usuario(self, id,ficha=0):
        Tipo = self.get_tipo_usuario(id)    
        if Tipo == 1:
            datos = FichaAprendiz.get(FichaAprendiz.DNIA == id)
            mdatos={
                "FICHA":datos.FICHA,
                "NOMBRE":datos.NOMBREAP,
                "DNI":datos.DNIA,
                "TITULACION":datos.TITULACION,
                "TIPO":1
            }
            return mdatos
        elif Tipo == 2:
            datos = FichaInstructor.get((FichaInstructor.DNI == id) & (FichaInstructor.FICHA == ficha))
            mdatos={
                "FICHA":datos.FICHA,
                "NOMBRE":datos.NOMINST,
                "DNI":datos.DNI,
                "TIPO":2
            }
            return mdatos
        elif Tipo == 3:
            datos = Admin.get(Admin.NOM == id)
            mdatos={
                "NOMBRE":"ADMINISTRADOR",
                "TIPO":3
            }
            return mdatos
        else: 
            falla={"Tipo":Tipo,"Error":"Usuario no encontrado"}
            return falla

if __name__=='__main__':
    OUsuario =Usuario()
    print(OUsuario.get_all_datos_usuario(1234))
        