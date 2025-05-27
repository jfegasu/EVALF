from flask import Flask, request, jsonify
from peewee import *
from peewee import fn
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

# db = SqliteDatabase(DATABASE)
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
def Ejecutar(db,sql):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return '200' 
    except Exception as e:
        print(e)
        return("400")
@app.route('/u/1/<email>', methods=['GET']) # Detemina tipo de usuario
def TipoUsuario(email):
    email = email.strip().lower()
    sql=f"SELECT COUNT(*) CANT FROM Fichaaprendiz    WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    # total = FichaAprendiz.select(FichaAprendiz.EMAIL).where(fn.LOWER(FichaAprendiz.EMAIL) == email).count()
    # print("oooo>",total)
    if datos[0]:
        return str(1)
    sql=f"SELECT COUNT(*) CANT FROM fichainstructor WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    if datos[0]:
        return str(2)
    sql=f"SELECT COUNT(*) CANT FROM admin WHERE EMAIL='{email}'".format(email)
    datos=ConsultarUno(DATABASE,sql)
    if datos[0]:
        return str(3)
    return str(-1)
@app.route('/a/0/<email>', methods=['GET']) # Entrega ficha del aprendiz
def Aprendiz(email):
    sql=f"SELECT * FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    # return datos
    return jsonify({"FICHA":datos[0][1],"DNI":datos[0][2],"NOMBRE":datos[0][3],"ESTADOAP":datos[0][4],"EMAIL":datos[0][6]})

@app.route('/a/1/<email>', methods=['GET']) # Entrega ficha del aprendiz
def FichaAprendiz1(email):

    Aux=FichaAprendiz.get(FichaAprendiz.EMAIL==email)
    return Aux.FICHA
    
@app.route('/a/2/<email>', methods=['GET']) # Entrega el DNI del aprendiz
def DNIAprendiz(email):
    Aux=FichaAprendiz.get(FichaAprendiz.EMAIL==email)
    return Aux.DNIA

@app.route('/a/3/<email>', methods=['GET']) # Entrega el estado del aprendiz
def EstaAprendiz(email):
    Aux=FichaAprendiz.get(FichaAprendiz.EMAIL==email)
    return str(Aux.ESTADOAP)

@app.route('/a/4/<email>', methods=['GET']) # Entrega el estado del aprendiz
def NomAprendiz(email):
    Aux=FichaAprendiz.get(FichaAprendiz.EMAIL==email)
    return Aux.NOMBREAP
    
@app.route('/u/2/<email>/<pwd>', methods=['GET']) # Valida clave de acceso a usuario
def ValidaUsuario(email,pwd):
    Tipo=TipoUsuario(email)
    print("-->",Tipo)
    if Tipo:
        total = FichaAprendiz.select().where((FichaAprendiz.EMAIL==email) and (FichaAprendiz.PWDAP==pwd)).count()
        if total:
            return "1"
        else:
            return "0"
    if Tipo=="2":
        total = FichaInstructor.select().where((FichaInstructor.EMAIL==email) and (FichaInstructor.PWD==pwd)).count()
        if total:
            return "1"
        else:
            return "0"
    return jsonify({"ERROR":401})

@app.route('/u/<email>', methods=['GET']) # Datos de usuario
def DatosUsuario(email):
    Tipo=TipoUsuario(email)
    if Tipo=="1":
        datos = FichaAprendiz.get(FichaAprendiz.EMAIL==email)
        return jsonify({"FICHA":datos.FICHA,"DNI":datos.DNIA,"NOM":datos.NOMBREAP,"EMAIL":datos.EMAIL,"ESTADO":datos.ESTADOAP,"TITULACION":datos.TITULACION})
    if Tipo=="2":
        sql=f"SELECT  * FROM FICHAINSTRUCTOR WHERE EMAIL='{email}'".format(email)
        datos=ConsultarUno(DATABASE,sql)
        datos = FichaInstructor.get(FichaInstructor.EMAIL==email)
        return jsonify({"FICHA":datos.FICHA,"DNI":datos.DNI,"NOM":datos.NOMINST,"EMAIL":datos.EMAIL})

@app.route('/i/1/<email>', methods=['GET']) # Instructores por evaluar por el aprendiz
def InstructorUsuarioXEvaluar(email):
    Ficha=FichaAprendiz1(email)
    DNI=DNIAprendiz(email)
    sql=f"SELECT * FROM FICHAINSTRUCTOR FI WHERE FI.FICHA={Ficha} AND FI.DNI NOT IN (SELECT idINSTRUCTOR FROM THEVAL WHERE IDFICHA={Ficha} AND idAPRENDIZ={DNI})".format(Ficha,DNI)
    datos=Consultar(DATABASE,sql)
    # return datos
    subquery = TheVal.select(TheVal.idINSTRUCTOR).where(
    (TheVal.idFICHA == Ficha) & (TheVal.idAPRENDIZ == DNI))
    
    
    query = FichaInstructor.select().where(
    (FichaInstructor.FICHA == Ficha) &
    (FichaInstructor.DNI.not_in(subquery))
    )
    return str(query)

@app.route('/p', methods=['GET']) # Instructores por evaluar por el aprendiz
def Preguntas():
    try:
        datos = Pregunta.select().where(Pregunta.ESTADO==1)  # puedes agregar filtros si deseas

        resultado = []
        for fila in datos:
            resultado.append({
                "ID":fila.id,
                "DESCRIPCION": fila.DESCRIPCION,
                "VALORES": fila.VALORES
            })

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/i/2/<ficha>', methods=['GET']) # Instructores por evaluar por el aprendiz
def InstructoresXFicha(ficha):
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE FICHA={ficha}".format(ficha)
    datos=Consultar(DATABASE,sql)
    return datos
import sqlite3

@app.route('/act', methods=['POST','GET'])  # Instructores por evaluar por el aprendiz
def inserta():
    datos = request.get_json()
    a = datos['ACTIVIDAD']
    b = datos['DNIA']
    c = datos['DNII']
    D = datos['FICHA']

    print(a)
    sql = "INSERT INTO ASISTENCIA(ACTIVIDAD, DNIA, DNII,FICHA) VALUES (?, ?, ?,?)"
    print(DATABASE)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, (a, b, c))
    conn.commit()
    conn.close()
    
    return "200"

# app.py (continuación)
# from modelos import Asistencia

from flask import Flask, request, jsonify

@app.route('/act1', methods=['POST'])
def insertar_asistencia():
    try:
        data = request.get_json()

        asistencia = Asistencia.create(
            actividad=data.get('actividad', 'BASE DE DATOS'),
            dnia=data.get('dnia', '1234'),
            dnii=data.get('dnii', '5678'),
            ficha=data.get('ficha', '90'),
            falla=str(data.get('falla', '1'))
        )
        return jsonify({"status": "ok", "id": asistencia.id}), 200
    except Exception as e:
        print("[ERROR]:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/inst/<pficha>/<paprendiz>', methods=['GET'])
def noEvaluados(pficha, paprendiz):
    # sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE FICHA='{pficha}' AND DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{pficha}' AND IDAPRENDIZ='{paprendiz}')".format(pficha,paprendiz)
    # sql=f"SELECT * FROM VINSTRUCTORESP WHERE FICHA={pficha} AND DNIAP={paprendiz}".format(pficha,paprendiz)
    # print(sql)
    # datos=Consultar(DATABASE,sql)
    # return jsonify(datos)
    # datos=  VINSTRUCTORESP.select().where((VINSTRUCTORESP.FICHA==pficha) & (VINSTRUCTORESP.DNIAP==paprendiz))
    datos = VInstructorEsp.select().where((VInstructorEsp.ficha==pficha) & (VInstructorEsp.dniap==paprendiz))
    resultado = [{
        'titulacion': d.titulacion,
        'ficha': d.ficha,
        'dninst': d.dninst,
        'emailinst': d.emailinst,
        'nominst': d.nominst,
        'dniap': d.dniap,
        'nombreap': d.nombreap,
        'emailap': d.emailap
    } for d in datos]
    return jsonify(resultado)
#     try:
#             query = (FichaInstructor.select(
#             #  FichaInstructor.TITULACION,
#              FichaInstructor.FICHA,
#              FichaInstructor.DNI,
#              FichaInstructor.EMAIL.alias('EMAILINST'),
#              FichaInstructor.NOMINST,
#              FichaAprendiz.TITULACION,
#              FichaAprendiz.DNIA.alias('DNIAP'),
#              FichaAprendiz.NOMBREAP,
#              FichaAprendiz.EMAIL.alias('EMAILAP')
#          ).join(FichaAprendiz, on=(FichaInstructor.FICHA == FichaAprendiz.FICHA)).where(FichaInstructor.DNI.not_in(
#              TheVal.select(TheVal.idINSTRUCTOR).distinct()
#              .where((TheVal.idFICHA == FichaInstructor.FICHA) &
#                     (TheVal.idAPRENDIZ == FichaAprendiz.DNIA))
#          ))
#          .distinct()
# )
#             resultado = []
#             for fila in query:
#                 resultado.append({
#                     "FICHA": fila.FICHA,
#                     "DNI": fila.DNI,
#                     "EMAILINST":fila.EMAILINST
                    
                    
#                 })

#             return jsonify(resultado)
    # except Exception as e:
    #         return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True,port=5556)
    