from flask import Flask
from peewee import MySQLDatabase  

MYSQL= MySQLDatabase(
    'evalf',
    user='root',
    password='',
    host='localhost',
    port=3306
)
    

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'evalf'