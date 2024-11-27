import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.services.user_service import UserService


user_bp = Blueprint('user_blueprint', __name__)
user_srv = UserService()


@user_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    result = user_srv.get_all()

    return jsonify(result), 200

@user_bp.route("/id/<int:id>", methods=["GET"])
@jwt_required()
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


from src import basic_auth

@user_bp.route("/token", methods=["POST"])
@basic_auth.required
def get_token():
    data = request.get_json()
    result = user_srv.get_token(data)

    print(result)

    return jsonify(result), 200

@user_bp.route("/hash/<string:pwd>", methods=["GET"])
def get_hash(pwd):
    result = user_srv.get_hash(pwd)

    return jsonify(result), 200
