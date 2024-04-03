import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='flamberge',
    user='flamberge',
    port=5601,
    password='root')

schema = "flamberge_v2"

clusters_path = "clusters.csv"
vecteurs_path = "vecteurs.json"