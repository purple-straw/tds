@api_bp.route('/data/differences', methods=['GET'])
def get_data_differences():
    """获取数据差异详情"""
    try:
        org_service = OrganizationService()
        result = org_service.get_data_differences()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}) 