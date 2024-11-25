from src.services.base_service import BaseService
from mysql.connector.aio import connect

class TestUserService(BaseService):
    
    def __init__(self):
        super().__init__()

    async def get_all(self):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("select id, name, email, password, status from users")
                results = await cur.fetchall()

                return results    

    async def get_by_id(self, id):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("select  id, name, email, password, status from users where id = %s", (id,))
                results = await cur.fetchall()

                return results    

    async def create(self, model):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("insert into users (name, email, password, status) values (%s, %s, %s, %s)", 
                                    (model["name"], model["email"], model["password"], model["status"]))
                results = await cur.fetchall()

                return results    

    async def update(self, model):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("update users set name = %, email = %, password = %, status = %s where id = %s", 
                                    (model["name"], model["email"], model["password"], model["status"], model["id"]))
                results = await cur.fetchall()

                return results    
                
    async def delete(self, id):
        pass


    async def execute_query(self):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("SELECT id, name, email FROM users")
                results = await cur.fetchall()

                return results    

