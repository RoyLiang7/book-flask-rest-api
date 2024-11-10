from flask import Blueprint, jsonify, request

from src.services.book_category_service import BookCategoryService

cat_bp = Blueprint("cat_blueprint", __name__)
cat_srv = BookCategoryService()


@cat_bp.route("/", methods=["GET"])
def get_all():
    result = cat_srv.get_all()

    return jsonify(result), 200
