import datetime
from flask import Blueprint, jsonify, request

from src.services.book_category_service import BookCategoryService


cat_bp = Blueprint('book_category_bp', __name__)
cat_srv = BookCategoryService()


@cat_bp.route("/", methods=["GET"])
def get_all():
    result = cat_srv.get_all()
    # jsonstr1 = json.dumps(s1.__dict__) 
    
    return jsonify(result), 200

@cat_bp.route("/id/<int:id>", methods=["GET"])
def get_by_id(id):
    result = cat_srv.get_by_id(id)

    return jsonify(result), 200


@cat_bp.route("/", methods=["PUT"])
def update():
    data = request.get_json()
    result = cat_srv.update(data)

    return jsonify(result), 200

@cat_bp.route("/", methods=["POST"])
def insert():
    data = request.get_json()
    result = cat_srv.insert(data)

    return jsonify(result), 200

@cat_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    result = cat_srv.delete(id)

    return jsonify(result), 200
