import datetime
from flask import Blueprint, request, jsonify

from src.services.book_service import BookService



book_bp = Blueprint('book_blueprint', __name__)
book_srv = BookService()


@book_bp.route("/", methods=["GET"])
def get_all():
    result = book_srv.get_all()
    return jsonify(result), 200

@book_bp.route("/id/<int:id>", methods=["GET"])
def get_by_id(id):
    result = book_srv.get_by_id(id)

    return jsonify(result), 200


@book_bp.route("/", methods=["PUT"])
def update():
    data = request.get_json()
    result = book_srv.update(data)

    return jsonify(result), 200

@book_bp.route("/", methods=["POST"])
def insert():
    data = request.get_json()
    result = book_srv.insert(data)

    return jsonify(result), 200

@book_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    result = book_srv.delete(id)

    return jsonify(result), 200

