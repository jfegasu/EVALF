from flask import Flask, request, jsonify
from peewee import *
from models import *
from playhouse.shortcuts import model_to_dict
from peewee import fn
import os
import sqlite3
import json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR,  'sena.db')

# Configuración de base de datos
db = SqliteDatabase(DATABASE)
def Consultar(db,sql):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row  # Esto permite acceder a los resultados como diccionarios
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    # Convertir cada fila a un diccionario
    output = [dict(row) for row in rows]

    return output  # Devolver como JSON string
def ConsultarUno(db,sql):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    output = cursor.fetchone() 
    conn.close()
    return output 

class BaseModel(Model):
    class Meta:
        database = db



# Inicialización de Flask
app = Flask(__name__)

# CREATE - Crear un nuevo admin
@app.route('/admin', methods=['POST'])
def crear_admin():
    data = request.json
    admin = Admin.create(
        NOM=data['NOM'],
        EMAIL=data['EMAIL'],
        CLA=data['CLA']
    )
    return jsonify({'message': 'Admin creado', 'id': admin.id})

# READ - Obtener todos los admins
@app.route('/admin', methods=['GET'])
def obtener_admins():
    admins = Admin.select()
    return jsonify([{'id': a.id, 'NOM': a.NOM, 'EMAIL': a.EMAIL} for a in admins])

# READ - Obtener admin por ID
@app.route('/admin/<int:admin_id>', methods=['GET'])
def obtener_admin(admin_id):
    admin = Admin.get_or_none(Admin.id == admin_id)
    if admin:
        return jsonify({'id': admin.id, 'NOM': admin.NOM, 'EMAIL': admin.EMAIL})
    return jsonify({'error': 'Admin no encontrado'}), 404

# UPDATE - Actualizar admin
@app.route('/admin/<int:admin_id>', methods=['PUT'])
def actualizar_admin(admin_id):
    data = request.json
    admin = Admin.get_or_none(Admin.id == admin_id)
    if not admin:
        return jsonify({'error': 'Admin no encontrado'}), 404
    admin.NOM = data.get('NOM', admin.NOM)
    admin.EMAIL = data.get('EMAIL', admin.EMAIL)
    admin.CLA = data.get('CLA', admin.CLA)
    admin.save()
    return jsonify({'message': 'Admin actualizado'})

# DELETE - Eliminar admin
@app.route('/admin/<int:admin_id>', methods=['DELETE'])
def eliminar_admin(admin_id):
    admin = Admin.get_or_none(Admin.id == admin_id)
    if not admin:
        return jsonify({'error': 'Admin no encontrado'}), 404
    admin.delete_instance()
    return jsonify({'message': 'Admin eliminado'})
@app.route('/inst', methods=['GET'])
def obtener_Inst():
     instructores = FichaInstructor.select()
     data = [model_to_dict(inst) for inst in instructores]
     return jsonify(data)
@app.route('/inst/d/<dni>', methods=['GET'])
def obtener_instructor_por_dni(dni):
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE DNI='{dni}'".format(dni)
    datos=Consultar(DATABASE,sql)
    return jsonify(datos),404
@app.route('/u/<int:t>/<p>/<m>')
def Valida(t,p,m):
    if t==1:
        sql=f"SELECT COUNT(*) cant FROM FICHAAPRENDIZ WHERE PWDAP='{p}' AND EMAIL='{m}'".format(p,m)
        try:
            datos=ConsultarUno(DATABASE,sql)
            return jsonify(datos[0])
        except Exception as e:
            return 401
    if t==2:
        sql=f"SELECT COUNT(*) cant FROM FICHAINSTRUCTOR WHERE PWDAP='{p}' AND EMAIL='{m}'".format(p,m)
        try:
            datos=ConsultarUno(DATABASE,sql)
            return jsonify(datos[0])
        except Exception as e:
            return 401
    
@app.route('/inst/e/<email>', methods=['GET'])
def obtener_instructor_por_email(email):
    sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    return jsonify(datos),404
    
@app.route('/inst/ficha/<ficha>', methods=['GET'])
def obtener_instructores_por_ficha(ficha):
    instructores = FichaInstructor.select().where(FichaInstructor.FICHA == ficha)
    data = [model_to_dict(inst) for inst in instructores]
    return jsonify(data)
@app.route('/aprend', methods=['GET'])
def obtener_aprend():
     aprend = FichaAprendiz.select()
     data = [model_to_dict(inst) for inst in aprend]
     return jsonify(data),404
@app.route('/aprend/<dni>', methods=['GET'])
def obtener_aprendiz_por_dni(dni):
    aprend = FichaAprendiz.get_or_none(FichaAprendiz.DNIA == dni)
    if aprend:
        return jsonify(model_to_dict(aprend))
    return jsonify({'error': 'Instructor no encontrado'}), 404
@app.route('/aprend/v/<tipo>/<email>/<pwd>', methods=['GET'])
def valida_aprendiz_por_email(tipo,email,pwd):
    aprend="0"
    if tipo=="1":
        aprend = FichaAprendiz.get_or_none(FichaAprendiz.EMAIL == email )
        
        aa=jsonify(model_to_dict(aprend))
        
        if aprend.PWDAP==pwd:
            return "1"
        else:
            return "0"
@app.route('/aprend/vd/<tipo>/<email>/<pwd>', methods=['GET'])
def valida_aprendiz_por_emailvd(tipo,email,pwd):
    aprend="0"
    if tipo=="1":
        try:
            aprend = FichaAprendiz.get_or_none(FichaAprendiz.EMAIL == email )
            
            aa=jsonify(model_to_dict(aprend))
            
            if aprend.PWDAP==pwd:
                return aa
        except Exception as e:    
            return jsonify({"Error":"Las credenciales no coinciden"})
 
@app.route('/inst/<pficha>/<paprendiz>', methods=['GET'])
def noEvaluados(pficha, paprendiz):
    # sql=f"SELECT * FROM FICHAINSTRUCTOR WHERE FICHA='{pficha}' AND DNI NOT IN(SELECT IDINSTRUCTOR FROM THEVAL WHERE IDFICHA='{pficha}' AND IDAPRENDIZ='{paprendiz}')".format(pficha,paprendiz)
    sql=f"SELECT * FROM VINSTRUCTORESP WHERE FICHA={pficha} AND DNIAP={paprendiz}".format(pficha,paprendiz)
    print(sql)
    datos=Consultar(DATABASE,sql)
    return jsonify(datos)
  
@app.route('/inst/contar/<email>', methods=['GET'])
def contar_instructores_por_email(email):
    sql=f"SELECT COUNT(*) CANT FROM VINSTRUCTOR WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    tinstructor=datos[0]['CANT']
    sql=f"SELECT COUNT(*) CANT FROM VAPRENDIZ WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    taprendiz=datos[0]['CANT']
    sql=f"SELECT COUNT(*) CANT FROM VADMIN WHERE EMAIL='{email}'".format(email)
    datos=Consultar(DATABASE,sql)
    tadmin=datos[0]['CANT']
    
    if tinstructor>0:
        tipo=2
    elif taprendiz>0:
        tipo=1
    elif tadmin>0:
        tipo=3
    else:
        tipo=0
        
    total={"Tipo":tipo,"Email":email,"Instructor":tinstructor,"Aprendiz":taprendiz,"Admin":tadmin}
    return jsonify(total)
    # return jsonify({"Tipo":tipo})

@app.route("/menurol/<tipo>")
def menurol(tipo):
    menues = Menu.select().where(Menu.ROL == tipo)
    if menues:
        data = [model_to_dict(menu) for menu in menues]
        return jsonify(data)
    return jsonify({"Error":"No hay opciones"})

@app.route("/v/<tipo>/<usua>/<cla>")
def validaUsuario(tipo,usua,cla):
    if tipo==1:
        menues = Menu.select().where(Menu.ROL == tipo)
    return jsonify({"Error":"No implementado aun"})

validaUsuario
# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True,port=5555)
