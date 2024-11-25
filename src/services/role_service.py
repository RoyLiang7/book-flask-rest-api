from src.services.base_service import BaseService
from mysql.connector.aio import connect

class TestService(BaseService):
    
    def __init__(self):
        super().__init__() 

    async def get_all(self):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("select id, descriptions from roles")
                results = await cur.fetchall()

                return results    

    async def get_by_id(self, id):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("select id, descriptions from roles where id = %s", (id,))
                results = await cur.fetchall()

                return results    
                
    async def create(self, model):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("insert into roles (descriptions) values (%s)", (model["descriptions"],))
                result = await cur.lastrowid

                return result
    
    async def update(self, model):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("update roles set descriptions = %s", (model["descriptions"],))
                result = await cur.rowcount

                return result    
    
    async def delete(self, id):
        async with await self.dbcnx.connect() as cnx:
            async with await cnx.cursor() as cur:
                await cur.execute("delete roles where id = %s", (id,))
                result = await cur.rowcount

                return result    
