from flask import Blueprint, jsonify, request
from app.services.modal import modal_service

bp = Blueprint('modal', __name__, url_prefix='/api/modal')

@bp.route('/detail', methods=['POST'])
def get_detail_modal():
    """获取详情模态窗模板"""
    try:
        data = request.get_json()
        modal_config = modal_service.create_detail_modal(data)
        return jsonify({
            'status': 'success',
            'data': modal_config
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 