import asyncio
from flask import Flask, jsonify
from src.services.user_service_async import UserServiceAsync

app = Flask(__name__)
user_async_service = UserServiceAsync()

@app.route('/users', methods=['GET'])
async def get_all_users():
    loop = asyncio.get_event_loop()
    # users = await user_async_service.get_all()
    users = loop.run_until_complete(user_async_service.get_all())
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
async def get_user(user_id):
    user = await user_async_service.get_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid double calls in debug mode