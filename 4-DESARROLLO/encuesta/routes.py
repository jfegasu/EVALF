from flask import Blueprint,render_template,session,request,jsonify
import requests
from config import apidb
import os
eval = Blueprint('eval', __name__, template_folder='templates',static_folder='static',
    static_url_path='/eval/static')

@eval.route('/')
def index(): 
    usua=session['usua']   
    datos=requests.get(f'{apidb}/u/datos/{usua}').json()
    ficha=requests.get(f'{apidb}/a/1/{usua}').text
    session['datos']=datos
    aa=f'{apidb}/i/2/{ficha}/{usua}'
    datos=requests.get(aa).json()
    return render_template('eval_carga.html',N=1,datos=datos,apr=session['datos'])