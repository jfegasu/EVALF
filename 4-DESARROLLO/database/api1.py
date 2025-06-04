from flask import Flask, request, jsonify,session
from peewee import *
from peewee import fn
from models import *
from playhouse.shortcuts import model_to_dict
from peewee import fn
import os
import sqlite3
import json
import sentry_sdk

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
@app.route('/u/1/<id>', methods=['GET']) # Detemina tipo de usuario
def TipoUsuario(id):
    cantidad = FichaAprendiz.select().where(FichaAprendiz.DNIA == id).count()
    if cantidad:
        return str(cantidad)
    cantidad = FichaInstructor.select().where(FichaInstructor.DNI == id).count()
    if cantidad:
        return str(cantidad)
    cantidad = Admin.select().where(Admin.NOM == id).count()
    if cantidad:
        return str(cantidad)
    
    return str(0)

@app.route('/yyyy/<id>', methods=['GET'])
def UsuarioAprendiz(id):
    try:
        datos = FichaAprendiz.get(FichaAprendiz.DNIA == id)
        aprendiz_data = {
            "TIPO": 1,
            "FICHA": datos.FICHA,
            "DNI": datos.DNIA,
            "NOMBRE": datos.NOMBREAP,
            "ESTADOAP": datos.ESTADOAP,
            "EMAIL": datos.EMAIL
        }
        session['datos'] = aprendiz_data
        return session['datos']
    except FichaAprendiz.DoesNotExist:
        return jsonify({"Error": f"Usuario {id} no encontrado"}), 401
    except Exception as e:
        # Puedes loguear `str(e)` aquí si deseas
        return jsonify({"Error": "Error interno del servidor"}), 500
    
def UsuarioInstructor(id):
    try:
        datos=FichaInstructor.get(FichaInstructor.DNI==id)
        return jsonify({"TIPO":2,"FICHA":datos.FICHA,"DNI":datos.DNI,"NOMBRE":datos.NOMINST,"EMAIL":datos.EMAIL})
    except Exception as e:
        print(e)
        return jsonify({"Error":f"Usuario {id} no encontrado "})

@app.route('/u/<id>/<pwd>', methods=['GET'])  # Entrega Datos del Usuario
def AllUsuario(id,pwd):
    tipo = TipoUsuario(id)

    if tipo == "1":
        datos = UsuarioAprendiz(id)
        return session['datos']
    elif tipo== "2":
        datos = UsuarioInstructor(id)
        return session['datos']
    #     if isinstance(datos, tuple):  # Significa que hubo un error (jsonify, código)
    #         return datos
    #     return jsonify(datos)
    # else:
    #     return jsonify({"Error": f"Usuario {id} no es un aprendiz autorizado"}), 403
    
    # return jsonify( "FICHA":datos[0][1],"DNI":datos[0][2],"NOMBRE":datos[0][3],"ESTADOAP":datos[0][4],"EMAIL":datos[0][6]})
@app.route('/a/0/<email>', methods=['GET']) # Entrega ficha del aprendiz
def Aprendiz(email):
    sql=f"SELECT * FROM FICHAAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    datos=FichaAprendiz.select().where(FichaAprendiz.EMAIL)
    return jsonify({"FICHA":datos.FICHA})
    # return jsonify( "FICHA":datos[0][1],"DNI":datos[0][2],"NOMBRE":datos[0][3],"ESTADOAP":datos[0][4],"EMAIL":datos[0][6]})

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

@app.route('/i/2a/<ficha>', methods=['GET']) # Instructores por evaluar por el aprendiz
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

@app.route('/i/2/<pficha>/<paprendiz>', methods=['GET'])
def noEvaluados(pficha, paprendiz):
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





# or, without the decorator


@app.route('/i/e/<email>', methods=['GET'])
def obtener_instructor_por_email(email):
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    return jsonify(datos),404
def pagina_no_encontrada(error):
    return "<h1>RUTA NO ENCONTRADA</h1>", 404
def metodo_no_aceptado(error):
    return "<h1>Este metodo no esta permitido para esta ruta</h1>", 423
def servicio_no_dispoible(error):
    return "<h1>Este metodo no esta permitido para esta ruta</h1>", 423
if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(405, metodo_no_aceptado)
    app.register_error_handler(503, servicio_no_dispoible)
    app.run(debug=True,port=5556)
    
