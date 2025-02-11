import datetime

from flask import Blueprint, jsonify, request
from src.services.user_service import UserService


user_bp = Blueprint('user_blueprint', __name__)
user_srv = UserService()


@user_bp.route("/", methods=["GET"])
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
