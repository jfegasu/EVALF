from flask import Flask, request, jsonify
from peewee import *
from models import *
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

# Ejecutar app
if __name__ == '__main__':
    app.run(debug=True,port=5555)
