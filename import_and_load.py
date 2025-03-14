import pandas as pd
import sqlite3
import requests
from io import StringIO


URL_CSV = "https://docs.google.com/spreadsheets/d/1q1Iem5d06U2CJZmwhRFm_MSE/export?format=csv&gid=1177547531"


response = requests.get(URL_CSV)
if response.status_code != 200:
    raise Exception("Erro ao baixar a planilha!")


csv_data = StringIO(response.text)
df = pd.read_csv(csv_data)

columns = ['item_id', 'item_name', 'Natureza do Item', 'target_date', 'board', 'deadline', 'Data_inicio_entrega', 'Data_Fim_Entrega', 'block_time', 'block_reason']
df = df[columns]

conn = sqlite3.connect("dados.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS dados_teste_pratico (
    idItem INTEGER,
    nameItem TEXT,
    naturezaItem TEXT,
    dataAlvo DATE,
    projeto TEXT,
    dataPrazo DATE,
    dataInicioEntrega DATE,
    dataFimEntrega DATE,
    tempoBloqueio INTEGER,
    rezaoBloqueio TEXT           
)
""")

for _, row in df.iterrows():
    cursor.execute(f"""INSERT INTO dados_teste_pratico ({', '.join(df.columns)}) 
                   VALUES ({', '.join(['?'] * len(df.columns))})""", tuple(row))


conn.commit()
cursor.close()
conn.close()
print("✅ Dados importados com sucesso para SQLite!")
