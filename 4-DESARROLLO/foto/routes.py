from flask import Blueprint,render_template,session
import requests
from config import apidb
foto = Blueprint('foto', __name__, template_folder='templates')


@foto.route('/')
def index():
    usua=session['usua']
    sql=f"/i/e/{usua}".format(usua)    
    datos=requests.get(sql)
    
    return render_template('foto_index.html',datos=datos)