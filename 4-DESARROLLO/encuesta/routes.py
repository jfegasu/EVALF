from flask import Blueprint,render_template,session,request,jsonify
import requests
from config import apidb
import os
eval = Blueprint('eval', __name__, template_folder='templates',static_folder='static',
    static_url_path='/eval/static')

@eval.route('/')
def index():
    return "Evaluacion"