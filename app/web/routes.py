from flask import jsonify, Blueprint, current_app
from app.services.organization.organization_service import OrganizationService

# 创建蓝图
api = Blueprint('api', __name__)
organization_service = OrganizationService()


@api.route('/comparison/total', methods=['GET'])
def get_total_comparison():
    """获取总人数对比数据"""
    try:
        result = organization_service.compare_total_people()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/comparison/rank', methods=['GET'])
def get_rank_comparison():
    """获取职级分布对比数据"""
    try:
        result = organization_service.compare_rank_distribution()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/db/data', methods=['GET'])
def get_db_data():
    """获取数据库数据"""
    try:
        result = organization_service.get_db_table_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/api-data', methods=['GET'])
def get_api_data():
    """获取API数据"""
    try:
        result = organization_service.get_api_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
