import datetime

from src import app, basic_auth
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from src.services.user_service import UserService


user_bp = Blueprint('user_blueprint', __name__)
user_srv = UserService()


@user_bp.route("/authenticate", methods=["POST"])
@basic_auth.auth_required
def authenticate():
    data = request.get_json()

    result = user_srv.authenticate(data)
    if(result):
        access_token = create_access_token(identity=result, expires_delta=datetime.timedelta(minutes=10))
        return jsonify({'status': 1, 'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'status': 0, 'message': 'Invalid authentication'}), 401


@user_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    result = user_srv.get_all()

    return jsonify(result), 200

@user_bp.route("/id/<int:id>", methods=["GET"])
def get_by_id(id):
    result = user_srv.get_by_id(id)

    return jsonify(result), 200

@user_bp.route("/email/<string:email>", methods=["GET"])
def get_by_email(email):
    result = user_srv.get_by_email(email)

    return jsonify(result), 200

@user_bp.route("/related", methods=["GET"])
def get_related():
    result = user_srv.get_related()

    return jsonify(result), 200

@user_bp.route("/sproc", methods=["GET"])
def get_sproc():
    result = user_srv.get_sproc()

    return jsonify(result), 200




@user_bp.route("/", methods=["PUT"])
def update():
    data = request.get_json()

    result = user_srv.update(data)

    return jsonify(result), 200

@user_bp.route("/", methods=["POST"])
def insert():
    data = request.get_json()
    
    result = user_srv.create(data)

    return jsonify(result), 200

@user_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    result = user_srv.delete(id)

    return jsonify(result), 200
