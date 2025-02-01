"""
组织相关的业务逻辑
"""
from app.base.base_request import BaseRequest
from app.config.api_config import (
    API_ORGANIZATION_INFO, 
    ORGANIZATION_INFO_DATA, 
    NEW_API_ENDPOINT, 
    NEW_API_REQUEST_DATA
)
from app.config.data_mapping import CODE_TO_NAME, EFFICIENCY_NAME_MAPPING
from app.utils.log_control import INFO, ERROR
from .data_processor import OrganizationDataProcessor
from app.utils.db_utils import DatabaseConnection
from app.utils.comparison_utils import DataComparison
from app.config.sql_config import TOTAL_NUMBER_OF_PEOPLE, RANK_OF_RANK, PERSONNEL_MAIN_TABLE_SQL, AVERAGE_AGE_SQL
import requests
import json
import time
from datetime import datetime


class OrganizationService(BaseRequest):
    def __init__(self):
        super().__init__()
        self.data_processor = OrganizationDataProcessor()
        self._cache = None
        self._cache_time = None
        # 恢复数据库相关初始化
        self.db = DatabaseConnection()
        self.comparison = DataComparison()
        self.BASE_URL = 'https://test-tds-standard.cepin.com'

    def get_organization_info(self, use_cache=True):
        """获取组织画像信息，支持缓存"""
        if use_cache and self._cache:
            return self._cache

        try:
            if not self.token:
                INFO.logger.info("Token不存在，重新登录")
                self._login()

            INFO.logger.info("正在请求组织画像信息")
            response = requests.post(
                API_ORGANIZATION_INFO,
                json=ORGANIZATION_INFO_DATA,
                headers=self.headers,
                verify=False
            )

            result = response.json()
            print(result)
            if result.get('code') == 0:
                INFO.logger.info("获取组织画像信息成功")
                self._cache = self._process_response(result.get('response', {}))
                return self._cache
            else:
                ERROR.logger.error(f"获取组织画像信息失败: {result.get('message')}")
                return None

        except Exception as e:
            ERROR.logger.error(f"请求失败: {str(e)}")
            raise

    def _process_tag_group(self, tag_group, processed_data):
        """处理标签组数据"""
        group_name = tag_group.get('name')
        group_code = tag_group.get('code')

        if group_name == '组织概览':
            for tag in tag_group.get('tags', []):
                if tag['code'] in CODE_TO_NAME:
                    processed_data[CODE_TO_NAME[tag['code']]] = tag['value']

        elif group_code == 'RXFX':
            for tag in tag_group.get('tags', []):
                if tag['name'] in EFFICIENCY_NAME_MAPPING:
                    processed_data[EFFICIENCY_NAME_MAPPING[tag['name']]] = tag['value']

        elif group_code == 'zzhx_rcfx_yjfx':
            for tag in tag_group.get('tags', []):
                if tag['name'] == '团队业绩':
                    processed_data.update(self.data_processor.process_tag_value(tag['value']))
                elif tag['name'] == '客群分析':
                    processed_data.update(self.data_processor.process_tag_value(tag['value']))

        elif group_code == 'HXMB_ZZHX_RCFX_JGFX':
            self._process_structure_analysis(tag_group.get('tags', []), processed_data)

    def _process_structure_analysis(self, tags, processed_data):
        """处理结构分析数据"""
        for tag in tags:
            if tag['name'] == '职级统计':
                processed_data['职级分布'] = self.data_processor.process_position_levels(tag['value'])
            elif tag['name'] in ['年龄分析', '全日制最高学历统计', '工作稳定性', '人员类型汇总']:
                key_mapping = {
                    '年龄分析': '年龄分布',
                    '全日制最高学历统计': '学历分布',
                    '工作稳定性': '工作稳定性',
                    '人员类型汇总': '人员类型'
                }
                processed_data[key_mapping[tag['name']]] = self.data_processor.process_distribution_data(tag['value'])

    def _process_response(self, response_data):
        """处理响应数据"""
        processed_data = {}
        if response_data.get('tagList'):
            for tag_group in response_data['tagList']:
                self._process_tag_group(tag_group, processed_data)
        return processed_data

    def get_overview_info(self):
        """获取组织概览信息"""
        data = self.get_organization_info()
        if data:
            return {
                "总人数": data.get("总人数"),
                "正式工总人数": data.get("正式工总人数"),
                "男女比例": data.get("男女比例"),
                "平均年龄": data.get("平均年龄"),
                "平均司龄": data.get("平均司龄"),
                "管理岗人数": data.get("管理岗人数"),
                "平均汇报深度": data.get("平均汇报深度"),
                "平均管理幅度": data.get("平均管理幅度"),
                "试用期人数": data.get("试用期人数"),
                "党员比例": data.get("党员比例"),
                "校招生比例": data.get("校招生比例"),
                "近一年新员工比例": data.get("近一年新员工比例"),
                "近一年离职率": data.get("近一年离职率"),
                "官兵比": data.get("官兵比")
            }
        return None

    def get_efficiency_analysis(self):
        """获取人效分析数据"""
        data = self.get_organization_info()
        if data:
            return {
                "人均利润": data.get("人均利润"),
                "人均毛利": data.get("人均毛利"),
                "人均收入": data.get("人均收入")
            }
        return None

    def get_team_performance(self):
        """获取团队业绩数据"""
        data = self.get_organization_info()
        if data:
            return {
                "日均余额": data.get("日均余额"),
                "营业净收入": data.get("营业净收入"),
                "人效": data.get("人效"),
                "存款增量": data.get("存款增量"),
                "贷款增量": data.get("贷款增量"),
                "贷款规模": data.get("贷款规模")
            }
        return None

    def get_customer_analysis(self):
        """获取客群分析数据"""
        data = self.get_organization_info()
        if data:
            return {
                "总客群数": data.get("总客群数"),
                "高价值客群数": data.get("高价值客群数"),
                "大中客群数": data.get("大中客群数"),
                "基础客群数": data.get("基础客群数"),
                "长尾客群数": data.get("长尾客群数")
            }
        return None

    def get_age_distribution(self):
        """获取年龄分布数据"""
        data = self.get_organization_info()
        if data:
            return data.get("年龄分布")
        return None

    def get_education_distribution(self):
        """获取学历分布数据"""
        data = self.get_organization_info()
        if data:
            return data.get("学历分布")
        return None

    def get_position_level_distribution(self):
        """获取职级分布数据"""
        try:
            data = self.get_organization_info()
            INFO.logger.info(f"职级分布原始数据: {data}")
            
            if not data:
                return {}
            
            # 获取职级分布数据
            level_data = data.get('职级分布', {})
            INFO.logger.info(f"获取到的职级分布数据: {level_data}")
            
            # 如果是字符串，尝试解析为字典
            if isinstance(level_data, str):
                try:
                    level_data = json.loads(level_data)
                except json.JSONDecodeError:
                    ERROR.logger.error("职级分布数据不是有效的JSON字符串")
                    return {}
            
            # 如果不是字典类型，返回空字典
            if not isinstance(level_data, dict):
                ERROR.logger.error(f"职级分布数据类型错误: {type(level_data)}")
                return {}
            
            return level_data
        except Exception as e:
            ERROR.logger.error(f"获取职级分布数据失败: {str(e)}")
            return {}

    def get_work_stability_distribution(self):
        """获取工作稳定性分布数据"""
        data = self.get_organization_info()
        if data:
            return data.get("工作稳定性")
        return None

    def get_employee_type_distribution(self):
        """获取人员类型汇总数据"""
        data = self.get_organization_info()
        if data:
            return data.get("人员类型")
        return None

    def get_new_data(self):
        """
        获取新的数据
        
        Returns:
            dict: 处理后的数据
            None: 获取失败时返回None
        """
        try:
            response = self.make_request(NEW_API_ENDPOINT, NEW_API_REQUEST_DATA)
            if response and response.get('code') == 0:
                # 获取响应数据
                data = response.get('response', {})
                # 处理数据
                processed_data = self._process_response(data)
                return processed_data
            else:
                ERROR.logger.error("获取新数据失败: 接口返回错误")
                return None
        except Exception as e:
            ERROR.logger.error(f"获取新数据失败: {str(e)}")
            return None

    def compare_organization_data(self):
        """
        对比组织数据 (暂时只返回API数据)
        
        Returns:
            Dict: API数据结果
        """
        api_data = self.get_organization_info()
        if not api_data:
            return {"error": "Failed to get API data"}

        # 暂时只返回API数据的结构化信息
        return {
            'organization_overview': self.get_overview_info(),
            'efficiency_analysis': self.get_efficiency_analysis(),
            'team_performance': self.get_team_performance(),
            'customer_analysis': self.get_customer_analysis(),
            'age_distribution': self.get_age_distribution(),
            'education_distribution': self.get_education_distribution(),
            'position_level': self.get_position_level_distribution(),
            'work_stability': self.get_work_stability_distribution(),
            'employee_type': self.get_employee_type_distribution()
        }

    def get_db_data(self):
        """获取数据库人员信息"""
        try:
            INFO.logger.info("开始查询数据库人员信息")
            result = self.db.execute_query(PERSONNEL_MAIN_TABLE_SQL)
            # INFO.logger.info(f"查询结果: {result}")
            
            if not result.get('data'):
                print(result)
                return {
                    'data': [],
                    'query_time': result.get('query_time', 0)
                }
            
            # 处理数据，添加额外的格式化
            formatted_data = []
            for row in result['data']:
                # 性别转换逻辑
                gender = row.get('gender')
                if gender == '1':
                    gender_display = '男'
                elif gender == '2':
                    gender_display = '女'
                else:
                    gender_display = '-'
                    
                # 日期格式化
                join_date = row.get('join_work_date')
                if join_date:
                    try:
                        # 尝试多种日期格式
                        date_formats = [
                            '%a, %d %b %Y %H:%M:%S GMT',  # Tue, 26 Jul 2011 00:00:00 GMT
                            '%Y-%m-%d %H:%M:%S',          # 2011-07-26 00:00:00
                            '%Y-%m-%d',                   # 2011-07-26
                            '%Y/%m/%d'                    # 2011/07/26
                        ]
                        
                        formatted_date = None
                        for date_format in date_formats:
                            try:
                                date_obj = datetime.strptime(str(join_date), date_format)
                                formatted_date = date_obj.strftime('%Y-%m-%d')
                                break
                            except ValueError:
                                continue
                        
                        if formatted_date is None:
                            INFO.logger.warning(f"无法解析日期: {join_date}")
                            formatted_date = str(join_date)
                            
                    except Exception as e:
                        ERROR.logger.error(f"日期转换失败: {str(e)}, 原始值: {join_date}")
                        formatted_date = str(join_date)
                else:
                    formatted_date = '-'
                formatted_row = {
                    'id': row.get('id'),
                    'name': row.get('name'),
                    'level': row.get('level'),
                    'gender': gender_display,
                    'department': row.get('per_code'),
                    'position': row.get('manage_name'),
                    'entry_date': formatted_date,
                    'status': row.get('status')
                }
                formatted_data.append(formatted_row)
            
            return {
                'data': formatted_data,
                'query_time': result.get('query_time', 0)
            }
        
        except Exception as e:
            ERROR.logger.error(f"获取数据库人员信息失败: {str(e)}")
            return {
                'error': str(e),
                'data': [],
                'query_time': 0
            }

    def get_total_comparison(self):
        """对比总人数数据"""
        try:
            # 获取API数据
            api_data = self.get_organization_info()
            INFO.logger.info(f"API数据: {api_data}")
            
            if not api_data:
                return {"error": "Failed to get API data"}
            
            # 获取数据库数据
            start_time = time.time()
            db_result = self.db.execute_query(TOTAL_NUMBER_OF_PEOPLE)
            query_time = round((time.time() - start_time) * 1000)
            INFO.logger.info(f"数据库结果: {db_result}")
            
            # 确保 api_data 中的总人数是整数
            try:
                api_total = int(api_data.get('总人数', 0))
                INFO.logger.info(f"API总人数: {api_total}")
            except (TypeError, ValueError) as e:
                ERROR.logger.error(f"API总人数转换失败: {str(e)}")
                api_total = 0
            
            # 确保数据库返回的总数是整数
            try:
                # SQLAlchemy 返回的结果结构不同
                db_total = int(db_result['data'][0]['count(*)']) if db_result.get('data') else 0
                INFO.logger.info(f"数据库总人数: {db_total}")
            except (TypeError, ValueError, KeyError, IndexError) as e:
                ERROR.logger.error(f"数据库总人数转换失败: {str(e)}")
                db_total = 0
            
            comparison_data = {
                'api_total': api_total,
                'db_total': db_total,
                'matched': api_total == db_total
            }
            
            INFO.logger.info(f"比较结果: {comparison_data}")
            return {
                'data': comparison_data,
                'query_time': query_time
            }
        
        except Exception as e:
            ERROR.logger.error(f"对比总人数失败: {str(e)}")
            return {"error": str(e)}

    def get_rank_comparison(self):
        """对比职级分布数据"""
        try:
            # 获取API数据
            api_data = self.get_position_level_distribution()
            INFO.logger.info(f"API职级数据: {api_data}")
            
            # 确保 api_data 是字典类型
            if not isinstance(api_data, dict):
                api_data = {}
            
            # 获取数据库数据
            start_time = time.time()
            db_result = self.db.execute_query(RANK_OF_RANK)
            query_time = round((time.time() - start_time) * 1000)
            INFO.logger.info(f"数据库查询结果: {db_result}")
            
            # 初始化所有序列
            db_rank_count = {
                "P序列": {},
                "M序列": {},
                "B序列": {}
            }
            
            # 处理数据库数据
            if db_result and isinstance(db_result, dict) and db_result.get('data'):
                for record in db_result['data']:
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
                        
                    db_rank_count[series][level] = count
                
                INFO.logger.info(f"处理后的数据库数据: {db_rank_count}")
            
            # 创建比较结果
            try:
                comparison = self.comparison.compare_data(api_data, db_rank_count)
            except Exception as e:
                ERROR.logger.error(f"比较数据失败: {str(e)}")
                comparison = {}
            
            comparison_data = {
                'api_data': api_data,
                'db_data': db_rank_count,
                'comparison': comparison
            }
            
            INFO.logger.info(f"最终比较结果: {comparison_data}")
            return {
                'data': comparison_data,
                'query_time': query_time
            }
        
        except Exception as e:
            ERROR.logger.error(f"对比职级分布失败: {str(e)}")
            return {
                'data': {
                    'api_data': {},
                    'db_data': {
                        "P序列": {},
                        "M序列": {},
                        "B序列": {}
                    },
                    'comparison': {}
                },
                'query_time': 0
            }

    def get_api_data(self):
        """获取API数据"""
        try:
            # 使用已有的登录凭证获取数据
            response = requests.post(
                API_ORGANIZATION_INFO,
                json=ORGANIZATION_INFO_DATA,
                headers=self.headers,
                verify=False
            )
            result = response.json()
            if result.get('code') == 0:
                return {"data": result.get('response', {})}
            return {"error": result.get('message', '获取数据失败')}
        except Exception as e:
            ERROR.logger.error(f"获取API数据失败: {str(e)}")
            return {"error": str(e)}

    def login(self):
        """登录获取token"""
        try:
            url = f"{self.BASE_URL}/api/user/login"
            data = {
                "loginName": "admin",
                "password": "123456",
                "type": "account"
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': self.BASE_URL,
                'Referer': f'{self.BASE_URL}/'
            }
            print(f"开始请求登录: {url}")
            print(f"请求头: {headers}")
            print(f"请求数据: {data}")
            
            response = requests.post(
                url, 
                json=data, 
                headers=headers,
                verify=False  # 如果是https但证书有问题，可以添加这个
            )
            
            print(f"登录响应状态码: {response.status_code}")
            print(f"登录响应头: {dict(response.headers)}")
            print(f"登录响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0 and result.get('data'):
                    self.token = result['data'].get('token') or result['data'].get('accessToken')
                    # 保存登录状态
                    self.headers.update({
                        'Authorization': f'Bearer {self.token}'
                    })
                    return result
            
            return {"error": "Login failed", "details": response.text}
        except Exception as e:
            print(f"登录异常: {str(e)}")
            return {"error": str(e)}

    def get_average_age_comparison(self):
        """对比平均年龄数据

        本函数从API和数据库分别获取平均年龄数据，进行对比，判断两者是否一致。
        主要步骤包括：
        1. 获取API数据，并从中提取平均年龄。
        2. 获取数据库数据，并从中计算平均年龄。
        3. 对比API和数据库的平均年龄，允许一定的误差范围。
        4. 返回对比结果，包括API和数据库的平均年龄、差异值及是否匹配。
        """
        try:
            # 获取API数据
            api_data = self.get_organization_info()
            INFO.logger.info(f"API数据: {api_data}")
            
            if not api_data:
                return {"error": "Failed to get API data"}
            
            # 获取API的平均年龄（去掉"岁"字并转换为浮点数）
            try:
                # 先获取原始值
                api_age_str = api_data.get('平均年龄', '0')
                INFO.logger.info(f"API原始年龄字符串: {api_age_str}")
                
                # 去掉"岁"字
                api_age_str = api_age_str.replace('岁', '')
                INFO.logger.info(f"去掉'岁'后的字符串: {api_age_str}")
                
                # 转换为浮点数
                api_avg_age = float(api_age_str)
                INFO.logger.info(f"API平均年龄: {api_avg_age}")
            except (TypeError, ValueError) as e:
                ERROR.logger.error(f"API平均年龄转换失败: {str(e)}")
                api_avg_age = 0
            
            # 获取数据库数据
            start_time = time.time()
            db_result = self.db.execute_query(AVERAGE_AGE_SQL)
            query_time = round((time.time() - start_time) * 1000)
            INFO.logger.info(f"数据库结果: {db_result}")
            
            # 获取数据库的平均年龄
            try:
                db_avg_age = round(float(db_result['data'][0].get('avg_age', 0)), 1) if db_result.get('data') else 0
                INFO.logger.info(f"数据库平均年龄: {db_avg_age}")
            except (TypeError, ValueError, KeyError, IndexError) as e:
                ERROR.logger.error(f"数据库平均年龄转换失败: {str(e)}")
                db_avg_age = 0
            
            # 计算差异（允许0.5岁的误差）
            age_difference = abs(api_avg_age - db_avg_age)
            is_matched = age_difference <= 0.5
            
            comparison_data = {
                'api_avg_age': api_avg_age,
                'db_avg_age': db_avg_age,
                'difference': round(age_difference, 1),
                'matched': is_matched
            }
            
            INFO.logger.info(f"平均年龄比较结果: {comparison_data}")
            return {
                'data': comparison_data,
                'query_time': query_time
            }
        
        except Exception as e:
            ERROR.logger.error(f"对比平均年龄失败: {str(e)}")
            return {"error": str(e)}

    def get_api_personnel_by_level(self, series, level):
        """获取API特定职级的人员数据"""
        try:
            # 检查token是否存在
            if not self.token:
                INFO.logger.info("Token不存在，重新登录")
                self._login()

            # 构建请求参数
            request_url = f"{self.BASE_URL}/api/tds-system/admin/organization/personnel/list"
            request_data = {
                "pageSize": 100,
                "pageNum": 1,
                "level": level,
                "series": series.replace("序列", "")  # 将"P序列"转换为"P"
            }
            
            INFO.logger.info(f"发送请求到: {request_url}")
            INFO.logger.info(f"请求参数: {json.dumps(request_data, ensure_ascii=False)}")
            INFO.logger.info(f"请求头: {json.dumps(self.headers, ensure_ascii=False)}")
            
            # 发送API请求
            response = requests.post(
                request_url,
                json=request_data,
                headers=self.headers,
                verify=False
            )
            
            INFO.logger.info(f"API响应状态码: {response.status_code}")
            INFO.logger.info(f"API响应内容: {response.text}")
            
            result = response.json()
            
            if result.get('code') != 0:
                ERROR.logger.error(f"API请求失败: {result.get('message')}")
                return {"error": result.get('message', '获取数据失败')}
            
            # 从响应中获取人员列表
            personnel_list = []
            response_data = result.get('response', {})
            personnel_data = response_data.get('list', [])
            
            INFO.logger.info(f"解析到的人员数据: {json.dumps(personnel_data, ensure_ascii=False)}")
            
            for person in personnel_data:
                personnel_info = {
                    'id': person.get('id', ''),
                    'name': person.get('name', '-'),
                    'level': person.get('level', level),
                    'gender': person.get('gender', '-'),
                    'department': person.get('department', series),
                    'position': person.get('position', level),
                    'entry_date': person.get('entryDate', '-'),
                    'status': person.get('status', '在职')
                }
                personnel_list.append(personnel_info)
                INFO.logger.info(f"添加人员信息: {json.dumps(personnel_info, ensure_ascii=False)}")
            
            result = {
                'data': personnel_list,
                'total': len(personnel_list)
            }
            INFO.logger.info(f"返回结果: {json.dumps(result, ensure_ascii=False)}")
            return result
            
        except Exception as e:
            ERROR.logger.error(f"获取API人员数据失败: {str(e)}")
            return {"error": str(e)}

    def get_db_personnel_by_level(self, series, level):
        """获取数据库特定职级的人员数据"""
        try:
            # 构建SQL查询
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
                WHERE level = :level
                AND del_flag = 0
            """
            
            # 执行查询
            result = self.db.execute_query(sql, {'level': level})
            
            if not result.get('data'):
                return {
                    'data': [],
                    'total': 0,
                    'query_time': result.get('query_time', 0)
                }
            
            return {
                'data': result['data'],
                'total': len(result['data']),
                'query_time': result.get('query_time', 0)
            }
            
        except Exception as e:
            ERROR.logger.error(f"获取数据库人员数据失败: {str(e)}")
            return {"error": str(e)}
