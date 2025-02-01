from flask import Blueprint, jsonify
from app.services.comparison import comparison_service

bp = Blueprint('comparison', __name__, url_prefix='/api/comparison')

@bp.route('/total', methods=['GET'])
def get_total_comparison():
    result = comparison_service.get_total_comparison()
    return jsonify(result) 