from peewee import *

# Conexión a la base de datos SQLite
db = SqliteDatabase('sena.db')  


class BaseModel(Model):
    class Meta:
        database = db


class Admin(BaseModel):
    NOM = TextField()
    EMAIL = TextField()
    CLA = TextField()


class FichaInstructor(BaseModel):
    NOMINST = TextField(null=True)
    DNI = TextField()
    FICHA = TextField(null=True)
    EMAIL = TextField(null=True)
    


class FichaAprendiz(BaseModel):
    FICHA = TextField(null=True)
    DNIA = TextField(null=True)
    NOMBREAP = TextField(null=True)
    ESTADOAP = TextField(null=True)
    PWDAP = TextField()
    EMAIL = TextField(null=True)
    TITULACION = TextField()


class Menu(BaseModel):
    idMenu = AutoField()
    LUGAR = IntegerField()
    NOM = TextField()
    RUTA = TextField()
    ROL = TextField()
    ICONO = TextField(null=True)


class Pregunta(BaseModel):
    DESCRIPCION = TextField()
    ESTADO = IntegerField(default=0)
    VALORES = TextField()


class TheVal(BaseModel):
    idTHEVAL = IntegerField(primary_key=True)
    idINSTRUCTOR = IntegerField()
    idFICHA = IntegerField()
    TITULACION = TextField()
    idAPRENDIZ = IntegerField()
    PREGUNTA = IntegerField(null=True)
    RESPUESTA = TextField(null=True)


# Crear las tablas si no existen
db.connect()
db.create_tables([Admin, FichaInstructor, FichaAprendiz, Menu, Pregunta, TheVal])
