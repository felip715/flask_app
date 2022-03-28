from multiprocessing import connection
import psycopg2

def conect_bbdd():
    try:
        connection=psycopg2.connect(
            host='206.189.202.152',
            user='emprinet',
            password='emprinet',
            database='test'
        )
        print("Conecttion Successful")
        return connection
    except Exception as ex:
        print(ex)
