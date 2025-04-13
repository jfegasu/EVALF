import pandas as pd
from utils.Utilitarios import *
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'EVALF.db')
XLS=os.path.join(BASE_DIR, 'CARGA.xlsx')
print('CARGANDO APRENDICES')
sql="DELETE FROM FICHAPRENDIZ"
Ejecutar(DATABASE,sql)
datos=pd.read_excel(XLS,sheet_name=1)
# print(datos)
aprendiz=pd.DataFrame(datos[['FICHA','DNI','NOMBRE','EMAIL','TITULACION']])
aprendiz.drop_duplicates(inplace=True)
aprendiz.fillna("SINCORREO",inplace=True)
aprendiz.to_csv("aprendiz.csv",index=False)
for index, row in aprendiz.iterrows():
    x=row['DNI']
    x=str(x)[-4:]
    # print(x)
    # x=hash(x)
    sql=f"INSERT INTO FICHAPRENDIZ(FICHA,DNIA,NOMBREAP,ESTADOAP,PWDAP,EMAIL,TITULACION) VALUES('{row['FICHA']}','{row['DNI']}','{row['NOMBRE']}',1,'{x}','{row['EMAIL']}','{row['TITULACION']}')".format(row['FICHA'],row['DNI'],row['NOMBRE'],1,x,row['EMAIL'],row['TITULACION'])
    Ejecutar(DATABASE,sql)
print('CARGANDO INSTRUCTORES')
sql="DELETE FROM FICHAINSTRUCTOR"
Ejecutar(DATABASE,sql)
datos=pd.read_excel(XLS,sheet_name=0)
instructor=pd.DataFrame(datos[['FICHA','DNI','NOMBRE','EMAIL']])
instructor.drop_duplicates(inplace=True)
instructor.to_csv("instructor.csv",index=False)
for index, row in instructor.iterrows():
    # print(row['FICHA'],row['DNI'],row['NOMBRE'],row['EMAIL'])
    sql=f"INSERT INTO FICHAINSTRUCTOR(FICHA,DNI,NOMINST,EMAIL) VALUES('{row['FICHA']}','{row['DNI']}','{row['NOMBRE']}','{row['EMAIL']}')".format(row['FICHA'],row['DNI'],row['NOMBRE'],row['EMAIL'])
    # print(sql)
    Ejecutar(DATABASE,sql)
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

print("PROCESO TERMINADO")