# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 18:58:21 2025

@author: FEGASU
"""

import pandas as pd
from funciones import *
import hashlib
from datetime import date
import re
class rutinas:
    __archi  =""  
    workbook=""
    Datos={}
    def setArchivo(self,archi):
        self.__archi=archi
    def getArchivo(self):
        return self.__archi      
    def diff_month(self,d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    def CrearCarpeta(self,ficha,a,cual):
        os.makedirs('./FICHAS/'+ficha+'/'+a[cual], exist_ok=True);    print('Creado .....',a[cual]) 

    def Cambiar(self,df,col,cambia):
        for x in cambia:
            df[col] = df[col].str.replace(r'\s*'+x+'\s*', ' ', regex=True)
    def AEXCEL(self,ruta,df,nom):
        #print(ruta)
        df.to_excel(ruta+"/"+nom+".xlsx", index=False)  
    def AEXCELibroInicio(self,nombre):
        libro=pd.ExcelWriter(nombre)
        return libro
    def AEXCELibro(self,libro,ruta,df,nom):
        #print(ruta)
        df.to_excel(ruta+"/"+nom+".xlsx", index=False)  

    def LeaArchivo(self,cual):
        self.workbook = pd.read_excel(cual)
        

    def SacaPorcion(self,ri,rs):
        x=pd.DataFrame(self.workbook[ri:rs])
        return x
    def SacaFicha(self):
        # x=pd.DataFrame(self.workbook[1:2])
        # print(x)
        # self.ficha=int(x['Unnamed: 2'])
        x=self.workbook.iloc[1]
        self.ficha=x[2]
        self.Datos["Ficha"]=x[2]
    def SacaCodigo(self):
        # x=pd.DataFrame(self.workbook[1:2])
        # print(x)
        # self.ficha=int(x['Unnamed: 2'])
        x=self.workbook.iloc[2]
        self.codigo=x[2]
        self.Datos["Codigo"]=x[2]
    def SacaRegional(self):
        # x=pd.DataFrame(self.workbook[1:2])
        # print(x)
        # self.ficha=int(x['Unnamed: 2'])
        x=self.workbook.iloc[9]
        self.codigo=x[2]
        self.Datos["Regional"]=x[2]
    def SacaCentro(self):
        # x=pd.DataFrame(self.workbook[1:2])
        # print(x)
        # self.ficha=int(x['Unnamed: 2'])
        x=self.workbook.iloc[10]
        self.codigo=x[2]
        self.Datos["Centro"]=x[2]
        
    def FechaInicio(self):
        x=self.workbook.iloc[6]
        self.FInicio=x[2]
        self.Datos["FInicia"]=x[2]
    def FechaFin(self):
        x=self.workbook.iloc[7]
        self.FFin=x[2]
        self.Datos["FFin"]=x[2]
    def Estado(self):
        x=self.workbook.iloc[5]
        self.FEstado=x[2]
        self.Datos["Estado"]=x[2]
    def FPrograma(self):
        x=self.workbook.iloc[4]
        self.FEstado=x[2]
        self.Datos["Programa"]=x[2]
    def FModalidad(self):
        x=self.workbook.iloc[8]
        self.FModalidad=x[2]
        self.Datos["Modalidad"]=x[2]
    def Encabezado(self):
        self.SacaFicha()
        self.FechaInicio()
        self.FechaFin()
        self.Estado()
        self.FModalidad()
        self.FPrograma()   
        self.SacaCodigo()
        self.SacaRegional()
        self.SacaCentro()

    def SacaFila(self,linea,columna):
        f=self.workbook.loc[linea:columna]
        return f

    def EscribeUnaLinea(self,df,que):
        df.loc[len(df)]=que

    def Extrae(self,data1,sql):
        DM=pd.DataFrame(sqldf(sql))
        DM.drop_duplicates(inplace=True)
        DM['id']=range(1,len(DM)+1)
        DM.set_index('id',inplace=True)
        return DM
    def BorrarCarpeta(self,cual):
        if os.path.exists('./FICHAS/'):
            rmtree('./FICHAS/')
    def CrearCarpetas(self,cual):
        os.makedirs(cual, exist_ok=True)
    def SacaColumna(self,df,cual):
        DM=df[cual]
        DM.drop_duplicates(inplace=True)
        return DM
    def Extrae(self,df,sql):
        data1=df
        DM=pd.DataFrame(sqldf(sql))
        DM.drop_duplicates(inplace=True)
        DM['id']=range(1,len(DM)+1)
        DM.set_index('id',inplace=True)
        return DM


rutinas=rutinas() 
rutinas.LeaArchivo('2826505Reporte de Juicios Evaluativos.xls')
rutinas.Encabezado()
Variables={
    "TITULACION":rutinas.Datos['Programa'],
    "CODIGO":rutinas.Datos['Codigo'],
    "FICHA":rutinas.Datos['Ficha'],
    "ESTADO":rutinas.Datos['Estado'],
    "REGIONAL":rutinas.Datos['Regional'],
    "CENTRO":rutinas.Datos['Centro'],
}
data1=rutinas.workbook.drop(range(0,12),axis=0)
data1.rename(columns={'Reporte de Juicios de Evaluación':'TDOC','Unnamed: 1':'DNI','Unnamed: 2':'NOMBRE','Unnamed: 3':'APELLIDOS','Unnamed: 4':'ESTADO','Unnamed: 5':'COMPETENCIA','Unnamed: 6':'RAP','Unnamed: 7':'EVALUADO','Unnamed: 9':'JUICIO','Unnamed: 10':'INSTRUCTOR'},inplace=True)
del data1['Unnamed: 8']
#data1.rename(columns={'Unnamed: 9':'FJUICIO','Unnamed: 10':'INSTRUCTOR'},inplace=True)
cmalo=[':','\t','\n','\r','%','#']    
rutinas.Cambiar(data1,'RAP',cmalo)


DM_COMPETENCIA=pd.DataFrame(data1,columns=['COMPETENCIA','RAP'])
DM_COMPETENCIA.drop_duplicates(inplace=True)
DM_COMPETENCIA['IDCOMPETENCIA']=range(1,len(DM_COMPETENCIA)+1)
DM_COMPETENCIA['FICHA']=Variables['FICHA']
DM_RAP=pd.DataFrame(DM_COMPETENCIA,columns=['COMPETENCIA','RAP'])
DM_RAP.drop_duplicates(inplace=True)


DM_RAP=pd.merge(DM_COMPETENCIA, DM_RAP,left_on='COMPETENCIA',right_on='COMPETENCIA',how='right')
DM_COMPETENCIA= DM_COMPETENCIA[['IDCOMPETENCIA','FICHA', 'COMPETENCIA']]

del DM_RAP['COMPETENCIA']
del DM_RAP['RAP_y']
DM_RAP.rename(columns={'RAP_x': 'RAP'}, inplace=True)
DM_RAP['IDRAP']=range(1,len(DM_RAP)+1)
DM_RAP['FICHA']=Variables['FICHA']
DM_RAP=DM_RAP[['IDRAP','IDCOMPETENCIA','FICHA', 'RAP']]

DM_APRENDIZ=pd.DataFrame(data1,columns=['DNI','NOMBRE','APELLIDOS','ESTADO'])
DM_APRENDIZ.drop_duplicates(inplace=True)
DM_APRENDIZ['EMAIL']=None
DM_APRENDIZ['FICHA']=Variables['FICHA']
x=DM_APRENDIZ['DNI']
def SacaPWDA(valor):
    x=valor[-4:]
    xx = hashlib.md5(x.encode()).hexdigest()
    return xx

DM_APRENDIZ['PWD']=DM_APRENDIZ['DNI'].apply(SacaPWDA)

# x=str(x)[-4:]
# xx = hashlib.md5(x.encode()).hexdigest()
# DM_APRENDIZ['PWD']=xx
DM_APRENDIZ['FECHA']=date.today()
from datetime import datetime

def obtener_trimestreT(fecha: str):
    if fecha is None or fecha == '':
        return '0'
    
    try:
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d')
        elif not isinstance(fecha, datetime):
            return '0'  # Si no es str ni datetime, lo ignoramos

        mes = fecha.month
        anual = fecha.year
        trimestre = (mes - 1) // 3 + 1
        return f"{anual}-{trimestre}"
    
    except Exception:
        return '0'  # Devuelve '0' si hay error al convertir la fecha



DM_INSTRUCTOR=pd.DataFrame(data1,columns=['JUICIO','INSTRUCTOR'])
DM_INSTRUCTOR=DM_INSTRUCTOR.dropna()

DM_INSTRUCTOR['TRIMESTRE']=DM_INSTRUCTOR['JUICIO'].apply(obtener_trimestreT)
del DM_INSTRUCTOR['JUICIO']
DM_INSTRUCTOR.drop_duplicates(inplace=True)
DM_INSTRUCTOR['EMAIL']=None
DM_INSTRUCTOR['FICHA']=Variables['FICHA']
def SacaDNI(valor):
    x=valor.lstrip()
    inicio = re.search(r'\d', valor).start()
    fin=re.search(r'-', valor).start()
    resultado = x[inicio:fin]
    return resultado
def SacaNOMI(valor):
    x=valor.lstrip()
    inicio = re.search(r'\d', valor).start()
    inicio=re.search(r'-', valor).start()
    resultado = x[inicio+2:]
    return resultado

DM_INSTRUCTOR['DNI']=DM_INSTRUCTOR['INSTRUCTOR'].apply(SacaDNI)
DM_INSTRUCTOR['NOM']=DM_INSTRUCTOR['INSTRUCTOR'].apply(SacaNOMI)
def SacaPWDI(valor):
    x=valor[-5:]
    xx = hashlib.md5(x.encode()).hexdigest()
    return xx

DM_INSTRUCTOR['PWD']=DM_INSTRUCTOR['DNI'].apply(SacaPWDI)

del DM_INSTRUCTOR['INSTRUCTOR']
DM_INSTRUCTOR['FECHA']=date.today()


DM_JUICIO=pd.DataFrame(data1,columns=['DNI','ESTADO','EVALUADO','COMPETENCIA', 'RAP', 'JUICIO','INSTRUCTOR'])
DM_JUICIO['FICHA']=Variables['FICHA']
DM_JUICIO.drop_duplicates(inplace=True)
DM_JUICIO['TRIMESTRE']=DM_JUICIO['JUICIO'].apply(obtener_trimestreT)
del DM_JUICIO['JUICIO']

DM_JUICIO['INSTRUCTOR']=DM_JUICIO['INSTRUCTOR'].replace('  -   ','SIN EVALUAR')

DM_APRENDIZ['ESTADO'] = DM_APRENDIZ['ESTADO'].astype(str).str.strip().str.upper()
DM_FORMACION=sqldf("SELECT * FROM data1 where ESTADO='EN FORMACION' AND NOT ESTADO='RETIRO VOLUNTARIO'")

# DM_RETIRO = data1[data1['ESTADO'].isin(['RETIRO VOLUNTARIO'])]

DM_CANCELADO=data1[data1['ESTADO'] == 'CANCELADO']
del DM_CANCELADO['JUICIO']
del DM_CANCELADO['RAP']
del DM_CANCELADO['INSTRUCTOR']
del DM_CANCELADO['COMPETENCIA']
del DM_CANCELADO['EVALUADO']

DM_RETIROV=data1[data1['ESTADO'] == 'RETIRO VOLUNTARIO']
del DM_RETIROV['JUICIO']
del DM_RETIROV['RAP']
del DM_RETIROV['INSTRUCTOR']
del DM_RETIROV['COMPETENCIA']
del DM_RETIROV['EVALUADO']


DM_RETIROV.drop_duplicates(inplace=True)
DM_CANCELADO.drop_duplicates(inplace=True)


print(DM_APRENDIZ['ESTADO'].unique())
print(len(DM_APRENDIZ['ESTADO']== 'CANCELADO'))
# DM_CANCELADON=DM_JUICIO[['DNI']]
# DM_CANCELADON=pd.merge(DM_APRENDIZ,DM_CANCELADO,left_on='DNI',right_on='DNI',how="left")
# DM_CANCELADON.drop_duplicates(inplace=True)
# del DM_CANCELADON['PWD']
# del DM_CANCELADON['EMAIL']
# del DM_CANCELADON['ESTADO_y']

DM_XEVALUARXRAPXAPRENDIZ=data1[(data1['EVALUADO'] == 'POR EVALUAR')  & (data1['ESTADO'] == 'EN FORMACION') ]
del DM_XEVALUARXRAPXAPRENDIZ['JUICIO']
del DM_XEVALUARXRAPXAPRENDIZ['COMPETENCIA']
del DM_XEVALUARXRAPXAPRENDIZ['INSTRUCTOR']
del DM_XEVALUARXRAPXAPRENDIZ['EVALUADO']

def ContarXEvaluar(que):
    Hay = DM_JUICIO[(DM_JUICIO['DNI'] == que) & (DM_JUICIO['ESTADO'] == 'EN FORMACION') & (DM_JUICIO['INSTRUCTOR'] == 'SIN EVALUAR') ].shape[0]
    return Hay
def ContarAprobados(que):
    Hay = DM_JUICIO[(DM_JUICIO['DNI'] == que) & (DM_JUICIO['ESTADO'] == 'EN FORMACION') & (DM_JUICIO['INSTRUCTOR'] != 'SIN EVALUAR') ].shape[0]
    return Hay

DM_XEVALUARXRAP=data1[(data1['EVALUADO'] == 'POR EVALUAR')  & (data1['ESTADO'] == 'EN FORMACION') ]
del DM_XEVALUARXRAP['JUICIO']
del DM_XEVALUARXRAP['COMPETENCIA']
del DM_XEVALUARXRAP['INSTRUCTOR']
del DM_XEVALUARXRAP['EVALUADO']
del DM_XEVALUARXRAP['DNI']
del DM_XEVALUARXRAP['NOMBRE']
del DM_XEVALUARXRAP['APELLIDOS']
del DM_XEVALUARXRAP['TDOC']


DM_XEVALUARXCOMPETENCIA=data1[(data1['EVALUADO'] == 'POR EVALUAR')  & (data1['ESTADO'] == 'EN FORMACION') ]
del DM_XEVALUARXCOMPETENCIA['JUICIO']
del DM_XEVALUARXCOMPETENCIA['RAP']
del DM_XEVALUARXCOMPETENCIA['INSTRUCTOR']
del DM_XEVALUARXCOMPETENCIA['EVALUADO']
DM_XEVALUARXCOMPETENCIA.drop_duplicates(inplace=True)

DM_XEVALUARXAPRENDIZ=data1[(data1['EVALUADO'] == 'POR EVALUAR')  & (data1['ESTADO'] == 'EN FORMACION') ]
DM_XEVALUARXAPRENDIZ['APRENDIZ']=DM_XEVALUARXAPRENDIZ['APELLIDOS']+DM_XEVALUARXAPRENDIZ['NOMBRE']
# DM_XEVALUARXAPRENDIZ['DNI']=DM_XEVALUARXAPRENDIZ['TDOC']+DM_XEVALUARXAPRENDIZ['DNI']

del DM_XEVALUARXAPRENDIZ['JUICIO']
del DM_XEVALUARXAPRENDIZ['RAP']
del DM_XEVALUARXAPRENDIZ['INSTRUCTOR']
del DM_XEVALUARXAPRENDIZ['EVALUADO']
del DM_XEVALUARXAPRENDIZ['COMPETENCIA']
del DM_XEVALUARXAPRENDIZ['NOMBRE']
del DM_XEVALUARXAPRENDIZ['APELLIDOS']

DM_XEVALUARXAPRENDIZ['RAPSINEVALUAR'] = data1['DNI'].apply(ContarXEvaluar)
DM_XEVALUARXAPRENDIZ['RAPAPROBADOS'] = data1['DNI'].apply(ContarAprobados)

DM_XEVALUARXAPRENDIZ.drop_duplicates(inplace=True)

with pd.ExcelWriter("./"+str(rutinas.Datos['Ficha'])+".xlsx") as writer:
    DM_APRENDIZ.to_excel(writer,sheet_name="APRENDICES", index=False)
    DM_CANCELADO.to_excel(writer,sheet_name="CANCELADOS", index=False)
    DM_FORMACION.to_excel(writer,sheet_name="EN_FORMACION", index=False)
    DM_RETIROV.to_excel(writer,sheet_name="RETIRO VOLUNTARIO", index=False)
    DM_XEVALUARXRAP.to_excel(writer,sheet_name="XEVALUARXRAP", index=False)
    DM_XEVALUARXAPRENDIZ.to_excel(writer,sheet_name="XEVALUARXAPRENDIZ", index=False)
    DM_XEVALUARXCOMPETENCIA.to_excel(writer,sheet_name="XEVALUARXCOMPETENCIA", index=False)
    
    DM_JUICIO.to_excel(writer,sheet_name="JUICIOS", index=False)
    DM_COMPETENCIA.to_excel(writer,sheet_name="COMPETENCIAS", index=False)
    DM_RAP.to_excel(writer,sheet_name="RAP", index=False)
    DM_INSTRUCTOR.to_excel(writer,sheet_name="INSTRUCTOR", index=False)
    
        



    
        






