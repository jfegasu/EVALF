import pandas as pd
from utils.Utilitarios import *
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'EVALF.db')
print('DESCARGANDO RESPUESTAS')
sql="SELECT * FROM THEVAL"
datos=pd.DataFrame(Consultar(DATABASE,sql))
datos.to_excel("RESPUESTAS.xlsx")
print("PROCESO TERMINADO")