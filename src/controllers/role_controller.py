from src import basic_auth
from src.services.role_service import RoleService

from flask import Blueprint, jsonify, request

role_bp = Blueprint('role_blueprint', __name__)
role_srv = RoleService()


@role_bp.route("/", methods=["GET"])
@basic_auth.required
def get_all():
    result = role_srv.get_all()
    # jsonstr1 = json.dumps(s1.__dict__) 
    
    return jsonify(result), 200

@role_bp.route("/id/<int:id>", methods=["GET"])
def get_by_id(id):
    result = role_srv.get_by_id(id)

    return jsonify(result), 200


@role_bp.route("/", methods=["PUT"])
def update():
    data = request.get_json()
    result = role_srv.update(data)

    return jsonify(result), 200

@role_bp.route("/", methods=["POST"])
def insert():
    data = request.get_json()
    result = role_srv.insert(data)

    return jsonify(result), 200

@role_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    result = role_srv.delete(id)

    return jsonify(result), 200
