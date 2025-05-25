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
    LIDER = IntegerField(default=0, constraints=[Check('LIDER IN (0, 1)')])
    TRIMESTRE = IntegerField(default=1, constraints=[Check('TRIMESTRE IN (1, 2, 3, 4)')])
    FECHA = DateTimeField(default=datetime.datetime.now)
    PWD = TextField(null=True)

class Menu(BaseModel):
    idMenu = AutoField()
    LUGAR = IntegerField()
    NOM = TextField()
    RUTA = TextField()
    ROL = TextField()
    ICONO = TextField()

class Pregunta(BaseModel):
    id = AutoField()
    DESCRIPCION = TextField(null=True)
    ESTADO = IntegerField(null=True)
    VALORES = TextField(null=True)
    FECHA = DateTimeField(default=datetime.datetime.now)

class TheVal(BaseModel):
    idINSTRUCTOR = IntegerField(null=True)
    idFICHA = IntegerField(null=True)
    TITULACION = TextField(null=True)
    idAPRENDIZ = IntegerField(null=True)
    PREGUNTA = TextField(null=True)
    RESPUESTA = TextField(null=True)
    TRIMESTRE = TextField(default='0',null=True)
    FECHA = DateTimeField(default=datetime.datetime.now)
    
# Crear las tablas si no existen

db.connect()
db.create_tables([Admin, FichaInstructor, FichaAprendiz, Menu, Pregunta, TheVal])
print("PROCESO FINALIZADO")