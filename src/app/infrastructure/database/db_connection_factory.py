import os
from mysql.connector import pooling


##SE VA A USAR FACTORY PARA GESTIONAR DE MANERA EFICIENTE LAS CONEXIONES
##FACTORY PROVEERA UNA UNICA INSTANCIA DE CONEXION AQUI SE USAURA SINGLETON conection_pull


class DatabaseConectionFactory:

    ##variable como instancia unica SINGLETON
    _connection_pool = None

    @classmethod
    def initialize(cls, minconn: int = 1, maxconn: int = 5):
        if cls._connection_pool is None:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=maxconn,
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "1234"),
                host=os.getenv("MYSQL_HOST", "localhost"),
                port=int(os.getenv("MYSQL_PORT", "3306")),
                database=os.getenv("MYSQL_DATABASE", "andina_trading"),
            )

    ##responsabilidad del programador liberar la conexion despues de ser usada para su reutiliacion
    @classmethod
    def get_connection(cls):
      if cls._connection_pool is None:
        raise Exception("Pool connection not initialized")
      return cls._connection_pool.get_connection()

    ##metodo para liberar el pool de conection
    @classmethod
    def release_connection(cls , connection):
        connection.close()

    ## Este metodo se levanta cuando se hace un reinicio de la app de FastApi
    @classmethod
    def close_pool(cls):
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            cls._connection_pool = None



