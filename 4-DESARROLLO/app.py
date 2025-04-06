from flask import Flask,Blueprint, render_template,session,request ,redirect,url_for
from flask_session import Session
import pandas as pd
from flask_cors import CORS

app = Flask(__name__) 
@app.route('/') 
def raiz():   
    return "HOLA"

if __name__=='__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')