# config.py
import os
apidb="http://127.0.0.1:5556"

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'tu_clave_secreta_segura'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    apidb="http://127.0.0.1:5556"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DevelopmentConfig(Config):
    DEBUG = True
    apidb="http://127.0.0.1:5556"

# menu = [
#     {
#         "titulo": "CONFIGURACION",
#         "items": [
#             {"texto": "DATOS INICIALES", "url": "/construir","svg":"","fa":"fa fa-address-book"},
#             {"texto": "APERTURA ENCUESTA", "url": "/construir","svg":"9211","fa":""}
#         ]
#     },
#     {
#         "titulo": "CARGUE DE DATOS",
#         "items": [
#             {"texto": "CARGA MASIVA", "url": "/CargaInicial","svg":"9981","fa":""},
#             {"texto": "APRENDICES", "url": "/construir","svg":"","fa":"fa fa-users"},
#             {"texto": "INSTRUCTORES", "url": "/construir","svg":"","fa":"fa fa-graduation-cap"},
#             {"texto": "PREGUNTAS", "url": "/construir","svg":"","fa":"fa fa-question"},
#         ]
#     },
#     {
#     "titulo": "RESULTADOS",
#         "items": [
#             {"texto": "EXPORTAR RESULTADOS(CSV)", "url": "/resp","svg":"","fa":"fa fa-table"},
#         ]
#     },
#         {
#     "titulo": "AUDITORIA",
#         "items": [
#             {"texto": "DESCARGA LOG TRANSACCIONES", "url": "/descargarlog","svg":"","fa":"fa fa-cloud-download"},
#             {"texto": "VER LOG DE TRANSACCIONES", "url": "/verlog","svg":"","fa":"fa fa-television"},
#         ]
#     },
# ]
   

class ProductionConfig(Config):
    SECRET_KEY = 'clave_muy_segura_en_producción'
    # SQLALCHEMY_DATABASE_URI = 'mysql://usuario:password@servidor/db'

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
