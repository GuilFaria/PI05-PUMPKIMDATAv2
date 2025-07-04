import psycopg2

conn = psycopg2.connect(
    host="pi05-pumpkimintelligence.cloym2g4gjkx.us-east-2.rds.amazonaws.com",   # ex: meu-banco-teste.xxxxxxxxx.us-east-1.rds.amazonaws.com
    database="postgres",           # ou outro nome que você criou
    user="postgres",               # seu usuário
    password="eKXAmoaNi5vtMDnxhuew",          # sua senha
    port=5432
)

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())

cur.close()
conn.close()