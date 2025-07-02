from flask import Flask,current_app
from peewee import MySQLDatabase  

try:
    MYSQL= MySQLDatabase(
'evalf',
user='root',
password='',
host='localhost',
port=3306
)
    db=MYSQL 
except Exception as e:
    print("Fallo la conexion")
   

