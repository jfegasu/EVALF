from flask import Blueprint,render_template,session,request,jsonify
import requests
from config import apidb,BASE_DIR
from database.models import *
import os
from utils.Utilitarios import *
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


eval_bp = Blueprint('eval', __name__, template_folder='templates',static_folder='static', static_url_path='/encuesta/static')
@eval_bp.route('/')
def index(): 
    usua=session['usua']   
    au=Auditor(BASE_DIR)
    au.registra(30,'Entra a responder la encuesta',usua) 
    
    datos=requests.get(f'{apidb}/u/datos/{usua}').json()
    ficha=requests.get(f'{apidb}/a/1/{usua}').text
    session['datos']=datos
    aa=f'{apidb}/i/2/{ficha}/{usua}'
    datos=requests.get(aa).json()
    return render_template('carga.html',N=1,datos=datos,apr=session['datos'])
@eval_bp.route('/1/<I>' ,methods=['POST','GET']) 
def eval1(I):  
    
    F=session['ficha']
    A=session['dnia']
    sql=f"SELECT * FROM THEVAL WHERE idFICHA={F} AND idAPRENDIZ={A}".format(F,A)
    datos=ConsultarUno(DATABASE,sql)
    
    session['instructor']=datos[3]
    I=session['instructor']
    datos=[N,F,I,A]
    return render_template('carga.html',N=1,datos=datos)
@eval_bp.route('/2/<I>' ,methods=['GET']) 
def eval2a(I):  
    # return '/2/<I>'
    # F=session['ficha']
    F=3147246
    # A=session['dnia']
    A=1013106019
    # I=session['instructor']
    N=2
    datos=[2,F,I,A]
    print("__________________________>",N)
    # preg=Consultar(DATABASE,'SELECT * FROM PREGUNTA WHERE ESTADO=1')
    # hay=len(preg)
    preg=requests.get(f'{apidb}/p').json()
    hay=len(preg)

    
    # au.registra(30,'ENTRA A EVALUAR A: '+getInstructor(I))
    # apr={
    #         "ficha":session['datos'].FICHA,
    #         "aprendiz":session['datos'].NOMBREAP,
    #         "titulacion":session['titulacion'],
    #         "dnia":session['dnia']
    #     }
    
    # session['apr']=apr
    NOMI=requests.get(f'{apidb}/i/e/{I}').json()
    # return NOMI[0]['NOMINST']
    return render_template('carga.html',N=2,datos=datos,hay=hay,preg=preg,nomi=NOMI[0]['NOMINST'],apr=session['datos'])

@eval_bp.route('/3/<I>' ,methods=['POST','GET']) 
def eval(I):  
    # return session['datos']['FICHA']
    F=session['datos']['FICHA']
    A=session['datos']['DNI']
    T=session['datos']['TITULACION']
    TRIMESTRE=obtener_trimestreT(datetime.now())
    
    
    conta = int(request.form.get('conta'))

    for i in range(1, conta + 1):  # Asegúrate de incluir el último valor
        Resp=request.form.get('R' + str(i))
        Preg=request.form.get('P' + str(i)) 
        pre=TheVal.create(idINSTRUCTOR=I,idFICHA=F,idAPRENDIZ=A,PREGUNTA=Preg,RESPUESTA=Resp,TITULACION=T,TRIMESTRE=TRIMESTRE)
    # au.registra(30,'EVALUO A: '+getInstructor(I))
    msgito="Respuestas registrada"
    regreso="/login"
    return render_template("alertas.html",msgito=msgito,regreso=regreso)

