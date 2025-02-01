from flask import jsonify, Blueprint
from app.utils.db_utils import DatabaseConnection
from app.services.organization.organization_service import OrganizationService

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/comparison/total')
def get_total_comparison():
    try:
        org_service = OrganizationService()
        result = org_service.get_total_comparison()
        return jsonify({'data': result, 'query_time': result.get('query_time', 0)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/comparison/rank')
def get_rank_comparison():
    try:
        org_service = OrganizationService()
        result = org_service.get_rank_comparison()
        return jsonify({'data': result, 'query_time': result.get('query_time', 0)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/db/data')
def get_db_data():
    try:
        org_service = OrganizationService()
        result = org_service.get_db_data()
        return jsonify(result)  # result 已经包含 data 和 query_time
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/api-data')
def get_api_data():
    try:
        org_service = OrganizationService()
        result = org_service.get_api_data()
        return jsonify({'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 