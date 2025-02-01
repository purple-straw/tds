"""
人员数据处理器
"""
from app.utils.log_control import INFO, ERROR


class PersonnelDataProcessor:
    @staticmethod
    def process_rank_data(data):
        """处理职级分布数据"""
        rank_count = {
            "P序列": {},
            "M序列": {},
            "B序列": {}
        }
        
        for person in data:
            level = person.get('level', '')
            if not level:
                continue
                
            if level.startswith('P'):
                series = "P序列"
            elif level.startswith('M'):
                series = "M序列"
            elif level.startswith('B'):
                series = "B序列"
            else:
                continue
                
            rank_count[series][level] = rank_count[series].get(level, 0) + 1
            
        return rank_count

    @staticmethod
    def calculate_average_age(data):
        """计算平均年龄"""
        total_age = 0
        valid_count = 0
        
        for person in data:
            try:
                age = int(person.get('age', 0))
                if age > 0:
                    total_age += age
                    valid_count += 1
            except (ValueError, TypeError):
                continue
        
        return round(total_age / valid_count, 1) if valid_count > 0 else 0

    @staticmethod
    def format_personnel_data(person, level=None, series=None):
        """格式化人员数据"""
        return {
            'id': person.get('id', ''),
            'name': person.get('name', '-'),
            'level': person.get('level', level),
            'gender': person.get('gender', '-'),
            'department': person.get('department', series),
            'position': person.get('position', level),
            'entry_date': person.get('entryDate', '-'),
            'status': person.get('status', '在职')
        }

    @staticmethod
    def calculate_match_rate(count1, count2):
        """计算匹配率"""
        if count1 == 0 and count2 == 0:
            return 100.0
        return round(min(count1, count2) / max(count1, count2) * 100, 2) if max(count1, count2) > 0 else 0 