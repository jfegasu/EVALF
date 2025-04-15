import pandas as pd
from utils.Utilitarios import *
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'EVALF.db')
print('DESCARGANDO RESPUESTAS')
sql="SELECT idFICHA,TITULACION,PREGUNTA,RESPUESTA FROM THEVAL"
datos=pd.DataFrame(ConsultarD(DATABASE,sql))
datos.to_csv("RESPUESTAS.csv",index=False)
print("PROCESO TERMINADO")