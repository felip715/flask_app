from multiprocessing import connection
import psycopg2

try:
    connection=psycopg2.connect(
        host='206.189.202.152',
        user='admin',
        password='emprinet',
        database='test'
    )

    print("Conexión exitosa")
except Exception as ex:
    print(ex)