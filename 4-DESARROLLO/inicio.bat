@echo on
@echo INICIANDO BASE DE DATOS
cd .\database
start  python api.py
@echo INICIANDO SERVIDOR WEB
cd ..
start python app.py
@echo INICIANDO APLICATIVO
start 127.0.0.1:5000

pause