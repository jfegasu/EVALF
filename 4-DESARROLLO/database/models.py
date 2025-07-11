from peewee import *
from peewee import SqliteDatabase
import datetime 
import os
from flask import Blueprint, current_app, g
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR,  'sena.db')
# DATABASE=current_app.config['DATABASE']

# Conexión a la base de datos SQLite
db = SqliteDatabase(DATABASE)  
class BaseModel(Model):
    class Meta:
        database = db

class Asistencia(BaseModel):
    ACTIVIDAD = TextField(null=True)
    DNIA = IntegerField(null=True)
    DNII = IntegerField(null=True)
    FICHA = IntegerField(null=True)

class Configura(BaseModel):
    CENTRO = TextField(null=True)
    FINICIA = DateField(null=True)
    FFIN = DateField(null=True)

class Admin(BaseModel):
    id = AutoField()
    NOM = TextField()
    EMAIL = TextField()
    CLA = TextField()
    FECHA = DateTimeField(default=datetime.datetime.now)



class FichaAprendiz(BaseModel):
    FICHA = TextField(null=True)
    DNIA = TextField(null=True)
    NOMBREAP = TextField(null=True)
    ESTADOAP = IntegerField(default=0)
    PWDAP = TextField(null=True)
    EMAIL = TextField(null=True)
    TITULACION = TextField(null=True)
    FECHA = DateTimeField(default=datetime.datetime.now,null=True)

class FichaInstructor(BaseModel):
    NOMINST = TextField(null=True)
    DNI = TextField(null=True)
    FICHA = TextField(null=True)
    EMAIL = TextField(null=True)
    LIDER = IntegerField(default=0, constraints=[Check('LIDER IN (0, 1)')],null=True)
    TRIMESTRE = IntegerField(default=1, constraints=[Check('TRIMESTRE IN (1, 2, 3, 4)')],null=True)
    FECHA = DateTimeField(default=datetime.datetime.now,null=True)
    PWD = TextField(null=True)

class Menu(BaseModel):
    idMenu = AutoField()
    LUGAR = IntegerField(null=True)
    NOM = TextField(null=True)
    RUTA = TextField(null=True)
    ROL = TextField(null=True)
    ICONO = TextField(null=True)

class Pregunta(BaseModel):
    id = AutoField()
    DESCRIPCION = TextField(null=True)
    ESTADO = IntegerField(null=True)
    VALORES = TextField(null=True)
    FECHA = DateTimeField(default=datetime.datetime.now,null=True)

class Asistencia(Model):
    actividad = CharField(null=True)
    dnia = CharField(null=True)
    dnii = CharField(null=True)
    ficha = CharField(null=True)
    falla = CharField(max_length=1, null=True)
    
class TheVal(BaseModel):
    idINSTRUCTOR = IntegerField(null=True)
    idFICHA = IntegerField(null=True)
    TITULACION = TextField(null=True)
    idAPRENDIZ = IntegerField(null=True)
    PREGUNTA = TextField(null=True)
    RESPUESTA = TextField(null=True)
    TRIMESTRE = TextField(default='0',null=True)
    FECHA = DateTimeField(default=datetime.datetime.now,null=True)


class VInstructorEsp(BaseModel):
    titulacion = CharField()
    ficha = IntegerField()
    dninst = CharField()
    emailinst = CharField()
    nominst = CharField()
    dniap = CharField()
    nombreap = CharField()
    emailap = CharField()

    class Meta:
        table_name = 'vinstructoresp'
        primary_key = False  # Las vistas normalmente no tienen clave primaria
    
db.connect()
# Crear las tablas si no existen


if __name__ == '__main__':
    
    db.create_tables([Admin, FichaInstructor, FichaAprendiz, Menu, Pregunta, TheVal])
    print("PROCESO FINALIZADO")