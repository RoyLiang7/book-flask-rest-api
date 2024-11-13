import datetime
from flask import Blueprint, jsonify, request

from src.services.book_trans_service import BookTransactionService


trans_bp = Blueprint('book_trans_blueprint', __name__)
trans_service = BookTransactionService()


@trans_bp.route( "/", methods=["GET"])
def get_all():
    result = trans_service.get_all()

    return jsonify(result)

@trans_bp.route("/late", methods=['GET'])
def get_late_all():
    result = trans_service.get_late_trans()

    return jsonify(result)

@trans_bp.route("/id/<int:id>", methods=["GET"])
def get_by_id(id):
    result = trans_service.get_by_id(id)

    return jsonify(result), 200


@trans_bp.route("/", methods=['PUT'])
def update():
    data = request.get_json()
    result = trans_service.update(data)

    return jsonify(result), 200

@trans_bp.route("/", methods=["POST"])
def create_transaction():
    data = request.get_json()
    result = trans_service.create(data)

    return jsonify(result), 200

@trans_bp.route("/id/<int:id>", methods=['DELETE'])
def cancel_trans():
    id = request.params.id
    result = trans_service.delete(id)

    return jsonify(result), 200
   
@trans_bp.route("/process", methods=['POST'])
def process_late_fees():
    result = trans_service.process_late_fees()

    return jsonify(result), 200
 

@trans_bp.route("/test", methods=["GET"])
def test_trans():
    result = trans_service.test_trans()

    return jsonify(result), 200
