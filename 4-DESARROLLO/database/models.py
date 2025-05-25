from peewee import *
import datetime 
# Conexión a la base de datos SQLite
db = SqliteDatabase('sena.db')  
class BaseModel(Model):
    class Meta:
        database = db

class Asistencia(BaseModel):
    ACTIVIDAD = TextField()
    DNIA = IntegerField()
    DNII = IntegerField()
    FICHA = IntegerField()

class Configura(BaseModel):
    CENTRO = TextField()
    FINICIA = DateField()
    FFIN = DateField()

class Admin(BaseModel):
    id = AutoField()
    NOM = TextField()
    EMAIL = TextField()
    CLA = TextField()
    FECHA = DateTimeField(default=datetime.datetime.now)

class FichaAprendiz(BaseModel):
    id = AutoField()
    FICHA = TextField()
    DNIA = TextField()
    NOMBREAP = TextField()
    ESTADOAP = IntegerField(default=0)
    PWDAP = TextField()
    EMAIL = TextField()
    TITULACION = TextField()
    FECHA = DateTimeField(default=datetime.datetime.now)

class FichaInstructor(BaseModel):
    NOMINST = TextField()
    DNI = TextField()
    FICHA = TextField()
    EMAIL = TextField()
    LIDER = IntegerField(default=0, constraints=[Check('LIDER IN (0, 1)')])
    TRIMESTRE = IntegerField(default=1, constraints=[Check('TRIMESTRE IN (1, 2, 3, 4)')])
    FECHA = DateTimeField(default=datetime.datetime.now)
    PWD = TextField()

class Menu(BaseModel):
    idMenu = AutoField()
    LUGAR = IntegerField()
    NOM = TextField()
    RUTA = TextField()
    ROL = TextField()
    ICONO = TextField()

class Pregunta(BaseModel):
    id = AutoField()
    DESCRIPCION = TextField()
    ESTADO = IntegerField()
    VALORES = TextField()
    FECHA = DateTimeField(default=datetime.datetime.now)

class TheVal(BaseModel):
    idINSTRUCTOR = IntegerField()
    idFICHA = IntegerField()
    TITULACION = TextField()
    idAPRENDIZ = IntegerField()
    PREGUNTA = TextField()
    RESPUESTA = TextField()
    TRIMESTRE = TextField(default='0')
    FECHA = DateTimeField(default=datetime.datetime.now)
    
# Crear las tablas si no existen
db.connect()
db.create_tables([Admin, FichaInstructor, FichaAprendiz, Menu, Pregunta, TheVal])
