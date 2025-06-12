from flask import Blueprint,render_template,session,request,jsonify,url_for,redirect
import requests
from config import apidb
import os
from .menu import menus
from utils.Utilitarios import *
import shutil
admin = Blueprint('admin', __name__, template_folder='templates',static_folder='static',
    static_url_path='/admin/static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@admin.route('/')
def index():
    usua=session['usua']
    au=Auditor(BASE_DIR)
    au.registra(30,'Inicia un administrador',usua) 


    return render_template("menuadmin.html",menu=menus)
@admin.route('/menu1', methods = ['GET'])   
def menu1():
    return render_template("menu1.html",menu=menus)

@admin.route('/verlog')
def verlog():
    fecha=datetime.now()
    fe=str(fecha.year)+str(fecha.month)+str(fecha.day)
    # au.registra(30,"Observa el Log de Transacciones:"+str(fecha))
    # return fe
    # os.makedirs(url_for('static',filename='archivos'),exist_ok=True)
    ruta_origen = os.path.join('/log/', f'{fe}.log')
    # return ruta_origen
# Crear carpeta si no existe
    os.makedirs('admin/static/archivos', exist_ok=True)

# Ruta destino
    ruta_destino = os.path.join('admin/', 'templates/',f'{fe}.html')
    # return ruta_destino
    shutil.copy(ruta_origen, ruta_destino)

# Ruta que el navegador pueda usar (relativa a /static/)
    # ruta_para_html = f'static/archivos/{fe}.html'
    # ruta_para_html=url_for('static',filename=f'/{fe}.html')
    url_log = url_for('static', filename=f'archivos/{fecha}.log', _external=True)

    baseurl=request.host_url
    ruta_para_html=baseurl+f'{fe}.html'
    # return render_template('verlog.html', ver=ruta_para_html)
    # return ruta_para_html
    with open(ruta_destino, 'r', encoding='utf-8') as f:
            contenido = f.read()
    return render_template(f'admin_verl.html',ver=contenido)
@admin.route('/verlog01/<pg>')
def verlog1(pg):
    return "****"
    return redirect(pg)
    return render_template(f'{pg}',ver=pg)


