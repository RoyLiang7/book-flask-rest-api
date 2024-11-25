
# from flask import Blueprint, jsonify, request
# from src.services.user_service_async import UserServiceAsync


# user_async_bp = Blueprint('user_async_blueprint', __name__)
# user_async_service = UserServiceAsync()

# @user_async_bp.route('/', methods=['GET'])
# async def get_all_users():
#     users = await user_async_service.get_all()

#     return jsonify(users)

# @user_async_bp.route('/id/<int:user_id>', methods=['GET'])
# async def get_user(user_id):
#     user = await user_async_service.get_by_id(user_id)
#     if user:
#         return jsonify(user)

#     return jsonify({"error": "User not found"}), 404
