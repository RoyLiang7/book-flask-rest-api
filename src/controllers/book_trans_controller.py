import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from src.services.book_trans_service import BookTransactionService


trans_bp = Blueprint('book_trans_blueprint', __name__)
trans_service = BookTransactionService()


@trans_bp.route( "/", methods=["GET"])
def get_all():
    result = trans_service.get_all()

    return jsonify(result)

@trans_bp.route("/", methods=["POST"])
def create_transaction():
    data = request.get_json()
    result = trans_service.create(data)

    return jsonify(result), 200

