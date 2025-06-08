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

    menus = [
    {
        "titulo": "CONFIGURACION",
        "items": [
            {"texto": "DATOS INICIALES", "url": "/construir","svg":"","fa":"fa fa-address-book"},
            {"texto": "APERTURA ENCUESTA", "url": "/construir","svg":"9211","fa":""}
        ]
    },
    {
        "titulo": "CARGUE DE DATOS",
        "items": [
            {"texto": "CARGA MASIVA", "url": "/CargaInicial","svg":"9981","fa":""},
            {"texto": "APRENDICES", "url": "/construir","svg":"","fa":"fa fa-users"},
            {"texto": "INSTRUCTORES", "url": "/construir","svg":"","fa":"fa fa-graduation-cap"},
            {"texto": "PREGUNTAS", "url": "/construir","svg":"","fa":"fa fa-question"},
        ]
    },
    {
    "titulo": "RESULTADOS",
        "items": [
            {"texto": "EXPORTAR RESULTADOS(CSV)", "url": "/resp","svg":"","fa":"fa fa-table"},
        ]
    },
        {
    "titulo": "AUDITORIA",
        "items": [
            {"texto": "DESCARGA LOG TRANSACCIONES", "url": "/descargarlog","svg":"","fa":"fa fa-cloud-download"},
            {"texto": "VER LOG DE TRANSACCIONES", "url": "/verlog","svg":"","fa":"fa fa-television"},
        ]
    },
    {
        "titulo":"TERMINAR APLICACION",
        "items":[{"texto":"SALIR DEL APLICATIVO","url":"/saliendo","svg":"","fa":"fa fa-window-close"}]

    }
]
    return render_template("menuadmin.html",menu=menus)
@admin.route('/menu1', methods = ['GET'])   
def menu1():
    menus = [
    {
        "titulo": "CONFIGURACION",
        "items": [
            {"texto": "DATOS INICIALES", "url": "/construir","svg":"","fa":"fa fa-address-book"},
            {"texto": "APERTURA ENCUESTA", "url": "/construir","svg":"9211","fa":""}
        ]
    },
    {
        "titulo": "CARGUE DE DATOS",
        "items": [
            {"texto": "CARGA MASIVA", "url": "/CargaInicial","svg":"9981","fa":""},
            {"texto": "APRENDICES", "url": "/construir","svg":"","fa":"fa fa-users"},
            {"texto": "INSTRUCTORES", "url": "/construir","svg":"","fa":"fa fa-graduation-cap"},
            {"texto": "PREGUNTAS", "url": "/construir","svg":"","fa":"fa fa-question"},
        ]
    },
    {
    "titulo": "RESULTADOS",
        "items": [
            {"texto": "EXPORTAR RESULTADOS(CSV)", "url": "/resp","svg":"","fa":"fa fa-table"},
        ]
    },
        {
    "titulo": "AUDITORIA",
        "items": [
            {"texto": "DESCARGA LOG TRANSACCIONES", "url": "/descargarlog","svg":"","fa":"fa fa-cloud-download"},
            {"texto": "VER LOG DE TRANSACCIONES", "url": "/verlog","svg":"","fa":"fa fa-television"},
        ]
    },
    {
        "titulo":"TERMINAR APLICACION",
        "items":[{"texto":"SALIR DEL APLICATIVO","url":"/saliendo","svg":"","fa":"fa fa-window-close"}]

    }
]
    return render_template("menu1.html",menu=menus)

