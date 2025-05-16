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
app.config['apidb'] =  "http://127.0.0.1:5555"
# app.config.from_object(DevelopmentConfig) 
au=Auditor(BASE_DIR)

@app.route('/') 
def raiz():   
    return render_template('inicio.html')
@app.route('/0') 
def indexppal():  
    au.registra(30,'Inicia Aplicacion') 
    return render_template('indexppal.html')
@app.route('/banner') 
def banner():   
    return render_template('banner.html')
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
    return ConsultarDB('/inst/contar/'+correo)

@app.route('/valida' ,methods=['POST','GET']) 
def valida():   
    N=1
    usua=request.form.get('usua')
    pw=request.form.get('pw')
    Tipo=tipoUsuario(usua)
    print(Tipo)
    pw1=hashlib.md5(pw.encode()).hexdigest()
    if Tipo['Tipo']==1:
        sql=f"SELECT count(*) FROM FICHAPRENDIZ WHERE PWDAP='{pw1}' AND EMAIL='{usua}'".format(usua,pw1)
        # hay=ConsultarUno(DATABASE,sql)
        hay=ConsultarDB(f"/aprend/v/1/{usua}/{pw1}".format(usua,pw1))
        if hay==1:
            N=1
            sql=f"SELECT * FROM FICHAPRENDIZ WHERE PWDAP='{pw1}' AND EMAIL='{usua}'".format(usua,pw1)
            aprendiz=ConsultarDB(f"/aprend/vd/1/{usua}/{pw1}".format(usua,pw1))
            print(jsonify(aprendiz))
            session['ficha']=aprendiz['FICHA']
            session['nombreap']= aprendiz['NOMBREAP']  
            session['titulacion']= aprendiz['TITULACION']   
            session['dnia']= aprendiz['DNIA']  
            # return str(aprendiz)
            F=aprendiz['FICHA']
            A=aprendiz['DNIA'] 
            sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
            # datos=Consultar(DATABASE,sql)
            datos=ConsultarDB(f"/inst/{F}/{A}".format(F,A))
            print(datos)
            apr={
                "ficha":session['ficha'],
                "aprendiz":session['nombreap'],
                "titulacion":session['titulacion'],
                "dnia":session['dnia']
            }
            print("-->",N)
            au.registra(30,'Ingresa:'+session['nombreap'])
            return render_template('carga.html',N=N,datos=datos,apr=apr)
  
        else:
            msgito="APRENDIZ O CLAVE ERRADOS**"
            regresa="/login"
            au.registra(30,msgito)
            # *******
            return render_template('alertas.html',msgito=msgito,regreso=regresa)
    elif Tipo['Tipo']==2:
        sql=f"/inst/e/{usua}".format(usua)
        print(sql)
        datos=ConsultarDB(sql)

        return render_template('foto.html',datos=datos)
        
        
    elif Tipo['Tipo']==3:
        return render_template('menuadmin.html')
    if Tipo['Tipo']==0:
        msgito="USUARIO NO EXISTE**"
        regresa="/login"
        au.registra(30,msgito)
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
        au.registra(30,'USUARIO O CLAVE ERRADOS')
        return render_template('login.html',msgito=msgito,regreso=regresa)
    
    hay=hay[0]
    # return "->"+str(hay)
    if hay=="0":
        au.registra(30,'USUARIO O CLAVE ERRADOS')
        return render_template("alertas.html",msgito="USUARIO O CLAVE INCORRECTO***",regreso="/login")
    
    
    
    
    try:
        sql=f"SELECT * FROM FICHAPRENDIZ WHERE EMAIL='{usua}' AND PWDAP='{pw1}'".format(usua,pw)
        aprendiz=ConsultarUno(DATABASE,sql)
        session['ficha'] = aprendiz[0]
        session['dnia'] = aprendiz[1]
        session['nombreap'] = aprendiz[2]
        session['titulacion'] = aprendiz[6]
        
    except:
        au.registra(30,'USUARIO O CLAVE ERRADOS')
        msgito="USUARIO O CLAVE ERRADOS**"
        regresa="/login"
        return render_template('alertas.html',msgito=msgito,regreso=regresa)
    
    F=session['ficha']
    A=session['dnia']
    N=1
    sql=f"SELECT count(*) FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
    au.registra(30,'INGRESO ',session['nombreap'])

    hay=ConsultarUno(DATABASE,sql)

    if hay[0]=="0":
        msgito="NO HAY INSTRUCTORES PARA EVALUAR"
        au.registra(30,msgito,session['nombreap'])

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
        au.registra(30,str(apr),session['nombreap'])
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
@app.route('/otro' ,methods=['POST','GET']) 
def otro():
    hay=ConsultarUno(DATABASE,f"SELECT count(*) FROM FICHAPRENDIZ WHERE DNIA='{usua}' AND EMAIL='{pw}'".format(usua,pw))
    hay=hay[0]
    if hay=="0":
        session[usua]=usua

        return render_template("alertas.html",msgito="USUARIO O CLAVE INCORRECTO",regreso="/login")
    sql=f"SELECT * FROM FICHAPRENDIZ WHERE EMAIL='{usua}' AND PWDAP='{pw}'".format(usua,pw)
    aprendiz=ConsultarUno(DATABASE,sql)
    session['ficha'] = aprendiz[0]
    session['dnia'] = aprendiz[1]
    session['nombreap'] = aprendiz[2]
    session['titulacion'] = aprendiz[6]
    F=session['ficha']
    A=session['dnia']
    N=1
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
    datos=Consultar(DATABASE,sql)
    session['instructor'] = datos[1]
    session['ninstructor'] = datos[0]

    return render_template('carga.html',N=N,datos=datos)

@app.route('/evalua/<N>/<I>' ,methods=['POST','GET']) 
def evalua(N,I):   
    print("N--->",N)
    if N=="1":
       
        F=session['ficha']
        A=session['dnia']
        sql=f"SELECT * FROM THEVAL WHERE idFICHA={F} AND idAPRENDIZ={A}".format(F,A)
        datos=ConsultarUno(DATABASE,sql)
        print("nnnnn>",datos)
        session['instructor']=datos[3]
        I=session['instructor']
        datos=[N,F,I,A]
        return render_template('carga.html',N=N,datos=datos)
    if N=="2":
        F=session['ficha']
        A=session['dnia']
        # I=session['instructor']
        datos=[N,F,I,A]
        print("------------->",F,I,A)
        preg=Consultar(DATABASE,'SELECT * FROM PREGUNTA WHERE ESTADO=1')
        hay=len(preg)
        au.registra(30,'ENTRA A EVALUAR A: '+getInstructor(I))
        apr={
                "ficha":session['ficha'],
                "aprendiz":session['nombreap'],
                "titulacion":session['titulacion'],
                "dnia":session['dnia']
            }
        session['apr']=apr
        print("Preguntas->>>",preg)
        return render_template('carga.html',N=N,datos=datos,preg=preg,hay=hay,nomi=getInstructor(I),apr=apr)
    if N=="3":
        F=session['ficha']
        A=session['dnia']
        T=session['titulacion']
        TRIMESTRE=obtener_trimestreT(datetime.now())
        
        # I=session['instructor']
        print(F,I,A)
        conta = int(request.form.get('conta'))

        for i in range(1, conta + 1):  # Asegúrate de incluir el último valor
            Resp=request.form.get('R' + str(i))
            Preg=request.form.get('P' + str(i))
            sql=f"insert into THEVAL(idINSTRUCTOR,idFICHA,idAPRENDIZ,PREGUNTA,RESPUESTA,TITULACION,TRIMESTRE) VALUES({I},{F},{A},'{Preg}','{Resp}','{T}','{TRIMESTRE}')".format(I,F,A,Preg,Resp,T,TRIMESTRE)
            print("CCCCC>>",sql)
            Ejecutar(DATABASE,sql)
            
        
            # print(sql)
        
        au.registra(30,'EVALUO A: '+getInstructor(I))
        msgito="Respuestas registrada"
        regreso="/login"
        return render_template("alertas.html",msgito=msgito,regreso=regreso)
    return "Nada"    
@app.route('/descargar')
def descargar():
    au.registra(30,"Descarga Respuestas")
    return send_from_directory('static/archivos', 'RESPUESTAS.csv', as_attachment=True)
@app.route('/descargarlog')
def descargarlog():
    fecha=datetime.now()
    fe=str(fecha.year)+str(fecha.month)+str(fecha.day)
    print(fe)
    au.registra(30,"Descarga Log de Transacciones")
    # return fe
    return send_from_directory('/log/', fe+'.log',as_attachment=True)
@app.route('/verlog')
def verlog():
    fecha=datetime.now()
    fe=str(fecha.year)+str(fecha.month)+str(fecha.day)
    print(fe)
    au.registra(30,"Observa el Log de Transacciones:"+str(fecha))
    # return fe
    ruta_origen='/log/'+fe+'.log'
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
    return render_template("menu1.html")   

@app.route('/CargaInicial', methods = ['GET'])   
def CargaInicial():
    au.registra(30,'Carga Inicial de la base de datos terminada con exito')
    from Carga import Cargando
    aux= Cargando()
    return render_template("alertas.html",msgito=aux, regreso="/menuadmin")
@app.route('/menuadmin')
def menuadmin():
    return render_template('menuadmin.html')
# juanav_duque@soy.sena.edu.co  6019
# jgalindos@sena.edu.co
# admin@sena.edu.co
if __name__=='__main__':
    app.run(debug=True,port=5000)