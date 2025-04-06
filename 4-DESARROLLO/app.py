from flask import Flask,Blueprint, render_template,session,request ,redirect,url_for
from flask_session import Session
import pandas as pd
from flask_cors import CORS

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

if __name__=='__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')