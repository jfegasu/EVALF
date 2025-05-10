from flask import Flask, request, jsonify
from peewee import *
from models import *
from playhouse.shortcuts import model_to_dict
from peewee import fn

# Configuración de base de datos
db = SqliteDatabase('sena.db')

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
@app.route('/inst/<dni>', methods=['GET'])
def obtener_instructor_por_dni(dni):
    inst = FichaInstructor.get_or_none(FichaInstructor.DNI == dni)
    if inst:
        return jsonify(model_to_dict(inst))
    return jsonify({'error': 'Instructor no encontrado'}), 404
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
    

@app.route('/inst/contar/<email>', methods=['GET'])
def contar_instructores_por_email(email):
    tinstructor = (FichaInstructor
              .select(fn.COUNT(FichaInstructor.id).alias('total'))
              .where(FichaInstructor.EMAIL == email)
              .scalar())  # Devuelve el valor directo, no una fila
    taprendiz = (FichaAprendiz
              .select(fn.COUNT(FichaAprendiz.id).alias('total'))
              .where(FichaAprendiz.EMAIL == email)
              .scalar())  # Devuelve el valor directo, no una fila
    tadmin = (Admin
              .select(fn.COUNT(Admin.id).alias('total'))
              .where(Admin.EMAIL == email)
              .scalar())  # Devuelve el valor directo, no una fila
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
