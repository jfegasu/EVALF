from flask import Flask,current_app
from peewee import MySQLDatabase  

MYSQL= MySQLDatabase(
'evalf',
user='root',
password='',
host='localhost',
port=3306
)
db=MYSQL    

# current_app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# current_app.config['MYSQL_DATABASE_USER'] = 'root'
# current_app.config['MYSQL_DATABASE_PASSWORD'] = ''
# current_app.config['MYSQL_DATABASE_DB'] = 'evalf'
# current_app.config['apidb'] =  "http://127.0.0.1:5556"