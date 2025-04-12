from flask import Flask,Blueprint, render_template,session,request ,redirect,url_for
from flask_session import Session
import pandas as pd
from flask_cors import CORS
from utils.Utilitarios import *

app = Flask(__name__) 
app.secret_key = 'BAD_SECRET_KEY'
@app.route('/') 
def raiz():   
    return render_template('index.html')
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
    return render_template('menu.html')
@app.route('/login') 
def login():   
    return render_template('login.html')

@app.route('/acerca') 
def acerca():   
    return render_template('acerca.html')
@app.route('/valida' ,methods=['POST','GET']) 
def valida():   
    N=1
    usua=request.form.get('usua')
    pw=request.form.get('pw')
    hay=EjecutarUno(f"SELECT count(*) FROM FICHAPRENDIZ WHERE DNIA='{usua}' AND EMAIL='{pw}'".format(usua,pw))
    hay=hay[0]
    if hay=="0":
        return render_template("alertas.html",msgito="USUARIO O CLAVE INCORRECTO",regreso="/login")
    sql=f"SELECT * FROM FICHAPRENDIZ WHERE EMAIL='{usua}' AND PWDAP='{pw}'".format(usua,pw)
    aprendiz=EjecutarUno(sql)
    session['ficha'] = aprendiz[0]
    session['dnia'] = aprendiz[1]
    session['nombreap'] = aprendiz[2]
    session['titulacion'] = aprendiz[6]
    
    F=session['ficha']
    A=session['dnia']
    N=1
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
    datos=Ejecutar(sql)

    return render_template('carga.html',N=N,datos=datos)

@app.route('/otro' ,methods=['POST','GET']) 
def otro():
    hay=EjecutarUno(f"SELECT count(*) FROM FICHAPRENDIZ WHERE DNIA='{usua}' AND EMAIL='{pw}'".format(usua,pw))
    hay=hay[0]
    if hay=="0":
        session[usua]=usua

        return render_template("alertas.html",msgito="USUARIO O CLAVE INCORRECTO",regreso="/login")
    sql=f"SELECT * FROM FICHAPRENDIZ WHERE EMAIL='{usua}' AND PWDAP='{pw}'".format(usua,pw)
    aprendiz=EjecutarUno(sql)
    session['ficha'] = aprendiz[0]
    session['dnia'] = aprendiz[1]
    session['nombreap'] = aprendiz[2]
    session['titulacion'] = aprendiz[6]
    F=session['ficha']
    A=session['dnia']
    N=1
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{F}' AND IDAPRENDIZ='{A}')".format(F,A)
    datos=Ejecutar(sql)
    session['instructor'] = datos[1]
    session['ninstructor'] = datos[0]

    return render_template('carga.html',N=N,datos=datos)

@app.route('/evalua/<N>/<I>' ,methods=['POST','GET']) 
def evalua(N,I):   
    if N=="1":
        F=session['ficha']
        A=session['dnia']
        sql=f"SELECT * FROM THEVAL WHERE idFICHA={F} AND idAPRENDIZ={A}".format(F,A)
        datos=EjecutarUno(sql)
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
        preg=Ejecutar('SELECT * FROM PREGUNTA WHERE ESTADO=1')
        hay=len(preg)
        return render_template('carga.html',N=N,datos=datos,preg=preg,hay=hay)
    if N=="3":
        F=session['ficha']
        A=session['dnia']
        T=session['titulacion']
        I=session['titulacion']
        
        # I=session['instructor']
        print(F,I,A)
        conta = int(request.form.get('conta'))
        for i in range(1, conta + 1):  # Asegúrate de incluir el último valor
            Resp=request.form.get('R' + str(i))
            Preg=request.form.get('P' + str(i))
            sql=f"insert into THEVAL(idINSTRUCTOR,idFICHA,idAPRENDIZ,PREGUNTA,RESPUESTA,TITULACION) VALUES({I},{F},{A},'{Preg}','{Resp}','{T}')".format(I,F,A,Preg,Resp,T)
            # Insertar(sql)
            print(sql)
        
        msgito="Respuestas registrada"
        regreso="/login"
        return render_template("alertas.html",msgito=msgito,regreso=regreso)
    return "Nada"    

if __name__=='__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')