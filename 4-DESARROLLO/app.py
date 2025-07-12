from flask import Flask,Blueprint, jsonify, render_template,session,request ,redirect,url_for,send_from_directory,app
from flask_session import Session
import pandas as pd
from flask_cors import CORS
import requests
import json
from utils.Utilitarios import *
from utils.menus import *
import socket
import hashlib
import logging
# from database.models import *
from foto.routes import foto
from encuesta.routes import eval_bp
from admin.routes import admin

from config import DevelopmentConfig 
from config import apidb
from datetime import datetime
import shutil
import os
app = Flask(__name__) 
# Ruta al directorio de la app
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT=os.getcwd()

# Ruta absoluta al archivo SQLite
app.config['DATABASE'] = os.path.join(APP_ROOT, 'database', 'sena.db')
app.config['APP_ROOT'] = APP_ROOT
app.secret_key = 'BAD_SECRET_KEY'   
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# BASE_DIR=os.path.join(os.path.dirname(__file__))
# BASE_DIR=app['BASE_DIR']
RESPUESTAS = os.path.join(BASE_DIR, 'static/archivos/RESPUESTAS.csv')
app.config['apidb'] =  "http://127.0.0.1:5556"
apidb="http://127.0.0.1:5556"

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'evalf'
app.config['apidb'] =  "http://127.0.0.1:5556"

# DATABASE = os.path.join(BASE_DIR, 'database', 'sena.db')
# print(BASE_DIR)
# Registrando modulos Blueprint
app.register_blueprint(foto, url_prefix='/foto')
app.register_blueprint(eval_bp, url_prefix='/evalu')
app.register_blueprint(admin, url_prefix='/admin')

# app.config.from_object(DevelopmentConfig) 
au=Auditor(BASE_DIR)

@app.route('/') 
def raiz():   
    return render_template('indexppal.html')
@app.route('/0') 
def indexppal():  
    server_ip = socket.gethostbyname(socket.gethostname())
    session['server_ip']=server_ip
    au.registra(30,'Inicia Aplicacion') 
    # return render_template('login.html',server_ip=session['server_ip'])
    return redirect('/login')
    return render_template('indexppal.html',server_ip=session['server_ip'])
@app.route('/banner') 
def banner():  
    ip_local = socket.gethostbyname(socket.gethostname()) 
    return render_template('banner.html',ip_local=ip_local)
@app.route('/footer') 
def footer():   
    return render_template('footer.html')
@app.route('/centro') 
def centro():   
    return render_template('centro.html')
@app.route('/nada') 
def nada():   
    return render_template('nada.html')

@app.route('/menu') 
def menu():   
    sql="SELECT * FROM MENU WHERE ROL='APR' order by 2"
    # opci=Consultar(DATABASE,sql)
    opci=[{"idMenu":1,"LUGAR":1,"NOM": "INICIO","RUTA":"/login","ROL":"APR","ICONO":"fa fa-home"}]
    opci=[1,1,"INICIO","/login","APR","fa fa-home"]
    ip_local = socket.gethostbyname(socket.gethostname())
    return render_template('menu.html',mip=ip_local,opci=opci)
@app.route('/login') 
def login():
    return render_template('login.html')

@app.route('/acerca') 
def acerca():   
    return render_template('acerca.html')
def tipoUsuario(id):
    aa=f'{apidb}/u/datos/{id}'
    bb=requests.get(aa).json()
    Tipo=bb['TIPO']
    return Tipo
# def Consulte(clave):
#     # apidb=session['apidb']
#     aa=f'{apidb}{clave}'
#     datos=requests.get(aa).json()
#     return (datos)

@app.route('/valida' ,methods=['POST','GET']) 
def valida():
    usua=request.form.get('usua')
    pw=request.form.get('pw')
    pw1=hashlib.md5(pw.encode()).hexdigest()
    session['pw']=pw
    session['pw1']=pw1
    session['usua']=usua 
    # return Consulte(f'/u/1/{usua}')
    try:
        Tipo=Consulte(f'/u/1/{usua}')
        session['Tipo']=str(Tipo)
        menus=jsonify(miMenu(Tipo))
    except Exception as e:
        msgito="503 SERVIDOR NO DISPONIBLE: [{str(e)}]"
        regresa="/login"
        return render_template('alertas.html',msgito=msgito,regreso=regresa)
    
    aa=f'/u/{usua}/{pw1}' 
    daticos=Consulte(aa)
    if str(daticos) != '1' and (Tipo < 2):
        msgito="APRENDIZ O CLAVE ERRADOS**"
        regresa="/login"
        au.registra(30,msgito,usua)
        return render_template('alertas.html',msgito=msgito,regreso=regresa)

    if Tipo == 1:
    #    return "1"
       aa=f'{apidb}/u/{usua}' 
       daticos=requests.get(aa).json()
       session['Datos']=daticos
       return redirect('/maqueta') 
    elif Tipo == 2:
        # return "2"
        aa=f'{apidb}/u/{usua}' 
        daticos=requests.get(aa).json()
        session['Datos']=daticos
        return redirect('/foto')
    elif Tipo == 3 :
        session['usua']=usua
        au.registra(30,"Ingresa un administrador",session['usua'])
        return redirect('/admin')
    elif Tipo == 0 :
        msgito="USUARIO NO EXISTE**"
        regresa="/login"
        # au.registra(30,msgito)
        # *******
        return render_template('alertas.html',msgito=msgito,regreso=regresa)
    return "400"
def getInstructor(id):
    sql=f"SELECT NOMINST FROM FICHAINSTRUCTOR WHERE  dni='{id}'".format(str(id))
    datos=ConsultarUno(DATABASE,sql)
    return datos[0]
def getAprendiz(id):
    sql=f"select * from fichaprendiz where dnia='{id}'".format(str(id))
    datos=ConsultarUno(DATABASE,sql)
    dato={
        "FICHA":datos['FICHA']
    }
    return datos[0]
    # return render_template('carga.html',N=N,datos=datos)

@app.route('/encuesta')
def encuesta():
    usua=session["usua"]
    # usua=id
    # 

    apr=requests.get(f'{apidb}/u/datos/{usua}')
    # session["ficha"]=apr['FICHA']
    apr1=apr.json()
    ficha=apr1['FICHA']
    # usua=apr1['DNI']
    a=f'{apidb}/i/2/{ficha}/{usua}'
    
    datos=requests.get(a).json()
    return render_template("carga.html",N=1,datos=datos,apr=datos)
@app.route('/descargar')
def descargar():
    # au.registra(30,"Descarga Respuestas")
    return send_from_directory('static/archivos', 'RESPUESTAS.csv', as_attachment=True)
@app.route('/descargarlog')
def descargarlog():
    fecha=datetime.now()
    fe=str(fecha.year)+str(fecha.month)+str(fecha.day)
    
    # au.registra(30,"Descarga Log de Transacciones")
    # return fe
    # 'static/archivos/'+fe+'.txt'
    return send_from_directory('static/archivos', fe+'.txt',as_attachment=True)

@app.route('/cargar')
def cargar():
    return send_from_directory('static/archivos', 'CARGA.xlsx', as_attachment=True)
@app.route('/resp') 
def resp():   
    print('DESCARGANDO RESPUESTAS')
    sql="SELECT idFICHA,TITULACION,PREGUNTA,RESPUESTA FROM THEVAL"
    datos=pd.DataFrame(ConsultarD(DATABASE,sql))
    # Guardar el archivo
    datos.to_csv(RESPUESTAS, index=False)

# O cambia el nombre en send_from_directory a minúsculas
    print("PROCESO TERMINADO")
    return redirect('/descargar')


@app.route('/CargaInicial', methods = ['GET'])   
def CargaInicial():
    au.registra(30,'Carga Inicial de la base de datos terminada con exito')
    from Carga import Cargando
    aux= Cargando()
    return render_template("alertas.html",msgito=aux, regreso="/menuadmin")
@app.route('/menuadmin')
def menuadmin():
    au.registra(30,'ingresa menuadmin',session['usua'])
    return render_template('menuadmin.html')
@app.route('/menu1')
def menu1():
    # au.registra(30,'ingresa menuadmin',session['usua'])
    return render_template('menu1.html')

@app.route('/aprendiz')
def aprendiz():
    return render_template("aprendices.html")
@app.route('/construir')
def construir():
    msgito="401 - PAGINA EN CONSTRUCCION"
    
    return render_template("alertas.html",msgito=msgito,regreso='#')
@app.route('/salir')
def salir():
    msgito="SALIENDO DEL APLICATIVO"
    au.registra(30,"Saliendo el administrador de la encuesta",session['usua'])
    return render_template("alertas.html",msgito=msgito,regreso='/saliendo')
@app.route('/saliendo')
def saliendo():
    au.registra(30,"Saliendo de la encuesta",session['usua'])       
    return render_template("saliendo.html")

def pagina_no_encontrada(error):
    msgito="RUTA NO ENCONTRADA:"+str(error)
    return render_template("alertas.html",msgito=msgito,regreso='#')
    return "<h1>RUTA NO ENCONTRADA</h1>", 404
def metodo_no_aceptado(error):
    msgito="405 METODO NO PERMITIDO"
    return render_template("alertas.html",msgito=msgito,regreso='#')
    # return "<h1>Este metodo no esta permitido para esta ruta</h1>", 423
def servicio_no_dispoible(error):
    msgito="503 SERVIDOR NO DISPONIBLE *"
    return render_template("alertas.html",msgito=msgito,regreso='#')
def servicio_errado(error):
    msgito="500 ALGO SALIO MAL"
    return render_template("alertas.html",msgito=msgito,regreso='#')
@app.route('/maqueta')
def maqueta():
    # au.registra(30,'ingresa menuadmin',session['usua'])   
    return render_template('maqueta1.html')


if __name__=='__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(405, metodo_no_aceptado)
    app.register_error_handler(503, servicio_no_dispoible)
    app.register_error_handler(500, servicio_errado)
    app.run(debug=True,port=5000)