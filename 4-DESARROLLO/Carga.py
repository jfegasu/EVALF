from flask import Flask, request, jsonify
import pandas as pd
from utils.Utilitarios import *
import os
import glob
import platform
import hashlib
def Cargando():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE = os.path.join(BASE_DIR, 'database', 'sena.db')
    # return "400"+DATABASE
    XLS=os.path.join(BASE_DIR, 'CARGA.xlsx')
    # INICIO=os.path.join(BASE_DIR, 'app.pyw')
    # if platform.system()=="Windows":
        # RegEdInicio("EVALF",INICIO)
    print('CARGANDO APRENDICES')
    sql="DELETE FROM FICHAAPRENDIZ"
    # conn = sqlite3.connect(DATABASE)
    # cursor = conn.cursor()
    # cursor.execute(sql)
    # conn.commit()
    # conn.close()
    Ejecutar(DATABASE,sql)
    # return DATABASE
    
    datos=pd.read_excel(XLS,sheet_name=1)
    # print(datos)
    aprendiz=pd.DataFrame(datos[['FICHA','DNI','NOMBRE','EMAIL','TITULACION']])
    aprendiz.drop_duplicates(inplace=True)
    aprendiz.fillna("SINCORREO",inplace=True)
    aprendiz.to_csv("aprendiz.csv",index=False)
    for index, row in aprendiz.iterrows():
        x=row['DNI']
        x=str(x)[-4:]
        xx = hashlib.md5(x.encode()).hexdigest()
        print(xx)
        # x=hash(x)
        sql=f"INSERT INTO FICHAAPRENDIZ(FICHA,DNIA,NOMBREAP,ESTADOAP,PWDAP,EMAIL,TITULACION) VALUES('{row['FICHA']}','{row['DNI']}','{row['NOMBRE']}',1,'{xx}','{row['EMAIL']}','{row['TITULACION']}')".format(row['FICHA'],row['DNI'],row['NOMBRE'],1,xx,row['EMAIL'],row['TITULACION'])
        print("->",sql)
        Ejecutar(DATABASE,sql)
    # os.remove("aprendiz.csv")
    print('CARGANDO INSTRUCTORES')
    sql="DELETE FROM FICHAINSTRUCTOR"
    Ejecutar(DATABASE,sql)
    datos=pd.read_excel(XLS,sheet_name=0)
    instructor=pd.DataFrame(datos[['FICHA','DNI','NOMBRE','EMAIL']])
    instructor.drop_duplicates(inplace=True)
    instructor.to_csv("instructor.csv",index=False)
    TRIMESTRE=obtener_trimestre(datetime.now())
    for index, row in instructor.iterrows():
        # print(row['FICHA'],row['DNI'],row['NOMBRE'],row['EMAIL'])
        x=row['DNI']
        x=str(x)[-4:]
        xx = hashlib.md5(x.encode()).hexdigest()
        
        sql=f"INSERT INTO FICHAINSTRUCTOR(FICHA,DNI,NOMINST,EMAIL,TRIMESTRE,PWD) VALUES('{row['FICHA']}','{row['DNI']}','{row['NOMBRE']}','{row['EMAIL']}',{TRIMESTRE},'{xx}')".format(row['FICHA'],row['DNI'],row['NOMBRE'],row['EMAIL'],TRIMESTRE,xx)
        # print(sql)
        Ejecutar(DATABASE,sql)
    # os.remove("instructor.csv")

    print('CARGANDO PREGUNTAS')
    sql="DELETE FROM PREGUNTA"
    Ejecutar(DATABASE,sql)
    datos=pd.read_excel(XLS,sheet_name=2)
    preguntas=pd.DataFrame(datos[['ENUNCIADO','CATEGORIAS']])
    preguntas.drop_duplicates(inplace=True)
    preguntas.to_csv("preguntas.csv",index=False)
    for index, row in preguntas.iterrows():
        # print(row['FICHA'],row['DNI'],row['NOMBRE'],row['EMAIL'])
        sql=f"INSERT INTO PREGUNTA(DESCRIPCION,ESTADO,VALORES) VALUES('{row['ENUNCIADO']}',1,'{row['CATEGORIAS']}')".format(row['ENUNCIADO'],row['CATEGORIAS'])
        # print(sql)
        Ejecutar(DATABASE,sql)
    # os.remove("preguntas.csv")

    print('BORRANDO TABLA DE RESPUESTAS')
    sql="DELETE FROM THEVAL"
    Ejecutar(DATABASE,sql)
    archivos_csv = glob.glob("*.csv")
    for archivo in archivos_csv:
        try:
            os.remove(archivo)
            print(f"Archivo eliminado: {archivo}")
        except Exception as e:
            print(f"No se pudo eliminar {archivo}: {e}")
    
    return  "200 - PROCESO TERMINADO CON EXITO"