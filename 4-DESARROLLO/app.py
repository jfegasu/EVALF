from flask import Flask,Blueprint, jsonify, render_template,session,request ,redirect,url_for,send_from_directory
from flask_session import Session
import pandas as pd
from flask_cors import CORS
import requests
from utils.Utilitarios import *
import socket
import hashlib
import logging
from config import DevelopmentConfig 

app = Flask(__name__) 
app.secret_key = 'BAD_SECRET_KEY'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'EVALF.db')
RESPUESTAS = os.path.join(BASE_DIR, 'static/archivos/RESPUESTAS.csv')
app.config['apidb'] =  "http://127.0.0.1:5555"
# app.config.from_object(DevelopmentConfig) 
au=Auditor()

@app.route('/') 
def raiz():   
    return render_template('inicio.html')
@app.route('/0') 
def indexppal():   
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
            return render_template('carga.html',N=N,datos=datos,apr=apr)
  
        else:
            msgito="APRENDIZ O CLAVE ERRADOS**"
            regresa="/login"
            au.registra(30,msgito)
            # *******
            return render_template('alertas.html',msgito=msgito,regreso=regresa)
    elif Tipo['Tipo']==2:
        return 'Instructor'
    elif Tipo['Tipo']==3:
        return 'Administrador'
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
        return render_template('carga.html',N=N,datos=datos,preg=preg,hay=hay,nomi=getInstructor(I),apr=apr)
    if N=="3":
        F=session['ficha']
        A=session['dnia']
        T=session['titulacion']

        
        # I=session['instructor']
        print(F,I,A)
        conta = int(request.form.get('conta'))

        for i in range(1, conta + 1):  # Asegúrate de incluir el último valor
            Resp=request.form.get('R' + str(i))
            Preg=request.form.get('P' + str(i))
            sql=f"insert into THEVAL(idINSTRUCTOR,idFICHA,idAPRENDIZ,PREGUNTA,RESPUESTA,TITULACION) VALUES({I},{F},{A},'{Preg}','{Resp}','{T}')".format(I,F,A,Preg,Resp,T)
            Ejecutar(DATABASE,sql)
            
        
            # print(sql)
        
        au.registra(30,'EVALUO A: '+getInstructor(I))
        msgito="Respuestas registrada"
        regreso="/login"
        return render_template("alertas.html",msgito=msgito,regreso=regreso)
    return "Nada"    
@app.route('/descargar')
def descargar():
    return send_from_directory('static/archivos', 'RESPUESTAS.csv', as_attachment=True)
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
    return render_template('respuestas.html')
# juanav_duque@soy.sena.edu.co  6019
# jgalindos@sena.edu.co
# admin@sena.edu.co
if __name__=='__main__':
    app.run(debug=True,port=5000)