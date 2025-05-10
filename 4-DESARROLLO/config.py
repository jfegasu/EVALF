# config.py
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'tu_clave_secreta_segura'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    apidb="http://127.0.0.1:5555"

class DevelopmentConfig(Config):
    DEBUG = True
    apidb="http://127.0.0.1:5555"

    

class ProductionConfig(Config):
    SECRET_KEY = 'clave_muy_segura_en_producción'
    # SQLALCHEMY_DATABASE_URI = 'mysql://usuario:password@servidor/db'

class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
