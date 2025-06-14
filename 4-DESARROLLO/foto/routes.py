from flask import Blueprint,render_template,session,request,jsonify,url_for
import requests
from config import apidb
import os
from utils.Utilitarios import *
foto = Blueprint('foto', __name__, template_folder='templates',static_folder='static',
    static_url_path='/foto/static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@foto.route('/')
def index():
    usua=session['usua']
    usua=session['usua']
    au=Auditor(BASE_DIR)
    au.registra(30,'Inicia un instructor',usua) 
    sql=f"{apidb}/i/e/{usua}".format(usua)    
    datos=requests.get(sql).json()

    return render_template('foto.html',datos=datos[0])

@foto.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':  
        dni=request.form['dni'] 
        
        # return session['usua']
        f = request.files['file'] 
        BASE_DIR=os.path.join(os.path.dirname(__file__))
        LUGAR = os.path.join(BASE_DIR, 'static', 'images','dni',session['usua']+'.png')
        
        # f.save(LUGAR+'/'+f.filename)   
        f.save(LUGAR)   
        msgito="FOTO EDITADA"
        regreso="/foto"
        return render_template("alertas.html", msgito=msgito,regreso=regreso)   
