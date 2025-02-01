from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from app.services.organization.organization_service import OrganizationService
from app.config.config import DevelopmentConfig
from app.utils.db_utils import DatabaseConnection
from app.utils.log_control import ERROR
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

# 设置调试模式
app.config.from_object(DevelopmentConfig)

# 创建一个全局的 service 实例
organization_service = OrganizationService()


@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')


@app.route('/api/comparison/total')
def get_total_comparison():
    """获取总人数对比数据"""
    try:
        result = organization_service.get_total_comparison()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取总人数对比数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/comparison/rank')
def get_rank_comparison():
    """获取职级分布对比数据"""
    try:
        result = organization_service.get_rank_comparison()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取职级分布对比数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/db/data')
def get_db_data():
    """获取数据库表数据"""
    try:
        service = OrganizationService()
        result = service.get_db_data()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取数据库表数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/api-data')
def get_api_data():
    """获取API数据"""
    try:
        service = OrganizationService()
        result = service.get_api_data()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取API数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/comparison/age')
def get_age_comparison():
    """获取平均年龄对比数据"""
    try:
        result = organization_service.get_average_age_comparison()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取平均年龄对比数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/db/update', methods=['POST'])
def update_db_data():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        print("Received update data:", data)
        
        if not all(k in data for k in ('id', 'field', 'value')):
            return jsonify({"error": "Missing required fields"}), 400
            
        row_id = data.get('id')
        field = data.get('field')
        value = data.get('value')
        
        # 字段名映射
        field_mapping = {
            'department': 'per_code',
            'position': 'manage_name',
            'entry_date': 'join_work_date'  # 添加入职日期字段映射
        }
        
        # 如果字段需要映射，进行转换
        db_field = field_mapping.get(field, field)
        
        # 验证字段名
        allowed_fields = {'name', 'level', 'gender', 'per_code', 'manage_name', 'join_work_date', 'status'}
        if db_field not in allowed_fields:
            return jsonify({"error": f"Invalid field name '{field}'. Allowed fields are: {', '.join(allowed_fields)}"}), 400
        
        # 构建更新SQL
        sql = f"UPDATE per_main SET {db_field} = :value WHERE id = :id"
        params = {'value': value, 'id': row_id}
        
        # 执行更新
        with DatabaseConnection() as db:
            db.execute(sql, params)
            return jsonify({"success": True})
            
    except Exception as e:
        ERROR.logger.error(f"更新数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/db/add', methods=['POST'])
def add_db_data():
    try:
        data = request.get_json()
        print("Received data for insert:", data)  # 添加日志
        
        # 字段映射
        field_mapping = {
            'department': 'per_code',
            'position': 'manage_name',
            'entry_date': 'join_work_date'
        }
        
        # 处理字段映射
        mapped_data = {}
        for key, value in data.items():
            # 跳过 ID 字段，让数据库自动处理
            if key.lower() != 'id':
                mapped_key = field_mapping.get(key, key)
                mapped_data[mapped_key] = value
        
        # 添加必要的默认字段
        mapped_data['del_flag'] = 0  # 0表示未删除
        
        # 构建插入SQL，使用命名参数
        fields = ', '.join(mapped_data.keys())
        placeholders = ', '.join([f':{key}' for key in mapped_data.keys()])
        sql = f"INSERT INTO per_main ({fields}) VALUES ({placeholders})"
        
        print("SQL:", sql)  # 添加日志
        print("Parameters:", mapped_data)  # 添加日志
        
        # 执行插入，使用映射后的数据
        with DatabaseConnection() as db:
            db.execute(sql, mapped_data)
            return jsonify({"success": True})
            
    except Exception as e:
        ERROR.logger.error(f"添加数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/db/delete', methods=['POST'])
def delete_db_data():
    try:
        data = request.get_json()
        row_id = data.get('id')
        
        # 执行删除，使用命名参数
        with DatabaseConnection() as db:
            sql = text("DELETE FROM per_main WHERE id = :id")
            db.execute(sql, {'id': row_id})
            return jsonify({"success": True})
            
    except Exception as e:
        ERROR.logger.error(f"删除数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/personnel/api')
def get_api_personnel():
    """获取API人员数据"""
    try:
        series = request.args.get('series')
        level = request.args.get('level')
        
        if not series or not level:
            return jsonify({"error": "Missing required parameters"}), 400
            
        service = OrganizationService()
        result = service.get_api_personnel_by_level(series, level)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取API人员数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/personnel/db')
def get_db_personnel():
    """获取数据库人员数据"""
    try:
        series = request.args.get('series')
        level = request.args.get('level')
        
        if not series or not level:
            return jsonify({"error": "Missing required parameters"}), 400
            
        service = OrganizationService()
        result = service.get_db_personnel_by_level(series, level)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"获取数据库人员数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
