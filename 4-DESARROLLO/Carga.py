import pandas as pd
from utils.Utilitarios import *
print('CARGANDO APRENDICES')
sql="DELETE FROM FICHAPRENDIZ"
Ejecutar(sql)
datos=pd.read_excel("CARGA.xlsx",sheet_name=1)
# print(datos)
aprendiz=pd.DataFrame(datos[['FICHA','DNI','NOMBRE','EMAIL','TITULACION']])
aprendiz.drop_duplicates(inplace=True)
aprendiz.to_csv("aprendiz.csv",index=False)
for index, row in aprendiz.iterrows():
    sql=f"INSERT INTO FICHAPRENDIZ(FICHA,DNIA,NOMBREAP,ESTADOAP,PWDAP,EMAIL,TITULACION) VALUES('{row['FICHA']}','{row['DNI']}','{row['NOMBRE']}',1,'{row['DNI']}','{row['EMAIL']}','{row['TITULACION']}')".format(row['FICHA'],row['DNI'],row['NOMBRE'],1,row['DNI'],row['EMAIL'],row['TITULACION'])
    Ejecutar(sql)
print('CARGANDO INSTRUCTORES')
sql="DELETE FROM FICHAINSTRUCTOR"
Ejecutar(sql)
datos=pd.read_excel("CARGA.xlsx",sheet_name=0)
instructor=pd.DataFrame(datos[['FICHA','DNI','NOMBRE','EMAIL']])
instructor.drop_duplicates(inplace=True)
instructor.to_csv("instructor.csv",index=False)
for index, row in instructor.iterrows():
    # print(row['FICHA'],row['DNI'],row['NOMBRE'],row['EMAIL'])
    sql=f"INSERT INTO FICHAINSTRUCTOR(FICHA,DNI,NOMINST,EMAIL) VALUES('{row['FICHA']}','{row['DNI']}','{row['NOMBRE']}','{row['EMAIL']}')".format(row['FICHA'],row['DNI'],row['NOMBRE'],row['EMAIL'])
    # print(sql)
    Ejecutar(sql)

print("PROCESO TERMINADO")