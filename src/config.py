from distutils.command.config import config
from distutils.debug import DEBUG
from multiprocessing import connection
import psycopg2


class DevelopmentConfig():
    DEBUG=True

config={
    'development':DevelopmentConfig
}

try:
    connection=psycopg2.connect(
        host='206.189.202.152',
        user='emprinet',
        password='emprinet',
        database='test'
    )
    print("Conexión exitosa")
except Exception as ex:
    print(ex)
