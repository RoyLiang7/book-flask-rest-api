import os
from mysql.connector.aio import connect

class MyDatabaseConnection:
    _cnx = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MyDatabaseConnection, cls).__new__(cls)

        return cls._instance

    async def connect(self):
        if self._cnx is None:
            self._cnx = await connect(
                host     = os.environ["MYSQL_HOST"],
                database = os.environ["MYSQL_DB"],
                user     = os.environ["MYSQL_USER"],
                password = os.environ["MYSQL_PASSWORD"]
            )

        return self._cnx

    async def close(self):
        if self._cnx:
            await self.cnx.close()            
            self._cnx = None        # Reset the connection to None after closing
