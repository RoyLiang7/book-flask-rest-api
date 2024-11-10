import datetime
from flask import Blueprint, jsonify, request

from src.services.book_type_service import BookTypeService

type_bp = Blueprint('book_type_blueprint', __name__)
type_srv = BookTypeService()


@type_bp.route("/", methods=["GET"])
def get_all():
    result = type_srv.get_all()
    # jsonstr1 = json.dumps(s1.__dict__) 
    
    return jsonify(result), 200

@type_bp.route("/id/<int:id>", methods=["GET"])
def get_by_id(id):
    result = type_srv.get_by_id(id)

    return jsonify(result), 200


@type_bp.route("/", methods=["PUT"])
def update():
    data = request.get_json()
    result = type_srv.update(data)

    return jsonify(result), 200

@type_bp.route("/", methods=["POST"])
def insert():
    data = request.get_json()
    result = type_srv.insert(data)

    return jsonify(result), 200

@type_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    result = type_srv.delete(id)

    return jsonify(result), 200
