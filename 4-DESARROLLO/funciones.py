# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 09:16:09 2024

@author: Administrador
"""
import pandas as pd
import sqlite3
from pandasql import sqldf
import os
from shutil import rmtree

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def CrearCarpeta(ficha,a,cual):
    os.makedirs('./FICHAS/'+ficha+'/'+a[cual], exist_ok=True);    print('Creado .....',a[cual]) 

def Cambiar(df,col,cambia):
    for x in cambia:
        df[col] = df[col].str.replace(r'\s*'+x+'\s*', ' ', regex=True)
def AEXCEL(ruta,df,nom):
    #print(ruta)
    df.to_excel(ruta+"/"+nom+".xlsx", index=False)  
def AEXCELibroInicio(nombre):
    libro=pd.ExcelWriter(nombre)
    return libro
def AEXCELibro(libro,ruta,df,nom):
    #print(ruta)
    df.to_excel(ruta+"/"+nom+".xlsx", index=False)  

def LeaArchivo(cual):
    w = pd.read_excel(cual)
    return w

def SacaPorcion(df,ri,rs):
    f=pd.DataFrame(df[ri:rs])
    return f

def SacaFila(df,linea,columna):
    f=df.loc[linea,columna]
    return f

def EscribeUnaLinea(df,que):
    df.loc[len(df)]=que

def Extrae(data1,sql):
    DM=pd.DataFrame(sqldf(sql))
    DM.drop_duplicates(inplace=True)
    DM['id']=range(1,len(DM)+1)
    DM.set_index('id',inplace=True)
    return DM
def BorrarCarpeta(cual):
    if os.path.exists('./FICHAS/'):
        rmtree('./FICHAS/')
def CrearCarpetas(cual):
    os.makedirs(cual, exist_ok=True)
def SacaColumna(df,cual):
    DM=df[cual]
    DM.drop_duplicates(inplace=True)
    return DM
def obtener_trimestreT(fecha):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    
    mes = fecha.month
    anual=fecha.year
    trimestre = (mes - 1) // 3 + 1
    return "T"+str(anual)+"-"+str(trimestre)