from flask import Flask,Blueprint, jsonify, render_template,session,request ,redirect,url_for,send_from_directory
from flask_session import Session
import pandas as pd
from flask_cors import CORS
import requests
import json
from utils.Utilitarios import *
import socket
import hashlib
import logging
from config import DevelopmentConfig 
from datetime import datetime
import shutil
import os
app = Flask(__name__) 
app.secret_key = 'BAD_SECRET_KEY'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'sena.db')
RESPUESTAS = os.path.join(BASE_DIR, 'static/archivos/RESPUESTAS.csv')
app.config['apidb'] =  "http://127.0.0.1:5556"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['BASE_DIR']=BASE_DIR
# app.config.from_object(DevelopmentConfig) 
#au=Auditor(app.config['BASE_DIR'])

@app.route('/') 
def raiz():   
    return render_template('inicio.html')
@app.route('/0') 
def indexppal():  
    server_ip = socket.gethostbyname(socket.gethostname())
    session['server_ip']=server_ip
    # au.registra(30,'Inicia Aplicacion') 
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

@app.route('/menu') 
def menu():   
    sql="SELECT * FROM MENU WHERE ROL='APR' order by 2"
    opci=Consultar(DATABASE,sql)
    ip_local = socket.gethostbyname(socket.gethostname())
    return render_template('menu.html',mip=ip_local,opci=opci)
@app.route('/login') 
def login():
    return render_template('login.html')

@app.route('/acerca') 
def acerca():   
    return render_template('acerca.html')
def tipoUsuario(correo):
    return ConsultarDB('/u/1/'+correo)

@app.route('/valida' ,methods=['POST','GET']) 
def valida():   
    N=1
    usua=request.form.get('usua')
    # au.registra(30,'Intento de logueo',usua)
    
    pw=request.form.get('pw')
    Tipo=tipoUsuario(usua)
    if Tipo<3:
        pw1=hashlib.md5(pw.encode()).hexdigest()
    if Tipo==1:
        sql=f"SELECT count(*) FROM FICHAPRENDIZ WHERE PWDAP='{pw1}' AND EMAIL='{usua}'".format(usua,pw1)
        hay=ConsultarDB(f"/u/2/{usua}/{pw1}".format(usua,pw1))
        if hay:
            N=1
            sql=f"SELECT * FROM FICHAPRENDIZ WHERE PWDAP='{pw1}' AND EMAIL='{usua}'".format(usua,pw1)
            aprendiz=ConsultarDB(f"/u/{usua}".format(usua))
            
            session['ficha']=aprendiz['FICHA']
            session['nombreap']= aprendiz['NOM']  
            session['titulacion']= aprendiz['TITULACION']   
            session['dnia']= aprendiz['DNI']  
            # return str(aprendiz)
            F=aprendiz['FICHA']
            A=aprendiz['DNI'] 
            # sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
            # datos=Consultar(DATABASE,sql)
            datos=ConsultarDB(f"/i/2/{F}/{A}".format(F,A))
            
            apr={
                "ficha":session['ficha'],
                "aprendiz":session['nombreap'],
                "titulacion":session['titulacion'],
                "dnia":session['dnia']
            }
            print("---->",datos)
            # au.registra(30,'Ingresa:'+session['nombreap'])
            return render_template('carga.html',N=1,datos=datos,apr=apr)
  
        else:
            msgito="APRENDIZ O CLAVE ERRADOS**"
            regresa="/login"
            # au.registra(30,msgito)
            # *******
            return render_template('alertas.html',msgito=msgito,regreso=regresa)
    elif Tipo==2:
        sql=f"/i/e/{usua}".format(usua)
        
        datos=ConsultarDB(sql)

        return render_template('foto.html',datos=datos)
        
        
    elif Tipo==3:
        session['usua']=usua
        # au.registra(30,"Ingresa un administrador",session['usua'])
        return render_template('menuadmin.html')
    if Tipo['Tipo']==0:
        msgito="USUARIO NO EXISTE**"
        regresa="/login"
        # au.registra(30,msgito)
        # *******
        return render_template('alertas.html',msgito=msgito,regreso=regresa)
    
    sql=f"SELECT count(*) FROM FICHAPRENDIZ WHERE PWDAP='{pw1}' AND EMAIL='{usua}'".format(usua,pw1)
    hay=ConsultarUno(DATABASE,sql)
    if hay[0]>0:
        N=1
        sql=f"SELECT * FROM FICHAPRENDIZ WHERE PWDAP='{pw1}' AND EMAIL='{usua}'".format(usua,pw1)
        aprendiz=ConsultarUno(DATABASE,sql)
        session['ficha']=aprendiz[0]
        session['nombreap']= aprendiz[2]   
        session['titulacion']= aprendiz[6]   
        session['dnia']= aprendiz[1]  
        # return str(aprendiz)
        F=aprendiz[0]
        A=aprendiz[1] 
        sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
        datos=Consultar(DATABASE,sql)
        
        apr={
            "ficha":session['ficha'],
            "aprendiz":session['nombreap'],
            "titulacion":session['titulacion'],
            "dnia":session['dnia']
        }
        render_template('carga.html',N=N,datos=datos,apr=apr)
    sql=f"SELECT count(*) FROM FICHAPRENDIZ WHERE PWDAP='{pw1}' AND EMAIL='{usua}'".format(usua,pw1)
    hay=ConsultarUno(DATABASE,sql)
    

    # return str(hay)
    try:
        hay=ConsultarUno(DATABASE,f"SELECT count(*) FROM FICHAPRENDIZ WHERE DNIA='{usua}' AND EMAIL='{pw1}'".format(usua,pw1))
    except Exception as e:
        msgito="USUARIO O CLAVE ERRADOS**"
        regresa="/login"
        # au.registra(30,'USUARIO O CLAVE ERRADOS')
        return render_template('login.html',msgito=msgito,regreso=regresa)
    
    hay=hay[0]
    # return "->"+str(hay)
    if hay=="0":
        # au.registra(30,'USUARIO O CLAVE ERRADOS')
        return render_template("alertas.html",msgito="USUARIO O CLAVE INCORRECTO***",regreso="/login")
    
    
    
    
    try:
        sql=f"SELECT * FROM FICHAPRENDIZ WHERE EMAIL='{usua}' AND PWDAP='{pw1}'".format(usua,pw)
        aprendiz=ConsultarUno(DATABASE,sql)
        session['ficha'] = aprendiz[0]
        session['dnia'] = aprendiz[1]
        session['nombreap'] = aprendiz[2]
        session['titulacion'] = aprendiz[6]
        
    except:
        # au.registra(30,'USUARIO O CLAVE ERRADOS')
        msgito="USUARIO O CLAVE ERRADOS**"
        regresa="/login"
        return render_template('alertas.html',msgito=msgito,regreso=regresa)
    
    F=session['ficha']
    A=session['dnia']
    N=1
    sql=f"SELECT count(*) FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
    # au.registra(30,'INGRESO ',session['nombreap'])

    hay=ConsultarUno(DATABASE,sql)

    if hay[0]=="0":
        msgito="NO HAY INSTRUCTORES PARA EVALUAR"
        # au.registra(30,msgito,session['nombreap'])

        regresa="/login"
        return render_template('alertas.html',msgito=msgito,regreso=regresa)
    else:
        sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
        datos=Consultar(DATABASE,sql)
        apr={
            "ficha":session['ficha'],
            "aprendiz":session['nombreap'],
            "titulacion":session['titulacion'],
            "dnia":session['dnia']
        }
        # au.registra(30,str(apr),session['nombreap'])
        session['apr']=apr
        return render_template('carga.html',N=N,datos=datos,apr=apr)
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
# @app.route('/otro' ,methods=['POST','GET']) 
# def otro():
#     hay=ConsultarUno(DATABASE,f"SELECT count(*) FROM FICHAPRENDIZ WHERE DNIA='{usua}' AND EMAIL='{pw}'".format(usua,pw))
#     hay=hay[0]
#     if hay=="0":
#         session[usua]=usua

#         return render_template("alertas.html",msgito="USUARIO O CLAVE INCORRECTO",regreso="/login")
#     sql=f"SELECT * FROM FICHAPRENDIZ WHERE EMAIL='{usua}' AND PWDAP='{pw}'".format(usua,pw)
#     aprendiz=ConsultarUno(DATABASE,sql)
#     session['ficha'] = aprendiz[0]
#     session['dnia'] = aprendiz[1]
#     session['nombreap'] = aprendiz[2]
#     session['titulacion'] = aprendiz[6]
#     F=session['ficha']
#     A=session['dnia']
#     N=1
#     sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
#     datos=Consultar(DATABASE,sql)
#     session['instructor'] = datos[1]
#     session['ninstructor'] = datos[0]

    return render_template('carga.html',N=N,datos=datos)

@app.route('/eval/1/<I>' ,methods=['POST','GET']) 
def eval1(I):  
    F=session['ficha']
    A=session['dnia']
    sql=f"SELECT * FROM THEVAL WHERE idFICHA={F} AND idAPRENDIZ={A}".format(F,A)
    datos=ConsultarUno(DATABASE,sql)
    
    session['instructor']=datos[3]
    I=session['instructor']
    datos=[N,F,I,A]
    return render_template('carga.html',N=1,datos=datos)
@app.route('/ev/2/<I>' ,methods=['POST','GET']) 
def eval2a(I):  
    # F=session['ficha']
    F=3147246
    # A=session['dnia']
    A=1013106019
    # I=session['instructor']
    N=2
    datos=[2,F,I,A]
    print("__________________________>",N)
    preg=Consultar(DATABASE,'SELECT * FROM PREGUNTA WHERE ESTADO=1')
    hay=len(preg)
    # au.registra(30,'ENTRA A EVALUAR A: '+getInstructor(I))
    apr={
            "ficha":session['ficha'],
            "aprendiz":session['nombreap'],
            "titulacion":session['titulacion'],
            "dnia":session['dnia']
        }
    session['apr']=apr
    
    return render_template('carga.html',N=2,datos=datos,preg=preg,hay=hay,nomi=getInstructor(I),apr=apr)
@app.route('/eval/3/<I>' ,methods=['POST','GET']) 
def eval(I):  
    F=session['ficha']
    A=session['dnia']
    T=session['titulacion']
    TRIMESTRE=obtener_trimestreT(datetime.now())
    
    # I=session['instructor']
    
    conta = int(request.form.get('conta'))

    for i in range(1, conta + 1):  # Asegúrate de incluir el último valor
        Resp=request.form.get('R' + str(i))
        Preg=request.form.get('P' + str(i))
        sql=f"insert into THEVAL(idINSTRUCTOR,idFICHA,idAPRENDIZ,PREGUNTA,RESPUESTA,TITULACION,TRIMESTRE) VALUES({I},{F},{A},'{Preg}','{Resp}','{T}','{TRIMESTRE}')".format(I,F,A,Preg,Resp,T,TRIMESTRE)
        
        Ejecutar(DATABASE,sql)
        
    
        
    
    # au.registra(30,'EVALUO A: '+getInstructor(I))
    msgito="Respuestas registrada"
    regreso="/login"
    return render_template("alertas.html",msgito=msgito,regreso=regreso)

@app.route('/evalua/<N>/<I>' ,methods=['POST','GET']) 
def evalua(N,I):  
    print("xxxxxxxxxxxxxxxx>",N)
    if N=="1":
       
        F=session['ficha']
        A=session['dnia']
        sql=f"SELECT * FROM THEVAL WHERE idFICHA={F} AND idAPRENDIZ={A}".format(F,A)
        datos=ConsultarUno(DATABASE,sql)
        
        session['instructor']=datos[3]
        I=session['instructor']
        datos=[N,F,I,A]
        return "->"+str(N)
        return render_template('carga.html',N=N,datos=datos)
    if N=="2":
        # F=session['ficha']
        F=3147246
        # A=session['dnia']
        A=1013106019
        # I=session['instructor']
        datos=[N,F,I,A]
        print("__________________________>",N)
        preg=Consultar(DATABASE,'SELECT * FROM PREGUNTA WHERE ESTADO=1')
        hay=len(preg)
        # au.registra(30,'ENTRA A EVALUAR A: '+getInstructor(I))
        apr={
                "ficha":session['ficha'],
                "aprendiz":session['nombreap'],
                "titulacion":session['titulacion'],
                "dnia":session['dnia']
            }
        session['apr']=apr
        
        return render_template('carga.html',N=2,datos=datos,preg=preg,hay=hay,nomi=getInstructor(I),apr=apr)
    if N=="3":
        F=session['ficha']
        A=session['dnia']
        T=session['titulacion']
        TRIMESTRE=obtener_trimestreT(datetime.now())
        
        # I=session['instructor']
        
        conta = int(request.form.get('conta'))

        for i in range(1, conta + 1):  # Asegúrate de incluir el último valor
            Resp=request.form.get('R' + str(i))
            Preg=request.form.get('P' + str(i))
            sql=f"insert into THEVAL(idINSTRUCTOR,idFICHA,idAPRENDIZ,PREGUNTA,RESPUESTA,TITULACION,TRIMESTRE) VALUES({I},{F},{A},'{Preg}','{Resp}','{T}','{TRIMESTRE}')".format(I,F,A,Preg,Resp,T,TRIMESTRE)
            
            Ejecutar(DATABASE,sql)
            
        
            
        
        # au.registra(30,'EVALUO A: '+getInstructor(I))
        msgito="Respuestas registrada"
        regreso="/login"
        return render_template("alertas.html",msgito=msgito,regreso=regreso)
    return "Nada"    
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
@app.route('/verlog')
def verlog():
    fecha=datetime.now()
    fe=str(fecha.year)+str(fecha.month)+str(fecha.day)
    
    # au.registra(30,"Observa el Log de Transacciones:"+str(fecha))
    # return fe
    ruta_origen='static/log/'+fe+'.log'
    ruta_destino='static/archivos/'+fe+'.txt'
    shutil.copy(ruta_origen, ruta_destino)
    # return ver
    return render_template('verlog.html',ver=ruta_destino)

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

@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':  
        dni=request.form['dni'] 
        f = request.files['file'] 
        LUGAR = os.path.join(BASE_DIR, 'static', 'images','dni',dni+'.png')
        # f.save(LUGAR+'/'+f.filename)   
        f.save(LUGAR)   
        msgito="FOTO EDITADA"
        regreso="/login"
        return render_template("alertas.html", msgito=msgito,regreso=regreso)   
@app.route('/menu1', methods = ['GET'])   
def menu1():
    menu = [
    {
        "titulo": "CONFIGURACION",
        "items": [
            {"texto": "DATOS INICIALES", "url": "/construir","svg":"","fa":"fa fa-address-book"},
            {"texto": "APERTURA ENCUESTA", "url": "/construir","svg":"9211","fa":""}
        ]
    },
    {
        "titulo": "CARGUE DE DATOS",
        "items": [
            {"texto": "CARGA MASIVA", "url": "/CargaInicial","svg":"9981","fa":""},
            {"texto": "APRENDICES", "url": "/construir","svg":"","fa":"fa fa-users"},
            {"texto": "INSTRUCTORES", "url": "/construir","svg":"","fa":"fa fa-graduation-cap"},
            {"texto": "PREGUNTAS", "url": "/construir","svg":"","fa":"fa fa-question"},
        ]
    },
    {
    "titulo": "RESULTADOS",
        "items": [
            {"texto": "EXPORTAR RESULTADOS(CSV)", "url": "/resp","svg":"","fa":"fa fa-table"},
        ]
    },
        {
    "titulo": "AUDITORIA",
        "items": [
            {"texto": "DESCARGA LOG TRANSACCIONES", "url": "/descargarlog","svg":"","fa":"fa fa-cloud-download"},
            {"texto": "VER LOG DE TRANSACCIONES", "url": "/verlog","svg":"","fa":"fa fa-television"},
        ]
    },
    {
        "titulo":"TERMINAR",
        "items":[{"texto":"SALIR DEL APLICATIVO","url":"/salir","svg":"","fa":"fa fa-window-close"}]

    }
]

    return render_template("menu1.html",menu=menu)   

@app.route('/CargaInicial', methods = ['GET'])   
def CargaInicial():
    # au.registra(30,'Carga Inicial de la base de datos terminada con exito')
    from Carga import Cargando
    aux= Cargando()
    return render_template("alertas.html",msgito=aux, regreso="/menuadmin")
@app.route('/menuadmin')
def menuadmin():
    # au.registra(30,'ingresa menuadmin')
    return render_template('menuadmin.html')
@app.route('/aprendiz')
def aprendiz():
    return render_template("aprendices.html")
@app.route('/construir')
def construir():
    msgito="401 - PAGINA EN CONSTRUCCION"
    
    return render_template("alertas.html",msgito=msgito,regreso='/menuadmin')
@app.route('/salir')
def salir():
    msgito="SALIENDO DEL APLICATIVO"
    return render_template("alertas.html",msgito=msgito,regreso='/saliendo')
@app.route('/saliendo')
def saliendo():
    return render_template("saliendo.html")

if __name__=='__main__':
    app.run(debug=True,port=5000)