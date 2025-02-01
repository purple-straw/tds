"""
组织应用服务
"""
from typing import Dict, List, Optional
from app.domain.organization.organization_entity import Personnel, RankDistribution, OrganizationMetrics
from app.domain.organization.organization_repository import OrganizationRepository
from app.utils.log_control import INFO, ERROR


class OrganizationApplicationService:
    def __init__(self, api_repo: OrganizationRepository, db_repo: OrganizationRepository):
        self.api_repo = api_repo
        self.db_repo = db_repo

    def get_total_comparison(self) -> Dict:
        """获取总人数对比数据"""
        try:
            # 获取API数据
            api_count = self.api_repo.get_total_count()
            
            # 获取数据库数据
            db_count = self.db_repo.get_total_count()
            
            return {
                'api_count': api_count,
                'db_count': db_count,
                'match_rate': OrganizationMetrics.calculate_match_rate(api_count, db_count)
            }
        except Exception as e:
            ERROR.logger.error(f"获取总人数对比数据失败: {str(e)}")
            raise

    def get_rank_comparison(self) -> Dict:
        """获取职级分布对比数据"""
        try:
            # 获取API数据
            api_rank_count = self.api_repo.get_rank_distribution()
            
            # 获取数据库数据
            db_rank_count = self.db_repo.get_rank_distribution()
            
            return {
                'api_data': {
                    "P序列": api_rank_count.p_series,
                    "M序列": api_rank_count.m_series,
                    "B序列": api_rank_count.b_series
                },
                'db_data': {
                    "P序列": db_rank_count.p_series,
                    "M序列": db_rank_count.m_series,
                    "B序列": db_rank_count.b_series
                }
            }
        except Exception as e:
            ERROR.logger.error(f"获取职级分布对比数据失败: {str(e)}")
            raise

    def get_average_age_comparison(self) -> Dict:
        """获取平均年龄对比数据"""
        try:
            # 获取API数据
            api_avg_age = self.api_repo.get_average_age()
            
            # 获取数据库数据
            db_avg_age = self.db_repo.get_average_age()
            
            return {
                'api_age': api_avg_age,
                'db_age': db_avg_age
            }
        except Exception as e:
            ERROR.logger.error(f"获取平均年龄对比数据失败: {str(e)}")
            raise

    def get_personnel_by_level(self, series: str, level: str) -> Dict:
        """获取指定职级的人员数据对比"""
        try:
            # 获取API数据
            api_personnel = self.api_repo.get_personnel_list(series, level)
            api_data = [
                {
                    'id': p.id,
                    'name': p.name,
                    'level': p.level,
                    'gender': p.gender,
                    'department': p.department,
                    'position': p.position,
                    'entry_date': p.entry_date,
                    'status': p.status
                }
                for p in api_personnel
            ]
            
            # 获取数据库数据
            db_personnel = self.db_repo.get_personnel_list(series, level)
            db_data = [
                {
                    'id': p.id,
                    'name': p.name,
                    'level': p.level,
                    'gender': p.gender,
                    'department': p.department,
                    'position': p.position,
                    'entry_date': p.entry_date,
                    'status': p.status
                }
                for p in db_personnel
            ]
            
            return {
                'api_data': api_data,
                'db_data': db_data
            }
        except Exception as e:
            ERROR.logger.error(f"获取人员数据失败: {str(e)}")
            raise 