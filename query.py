import sqlite3

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

#Quantidade total de entregas:
cursor.execute("SELECT COUNT(*) AS total_entregas FROM dados_teste_pratico")
total_entregas = cursor.fetchone()[0]

#Quantidade de entregas. Em dia, Atrasadas, Não iniciadas:
cursor.execute("""
    SELECT
        SUM(CASE WHEN dataInicioEntrega IS NULL THEN 1 ELSE 0 END) AS Nao_Iniciadas,
        SUM(CASE WHEN dataInicioEntrega IS NOT NULL AND dataFimEntrega <= dataPrazo THEN 1 ELSE 0 END) AS Em_Dia,
        SUM(CASE WHEN dataInicioEntrega IS NOT NULL AND dataFimEntrega > dataPrazo THEN 1 ELSE 0 END) AS Atrasadas
    FROM dados_teste_pratico
""")
entregas_status = cursor.fetchone()

#Quantidade de projetos únicos:
cursor.execute("SELECT COUNT(DISTINCT projeto) AS quantidade_projetos FROM dados_teste_pratico")
quantidade_projetos = cursor.fetchone()[0]

#Razões de bloqueio:
cursor.execute("SELECT DISTINCT rezaoBloqueio FROM dados_teste_pratico WHERE rezaoBloqueio IS NOT NULL")
razões_bloqueio = cursor.fetchall()

#Tempo total bloqueado:
cursor.execute("SELECT SUM(tempoBloqueio) AS tempo_total_bloqueado FROM dados_teste_pratico")
tempo_total_bloqueado = cursor.fetchone()[0]

#Quantidade de entregas por natureza do item:
cursor.execute("SELECT naturezaItem, COUNT(*) AS total_entregas FROM dados_teste_pratico GROUP BY naturezaItem")
entregas_por_natureza = cursor.fetchall()


conn.close()

print("Resultados:")
print(f"Quantidade total de entregas: {total_entregas}")
print(f"Entregas: \n  - Não iniciadas: {entregas_status[0]}\n  - Em dia: {entregas_status[1]}\n  - Atrasadas: {entregas_status[2]}")
print(f"Quantidade de projetos: {quantidade_projetos}")
print("5Razões de bloqueio:")
for razão in razões_bloqueio:
    print(f"  - {razão[0]}")
print(f"Tempo total bloqueado: {tempo_total_bloqueado}")
print("Quantidade de entregas por natureza do item:")
for natureza in entregas_por_natureza:
    print(f"  - {natureza[0]}: {natureza[1]}")
