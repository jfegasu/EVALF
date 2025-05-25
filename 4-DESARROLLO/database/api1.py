from flask import Flask, request, jsonify
from peewee import *
from models import *
from playhouse.shortcuts import model_to_dict
from peewee import fn
import os
import sqlite3
import json
app = Flask(__name__) 
app.secret_key = 'BAD_SECRET_KEY'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR,  'sena.db')

db = SqliteDatabase(DATABASE)
def Consultar(db,sql):
    conn = sqlite3.connect(db)
    # conn.row_factory = sqlite3.Row  # Esto permite acceder a los resultados como diccionarios
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

def ConsultarUno(db,sql):
    conn = sqlite3.connect(db)
    
    cursor = conn.cursor()
    cursor.execute(sql)
    output = cursor.fetchone() 
    conn.close()
    return output 

@app.route('/u/1/<email>', methods=['GET']) # Detemina tipo de usuario
def TipoUsuario(email):
    
    sql=f"SELECT COUNT(*) CANT FROM VAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    if datos[0]:
        return str(1)
    sql=f"SELECT COUNT(*) CANT FROM VINSTRUCTOR WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    if datos[0]:
        return str(2)
    sql=f"SELECT COUNT(*) CANT FROM VADMIN WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    if datos[0]:
        return str(3)
    return str(0)
@app.route('/a/0/<email>', methods=['GET']) # Entrega ficha del aprendiz
def Aprendiz(email):
    sql=f"SELECT * FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    # return datos
    return jsonify({"FICHA":datos[0][1],"DNI":datos[0][2],"NOMBRE":datos[0][3],"ESTADOAP":datos[0][4],"EMAIL":datos[0][6]})

@app.route('/a/1/<email>', methods=['GET']) # Entrega ficha del aprendiz
def FichaAprendiz(email):
    sql=f"SELECT FICHA FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    return jsonify({"FICHA":datos[0]})
    
@app.route('/a/2/<email>', methods=['GET']) # Entrega el DNI del aprendiz
def DNIAprendiz(email):
    sql=f"SELECT DNIA FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    return jsonify({"DNI":datos[0]})

@app.route('/a/3/<email>', methods=['GET']) # Entrega el estado del aprendiz
def EstaAprendiz(email):
    sql=f"SELECT ESTADOAP FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    return jsonify({"ESTADOAP":datos[0]})
@app.route('/a/4/<email>', methods=['GET']) # Entrega el estado del aprendiz
def NomAprendiz(email):
    sql=f"SELECT NOMBREAP FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    return jsonify({"NOMBRE":datos[0]}),200
    
@app.route('/u/2/<email>/<pwd>', methods=['GET']) # Valida clave de acceso a usuario
def ValidaUsuario(email,pwd):
    Tipo=TipoUsuario(email)
    if Tipo=="1":
        sql=f"SELECT COUNT(*) CANT FROM FICHAAPRENDIZ WHERE EMAIL='{email}' AND PWDAP='{pwd}'".format(email,pwd)
        datos=ConsultarUno(DATABASE,sql)
        if datos[0]:
            return "1"
        else:
            return "0"
    if Tipo=="2":
        sql=f"SELECT COUNT(*) CANT FROM FICHAINSTRUCTOR WHERE EMAIL='{email}' AND PWD='{pwd}'".format(email,pwd)
        datos=ConsultarUno(DATABASE,sql)
        if datos[0]:
            return "1"
        else:
            return "0"
    return jsonify({"ERROR":401})

@app.route('/u/<email>', methods=['GET']) # Datos de usuario
def DatosUsuario(email):
    Tipo=TipoUsuario(email)
    if Tipo=="1":
        sql=f"SELECT * FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
        datos=ConsultarUno(DATABASE,sql)
        return jsonify({"FICHA":datos[1],"DNI":datos[2],"NOM":datos[3],"EMAIL":datos[6],"TITULACION":datos[7]})

    if Tipo=="2":
        sql=f"SELECT  * FROM FICHAINSTRUCTOR WHERE EMAIL='{email}'".format(email)
        datos=ConsultarUno(DATABASE,sql)
        return jsonify({"FICHA":datos[2],"DNI":datos[1],"NOM":datos[0],"EMAIL":datos[3]})

    return jsonify({'Error':"Correo no se encuentra"})

@app.route('/i/1/<email>', methods=['GET']) # Instructores por evaluar por el aprendiz
def InstructorUsuarioXEvaluar(email):
    Ficha=FichaAprendiz(email)
    DNI=DNIAprendiz(email)
    sql=f"SELECT * FROM FICHAINSTRUCTOR FI WHERE FI.FICHA={Ficha} AND FI.DNI NOT IN (SELECT idINSTRUCTOR FROM THEVAL WHERE IDFICHA={Ficha} AND idAPRENDIZ={DNI})".format(Ficha,DNI)
    datos=Consultar(DATABASE,sql)
    return datos

@app.route('/p', methods=['GET']) # Instructores por evaluar por el aprendiz
def Preguntas():
    sql=f"SELECT * FROM PREGUNTA WHERE ESTADO=1"
    datos=Consultar(DATABASE,sql)
    return datos

@app.route('/i/2/<ficha>', methods=['GET']) # Instructores por evaluar por el aprendiz
def InstructoresXFicha(ficha):
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE FICHA={ficha}".format(ficha)
    datos=Consultar(DATABASE,sql)
    return datos



if __name__ == '__main__':
    app.run(debug=True,port=5556)