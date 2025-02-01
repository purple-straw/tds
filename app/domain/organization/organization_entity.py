"""
组织领域实体
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class Personnel:
    """人员实体"""
    id: str
    name: str
    level: str
    gender: str
    department: str
    position: str
    entry_date: datetime
    status: str
    age: Optional[int] = None
    
    @property
    def series(self) -> str:
        """获取职级序列"""
        return self.level[0] if self.level else ''

    @classmethod
    def from_api_data(cls, data: dict, level: str = None, series: str = None):
        return cls(
            id=data.get('id', ''),
            name=data.get('name', '-'),
            level=data.get('level', level),
            gender=data.get('gender', '-'),
            department=data.get('department', series),
            position=data.get('position', level),
            entry_date=data.get('entryDate', '-'),
            status=data.get('status', '在职'),
            age=int(data.get('age', 0))
        )

    @classmethod
    def from_db_data(cls, data: dict, level: str = None, series: str = None):
        return cls(
            id=data.get('id', ''),
            name=data.get('name', '-'),
            level=data.get('level', level),
            gender=data.get('gender', '-'),
            department=data.get('per_code', series),
            position=data.get('manage_name', level),
            entry_date=data.get('entry_date', '-'),
            status=data.get('status', '在职')
        )


@dataclass
class RankDistribution:
    """职级分布实体"""
    p_series: int = 0
    m_series: int = 0
    b_series: int = 0
    
    def add_personnel(self, personnel: Personnel) -> None:
        """添加人员统计"""
        series = personnel.series
        if series == 'P':
            self.p_series += 1
        elif series == 'M':
            self.m_series += 1
        elif series == 'B':
            self.b_series += 1

    @classmethod
    def from_api_data(cls, data: List[Personnel]):
        rank_count = {
            "P序列": {},
            "M序列": {},
            "B序列": {}
        }
        
        for person in data:
            level = person.level
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
            
        return cls(
            p_series=rank_count["P序列"],
            m_series=rank_count["M序列"],
            b_series=rank_count["B序列"]
        )

    @classmethod
    def from_db_data(cls, data: List[dict]):
        rank_count = {
            "P序列": {},
            "M序列": {},
            "B序列": {}
        }
        
        for record in data:
            level = record.get('level', '')
            count = record.get('count', 0)
            
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
                
            rank_count[series][level] = count
            
        return cls(
            p_series=rank_count["P序列"],
            m_series=rank_count["M序列"],
            b_series=rank_count["B序列"]
        )


class OrganizationMetrics:
    """组织指标计算"""
    
    @staticmethod
    def calculate_match_rate(count1: int, count2: int) -> float:
        """计算匹配率"""
        if count1 == 0 and count2 == 0:
            return 100.0
        elif count1 == 0 or count2 == 0:
            return 0.0
        
        min_count = min(count1, count2)
        max_count = max(count1, count2)
        return round((min_count / max_count) * 100, 2)

    @classmethod
    def calculate_average_age(cls, data: List[Personnel]) -> float:
        total_age = 0
        valid_count = 0
        
        for person in data:
            if person.age and person.age > 0:
                total_age += person.age
                valid_count += 1
        
        return round(total_age / valid_count, 1) if valid_count > 0 else 0 