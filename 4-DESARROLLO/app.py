from flask import Flask,Blueprint, render_template,session,request ,redirect,url_for
from flask_session import Session
import pandas as pd
from flask_cors import CORS
from utils.Utilitarios import *

app = Flask(__name__) 
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
@app.route('/valida' ,methods=['POST','GET']) 
def valida():   
    N=1
    hay=EjecutarUno('SELECT count(*) FROM VMOSTRAR WHERE FICHA=312746 AND DNI_APRENDIZ=1234')
    hay=hay[0]

    datos=Ejecutar('SELECT * FROM VINSTRUCTOR WHERE idINSTRUCTOR NOT IN(SELECT IDINSTRUCTOR FROM VMOSTRAR WHERE FICHA=312746 AND DNI_APRENDIZ=1234)')
   
    print(hay)
    return render_template('carga.html',N=N,datos=datos)
@app.route('/evalua/<N>/<F>/<I>/<A>' ,methods=['POST','GET']) 
def evalua(N,F,I,A):   
    if N==1:
        datos=EjecutarUno('SELECT count(*) FROM VMOSTRAR WHERE FICHA=312746 AND DNI_APRENDIZ=1234')
        datos=[N,F,I,A]
        return render_template('carga.html',N=N,datos=datos)
    if N=="2":
        datos=[N,F,I,A]
        preg=Ejecutar('SELECT * FROM PREGUNTA WHERE ESTADO=1')
        return render_template('carga.html',N=N,datos=datos,preg=preg)
    if N=="3":
        msgito="Respuestas registrada"
        regreso="/login"
        return render_template("alertas.html",msgito=msgito,regreso=regreso)
    return "Nada"    

if __name__=='__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')