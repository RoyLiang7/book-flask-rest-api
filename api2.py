import aiohttp

from src.services.user_service import TestUserService
from mysql.connector.aio import connect
from flask import Flask, request, jsonify

app = Flask(__name__)


# async def get_users():
#     async with await connect(host="103.3.173.137", database="testdb2" , user="looksee", password="return2626!") as cnx:
#         async with await cnx.cursor() as cur:
#             await cur.execute("SELECT id, name, email FROM users")
#             results = await cur.fetchall()
#             return results    
test_service = TestUserService()


@app.route('/test/1', methods=['GET'])
async def test_1():
    async with aiohttp.ClientSession() as session:
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print(pokemon['name'])
            return jsonify(pokemon), 200
        
@app.route('/test/2', methods=['GET'])
async def test_2():
    async with aiohttp.ClientSession() as session:
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print(pokemon['name'])
            return jsonify(pokemon), 200
        
@app.route('/test/3', methods=['GET'])
async def test_3():
    async with aiohttp.ClientSession() as session:
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print(pokemon['name'])
            return jsonify(pokemon), 200

@app.route('/db/1', methods=['GET'])
async def db_1():
    async with await connect(host="103.3.173.137", database="testdb2" , user="looksee", password="return2626!") as cnx:
        async with await cnx.cursor() as cur:
            # Execute a non-blocking query
            await cur.execute("select id, name, email from users")

            # Retrieve the results of the query asynchronously
            results = await cur.fetchall()
            return jsonify(results), 200

@app.route('/db/2', methods=['GET'])
async def db_2():
    users = await test_service.execute_query()
    return jsonify(users), 200



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
