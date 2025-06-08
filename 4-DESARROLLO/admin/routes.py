from flask import Blueprint,render_template,session,request,jsonify
import requests
from config import apidb
import os
admin = Blueprint('admin', __name__, template_folder='templates',static_folder='static',
    static_url_path='/admin/static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@admin.route('/')
def index():
    usua=session['usua']
    return render_template("menuadmin.html")
