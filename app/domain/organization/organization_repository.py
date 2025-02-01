"""
组织领域仓储接口
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .organization_entity import Personnel, RankDistribution, OrganizationMetrics
from app.infrastructure.database import DatabaseConnection
from app.infrastructure.api_client import APIClient
from app.config.sql_config import (
    TOTAL_NUMBER_OF_PEOPLE,
    RANK_OF_RANK,
    PERSONNEL_MAIN_TABLE_SQL,
    AVERAGE_AGE_SQL
)


class OrganizationRepository(ABC):
    """组织仓储接口"""
    
    @abstractmethod
    def get_personnel_list(self, series: str, level: str) -> List[Personnel]:
        """获取人员列表"""
        pass
    
    @abstractmethod
    def get_rank_distribution(self) -> RankDistribution:
        """获取职级分布"""
        pass
    
    @abstractmethod
    def get_total_count(self) -> int:
        """获取总人数"""
        pass
    
    @abstractmethod
    def get_average_age(self) -> float:
        """获取平均年龄"""
        pass


class APIOrganizationRepository(OrganizationRepository):
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_personnel_list(self, series: str, level: str) -> List[Personnel]:
        params = {
            'pageSize': 1000,
            'pageNum': 1,
            'suitRange': 1
        }
        if series:
            params['series'] = series.replace('序列', '')
        if level:
            params['level'] = level

        data = self.api_client.get_personnel_list(params)
        return [Personnel.from_api_data(item, level, series) for item in data]

    def get_rank_distribution(self) -> RankDistribution:
        personnel_list = self.get_personnel_list(series='序列', level='')
        return RankDistribution.from_api_data(personnel_list)

    def get_total_count(self) -> int:
        return len(self.get_personnel_list(series='序列', level=''))

    def get_average_age(self) -> float:
        personnel_list = self.get_personnel_list(series='序列', level='')
        return OrganizationMetrics.calculate_average_age(personnel_list)


class DBOrganizationRepository(OrganizationRepository):
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def get_personnel_list(self, series: str, level: str) -> List[Personnel]:
        sql = """
            SELECT 
                id,
                name,
                level,
                CASE gender 
                    WHEN '1' THEN '男'
                    WHEN '2' THEN '女'
                    ELSE '-'
                END as gender,
                per_code as department,
                manage_name as position,
                DATE_FORMAT(join_work_date, '%Y-%m-%d') as entry_date,
                status
            FROM per_main
            WHERE del_flag = 0
        """
        params = {}
        
        if level:
            sql += " AND level = :level"
            params['level'] = level

        result = self.db.execute_query(sql, params)
        return [Personnel.from_db_data(item, level, series) for item in result]

    def get_rank_distribution(self) -> RankDistribution:
        result = self.db.execute_query(RANK_OF_RANK)
        return RankDistribution.from_db_data(result)

    def get_total_count(self) -> int:
        result = self.db.execute_query(TOTAL_NUMBER_OF_PEOPLE)
        return int(result[0]['count(*)']) if result else 0

    def get_average_age(self) -> float:
        result = self.db.execute_query(AVERAGE_AGE_SQL)
        return round(float(result[0].get('avg_age', 0)), 1) if result else 0 