from flask import request,render_template,session
import logging
import requests
import os
from datetime import datetime
import re
import string
# import winreg
# pip install Flask Flask-Mail
# pip install --upgrade requests
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import sqlite3
from flask import current_app as app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))




class Api:
    def __init__(self,url="http://127.0.0.1:5556"):
        self.url = url  
        self.Estado=None     
    def ConsultaApi(self,clave):
        response = requests.get(self.url+clave) 
        self.Estado=response.status_code
        return  response.text
    def PostApi(self,clave,datos):
        response = requests.post(self.url+clave, json=datos)  
        return response.status_code   

class Auditor():
    logger=None
    def __init__(self,base1):
        
        fecha=datetime.now()
        fe=str(fecha.year)+str(fecha.month)+str(fecha.day)
        # print("** Inicia **")
        LOG = os.path.join('/log')
        # os.makedirs(LOG,exist_ok=True)
        logger = logging.getLogger('werkzeug')
        self.logger =logger 
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s ',filename=LOG+'/'+fe+'.log', encoding='utf-8',level=logging.WARNING)
        self.logger.setLevel(logging.WARNING  )
        # logger.setLevel(logging.INFO)
        # self.logger.warning("inicia")
    
    def logstart(self):
        return self.logger
    
    def registra(self,tipo,msg,usua="-"):
        client_ip = request.remote_addr
        if tipo==10:
            self.logger.debug(client_ip+' '+msg+' ['+usua+']')
        elif tipo==20:
            # print(client_ip+' '+msg+' '+usua)
            self.logger.info(client_ip+' '+msg+' '+usua)
        elif tipo==30:
            a=30
            # self.logger.warning(client_ip+' '+msg+' '+usua)
        elif tipo==40:
            # print(client_ip+' '+msg+' '+usua)
            self.logger.error(client_ip+' '+msg+' ['+usua+']')
        elif tipo==50:
            self.logger.critical(client_ip+' '+msg+' '+usua)
        elif tipo==60:
            self.logger.exception(client_ip+' '+msg+' '+usua)

class Utiles(Auditor):
    
    @classmethod
    def ConsistenciaClave(cs,datos):
            
            mayusculas = len([c for c in datos if c.isupper()])
            minusculas = len([c for c in datos if c.islower()])
            numeros = len([c for c in datos if c.isdigit()])
            canti=len(datos)
            
            espe=0
            caracteres = ['@', '#', '!', '*']
            for ca in datos:
                if ca not in string.ascii_letters and ca not in string.digits:
                    for char in caracteres:
                        cuenta = datos.count(char)
                        if cuenta:
                            espe+=1                
            print(f"datos={datos},mayusculas={mayusculas},minusculas={minusculas}, numeros={numeros}, longitud={canti},especiales={espe}")
            if mayusculas>=1 and minusculas>=1 and numeros>=1 and canti>=12 and espe>=1:
                return True
            else:
                return False
    @classmethod
    def Inyeccion(cs,dato,donde=" " ):
        Au=Auditor()
        patron=["--",';','union',"'"," or "," and ", "drop ",'1=1','1 = 1','"']
        for cadena in patron:
            resultado = re.search(cadena, dato.lower())   
            if resultado:
                 Au.registra(40,'Posible ataque de inyeccion sql ['+dato+'] '+donde)
                 return 'Posible ataque de inyeccion sql ['+dato+'] '+donde
        return 'x'  
    @classmethod
    def ValidaSesion(cs):
        if 'usuario' not in session or session['usuario'] is None:
            return True
        else:
            return False
# def RegEdInicio(clave,Valor):
    # reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")
    # winreg.SetValueEx(reg_key, clave, 0, winreg.REG_SZ, Valor)
    # winreg.CloseKey(reg_key)   
    
 
# def RegEdCrea(clave, Valor):
#     reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\InventaDB") 
#     winreg.SetValueEx(reg_key, clave, 0, winreg.REG_SZ, Valor) 
#     winreg.CloseKey(reg_key)
#     return "Ok"

# def getRegEd(clave):
#     reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\InventaDB")
#     valor, tipo = winreg.QueryValueEx(reg_key, clave)
#     return valor                   

# def EnviaCorreo(Para,Asunto,Cuerpo):
#     clave=getRegEd('pwd')
#     msg = EmailMessage()
    
#     msg['Subject'] = Asunto
#     msg['From'] = 'jfegasu@gmail.com'
#     msg['To'] = Para
    
#     msg.set_content(Cuerpo)
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login('jfegasu@gmail.com', clave)
#         smtp.send_message(msg)

# def CorreosHTML(Para,Asunto,Cuerpo):
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     password=getRegEd('pwd')
#     msg = MIMEMultipart('alternative')
#     username='jfegasu@gmail.com'
#     msg['Subject'] = Asunto
#     msg['From'] = username
#     msg['To'] = Para
    
#     html = """
# <html>
#   <body>
#     <div style="width:100%;overflow:auto" class="w3-w3-green mx-auto">
#       <img loading="lazy" class="tabla" src="https://blogger.googleusercontent.com/img/a/AVvXsEimdqxynaYJeDRuTUp3lzEWFnnQSC2KTVSxvnV70I2eZ5tOCfjwdNnExSTSm2tCf1xBFHVHwsN80OCpDCO0J80UTNWxPC86s7s5aB8rnizg7guNowqTxhr5Fd9WH48n7pn8uLZNFTgXuSGUH6BNncmfQEpOz9pAe_T0zD8n2-aGZk8-C_l6GWk-aq60fQ=s960" style="border:true;width:95%;border-color:black;height:100px;"><br>
#     </div>"""+Cuerpo+""" <br><br><br>
#     <div   style="background-color:green; color:white;padding: 15px 0px 15px 60px;"><b>Servicio Nacional de Aprendizaje SENA - Centro de Gestión de Mercados, Logística y Tenologías de la Información - Regional Distrito Capital <br />Dirección: Cl 52 N&#176; 13 65 -Telefono: +(57) 601 594 1301<br />Conmutador Nacional (601) 5461500 - Extensiones <br /> El SENA brinda a la ciudadanía, atención presencial en las 33 Regionales y 117 Centros de Formación
#  <br />Atención al ciudadano: Bogotá (601) 3430111 - Línea gratuita y resto del país 018000 910270 <br />Atención al empresario: Bogotá (601) 3430101 - Línea gratuita y resto del país 018000 910682</p></div>
#   </body>
# </html>
# """
#     msg.attach(MIMEText(html, 'html'))

# # Enviar el correo
#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(username, password)
#         server.sendmail(msg['From'], msg['To'], msg.as_string())
#         server.quit()
#         print("Correo enviado exitosamente")
#     except Exception as e:
#         print(f"Error al enviar el correo: {e}")    

def CargaMenu(rol):
    conn = sqlite3.connect('database/sena.db')
    cursor = conn.cursor()
    sql="select * from menu where rol='%s'" % rol
    sql1=(rol)
    cursor.execute(sql)
    output = cursor.fetchall() 
    return output

def getRol(login):
    conn = sqlite3.connect('database/sena.db')
    cursor = conn.cursor()
    
    cursor.execute(f"select * from usuario where login='%s'"  % login)
    output = cursor.fetchone() 
    return output
def valideUsuario(login,pw):
    conn = sqlite3.connect('database/EVALF.db')
    cursor = conn.cursor()
    sql=f"select cla from usuario where login='%s'"  % login
    cursor.execute(sql)
    output = cursor.fetchone() 
    if output is None:
        return False
    # print("********************",output[0])
    if pw==output[0]:
        return True
    else:
        return False
def crearTabla(tabla,columns,condicion):
    conn = sqlite3.connect('database/EVALF.db')
    cursor = conn.cursor()
    sql="select "
    k=0
    for hay in columns:
        k=k+1
    print(k)
    
    i=1
    for key in columns:
        if i<k:
            sql+=key+","
            i=i+1
        else:
           sql+=key
           i=i+1 
   
    if condicion is None:
        sql+=" from "+tabla+" " 
    else:
        sql+=" from "+tabla+" where "     
        i=0
        for key,value in condicion.items():
            if i==0:
                sql+=" "+key+"="+value
                i=i+1
            else:
                sql+=" and "+key+"="+value
    cursor.execute(sql)
    output = cursor.fetchall() 
    row=[]
    for rows in output:
        row.append(rows)
    # return row
    return sql
def ConsultarDB(clave):
    url=app.config['apidb']+clave
    response = requests.get(url)
    print("xxx>",response.status_code,url)
    if response.status_code == 200:
        data = response.json()
    # else:
    #     data={"Tipo":0} 
    return response.json()
 
def Ejecutar(db,sql):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return '200' 
    except Exception as e:
        print(e)
        return("400")
def ConsultarD(db, sql):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row  # <- necesario para acceder por nombre de columna
    cursor = conn.cursor()
    cursor.execute(sql)
    output = cursor.fetchall()
    conn.close()
    
    resultados = [dict(row) for row in output]
    return resultados

def Consultar(db,sql):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    output = cursor.fetchall() 
    conn.close()
    return output 
def ConsultarUno(db,sql):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    output = cursor.fetchone() 
    conn.close()
    return output 
 
def obtener_trimestre(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    
    mes = fecha.month
    trimestre = (mes - 1) // 3 + 1
    return trimestre
def obtener_trimestreT(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    
    mes = fecha.month
    anual=fecha.year
    trimestre = (mes - 1) // 3 + 1
    return "T"+str(anual)+"-"+str(trimestre)

menu = [
    {
        "titulo": "CONFIGURACION",
        "items": [
            {"texto": "DATOS INICIALES", "url": "/construir","svg":"","fa":"fa fa-address-book"},
            {"texto": "APERTURA ENCUESTA", "url": "/construir","svg":"9211","fa":""}
        ]
    },
    {
        "titulo": "CARGUE DE DATOS",
        "items": [
            {"texto": "CARGA MASIVA", "url": "/CargaInicial","svg":"9981","fa":""},
            {"texto": "APRENDICES", "url": "/construir","svg":"","fa":"fa fa-users"},
            {"texto": "INSTRUCTORES", "url": "/construir","svg":"","fa":"fa fa-graduation-cap"},
            {"texto": "PREGUNTAS", "url": "/construir","svg":"","fa":"fa fa-question"},
        ]
    },
    {
    "titulo": "RESULTADOS",
        "items": [
            {"texto": "EXPORTAR RESULTADOS(CSV)", "url": "/resp","svg":"","fa":"fa fa-table"},
        ]
    },
        {
    "titulo": "AUDITORIA",
        "items": [
            {"texto": "DESCARGA LOG TRANSACCIONES", "url": "/descargarlog","svg":"","fa":"fa fa-cloud-download"},
            {"texto": "VER LOG DE TRANSACCIONES", "url": "/verlog","svg":"","fa":"fa fa-television"},
        ]
    },
]
