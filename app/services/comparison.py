from typing import Dict, Any
from app.utils.http import http_client
from app.core.database import db
from app.models.user import User

class ComparisonService:
    def get_total_comparison(self) -> Dict[str, Any]:
        """获取总人数对比"""
        try:
            # 获取API数据
            api_data = http_client.request(
                'GET',
                '/api/users/total'
            )
            
            # 获取数据库数据
            with db.session_scope() as session:
                db_count = session.query(User).count()
            
            # 计算匹配率
            total = max(api_data['total'], db_count)
            match_rate = min(api_data['total'], db_count) / total if total > 0 else 0
            
            return {
                'status': 'success',
                'data': {
                    'api_count': api_data['total'],
                    'db_count': db_count,
                    'match_rate': match_rate
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

comparison_service = ComparisonService() 