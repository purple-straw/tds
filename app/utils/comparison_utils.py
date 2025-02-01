"""
数据对比工具模块
"""
from typing import Dict, Any


class DataComparison:
    @staticmethod
    def compare_values(api_value: Any, db_value: Any, tolerance: float = 0.01) -> bool:
        """
        比较两个值是否相等
        
        Args:
            api_value: API返回的值
            db_value: 数据库查询的值
            tolerance: 浮点数比较的容差
            
        Returns:
            bool: 比较结果
        """
        if isinstance(api_value, (int, float)) and isinstance(db_value, (int, float)):
            return abs(float(api_value) - float(db_value)) <= tolerance
        return str(api_value) == str(db_value)

    @staticmethod
    def compare_data(api_data: Dict, db_data: Dict) -> Dict:
        """
        比较API数据和数据库数据
        
        Args:
            api_data: API返回的数据
            db_data: 数据库查询的数据
            
        Returns:
            Dict: 比较结果，包含差异信息
        """
        differences = {}
        
        # 获取所有序列
        all_series = set(api_data.keys()) | set(db_data.keys())
        
        for series in all_series:
            # 获取两边的数据，如果不存在则用空字典代替
            api_series = api_data.get(series, {})
            db_series = db_data.get(series, {})
            
            # 获取该序列下所有职级
            all_levels = set(api_series.keys()) | set(db_series.keys())
            
            # 比较每个职级的数据
            series_diff = {}
            for level in all_levels:
                api_count = api_series.get(level, 0)
                db_count = db_series.get(level, 0)
                
                if api_count != db_count:
                    series_diff[level] = {
                        'api_value': api_count,
                        'db_value': db_count
                    }
            
            # 只有当存在差异时才添加到结果中
            if series_diff:
                differences[series] = series_diff
                
        return differences

