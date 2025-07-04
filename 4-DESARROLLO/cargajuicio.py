# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 18:58:21 2025

@author: FEGASU
"""

import pandas as pd
from funciones import *
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
rutinas.LeaArchivo('3147247Reporte de Juicios Evaluativos.xls')
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
data1.rename(columns={'Reporte de Juicios de Evaluación':'TDOC','Unnamed: 1':'DNI','Unnamed: 2':'NOMBRE','Unnamed: 3':'APELLIDOS','Unnamed: 4':'ESTADO','Unnamed: 5':'COMPETENCIA','Unnamed: 6':'RAP','Unnamed: 9':'JUICIO','Unnamed: 10':'INSTRUCTOR'},inplace=True)
#data1.rename(columns={'Unnamed: 9':'FJUICIO','Unnamed: 10':'INSTRUCTOR'},inplace=True)
cmalo=[':','\t','\n','\r','%','#']    
rutinas.Cambiar(data1,'RAP',cmalo)

DM_COMPETENCIA=pd.DataFrame(data1,columns=['COMPETENCIA','RAP'])
DM_COMPETENCIA.drop_duplicates(inplace=True)
DM_COMPETENCIA['IDCOMPETENCIA']=range(1,len(DM_COMPETENCIA)+1)

DM_RAP=pd.DataFrame(DM_COMPETENCIA,columns=['COMPETENCIA','RAP'])
DM_RAP.drop_duplicates(inplace=True)

DM_RAP=pd.merge(DM_COMPETENCIA, DM_RAP,left_on='COMPETENCIA',right_on='COMPETENCIA',how='right')
del DM_COMPETENCIA['RAP']
del DM_RAP['COMPETENCIA']
del DM_RAP['RAP_y']
DM_RAP.rename(columns={'RAP_x': 'RAP'}, inplace=True)

DM_APRENDIZ=pd.DataFrame(data1,columns=['DNI','NOMBRE','APELLIDOS','ESTADO'])
DM_APRENDIZ.drop_duplicates(inplace=True)

def obtener_trimestreT(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    
    mes = fecha.month
    anual=fecha.year
    trimestre = (mes - 1) // 3 + 1
    return str(anual)+"-"+str(trimestre)


DM_INSTRUCTOR=pd.DataFrame(data1,columns=['JUICIO','INSTRUCTOR'])
DM_INSTRUCTOR=DM_INSTRUCTOR.dropna()

DM_INSTRUCTOR['TRIMESTRE']=DM_INSTRUCTOR['JUICIO'].apply(obtener_trimestreT)
del DM_INSTRUCTOR['JUICIO']
DM_INSTRUCTOR.drop_duplicates(inplace=True)




    
        






