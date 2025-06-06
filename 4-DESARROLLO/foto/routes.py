from flask import Blueprint,render_template,url_for
foto = Blueprint('foto', __name__, template_folder='templates')

@foto.route('/')
def index():
    
    return render_template('foto_index.html')