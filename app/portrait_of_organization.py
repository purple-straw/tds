"""
组织画像信息处理模块

此模块主要用于获取和处理组织画像相关的数据，包括：
- 组织概览信息（人数、比例等）
- 人效分析数据
- 团队业绩数据
- 客群分析数据
- 各类分布数据（年龄、学历、职级等）

主要功能：
1. 从API获取原始数据
2. 处理和转换数据格式
3. 提供各类数据的访问方法
"""

from app.base.base_request import BaseRequest
from app.utils.log_control import INFO, ERROR
from app.config.api_config import API_ORGANIZATION_INFO, ORGANIZATION_INFO_DATA
from app.config.data_mapping import CODE_TO_NAME, EFFICIENCY_NAME_MAPPING
import requests
import json


class Request(BaseRequest):
    """组织画像数据请求处理类"""

    def __init__(self):
        """初始化请求处理器，继承基础请求类"""
        super().__init__()

    def _process_tag_value(self, tag_value):
        """
        处理标签值，提取名称和数量
        
        Args:
            tag_value: API返回的原始标签值数据
            
        Returns:
            dict: 处理后的键值对，如 {"总人数": "100"}
        """
        return {
            item[0]['value'].replace('(万)', '').replace('(亿)', '').replace('(户)', ''): item[1]['value']
            for item in tag_value
        }

    def _process_distribution_data(self, tag_value):
        """
        处理分布数据
        
        Args:
            tag_value: API返回的分布数据
            
        Returns:
            dict: 处理后的分布数据，如 {"18-25岁": "10"}
        """
        return {item[0]['value']: item[1]['value'] for item in tag_value}

    def portrait_of_organization_info(self):
        """
        获取组织画像完整信息
        
        Returns:
            dict: 处理后的组织画像数据，包含所有维度信息
            None: 获取失败时返回None
        """
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

            if result.get('code') == 0:
                INFO.logger.info("获取组织画像信息成功")
                data = result.get('response', {})
                processed_data = {}

                if data.get('tagList'):
                    for tag_group in data['tagList']:
                        self._process_tag_group(tag_group, processed_data)

                return processed_data
            else:
                ERROR.logger.error(f"获取组织画像信息失败: {result.get('message')}")
                return None

        except requests.exceptions.RequestException as e:
            ERROR.logger.error(f"请求失败: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            ERROR.logger.error(f"JSON解析失败: {str(e)}")
            raise

    def _process_tag_group(self, tag_group, processed_data):
        """
        处理标签组数据
        
        Args:
            tag_group: API返回的标签组数据
            processed_data: 用于存储处理后的数据的字典
        """
        group_name = tag_group.get('name')
        group_code = tag_group.get('code')

        # 处理组织概览数据
        if group_name == '组织概览':
            for tag in tag_group.get('tags', []):
                if tag['code'] in CODE_TO_NAME:
                    processed_data[CODE_TO_NAME[tag['code']]] = tag['value']

        # 处理人效分析数据
        elif group_code == 'RXFX':
            for tag in tag_group.get('tags', []):
                if tag['name'] in EFFICIENCY_NAME_MAPPING:
                    processed_data[EFFICIENCY_NAME_MAPPING[tag['name']]] = tag['value']

        # 处理业绩和客群数据
        elif group_code == 'zzhx_rcfx_yjfx':
            for tag in tag_group.get('tags', []):
                if tag['name'] == '团队业绩':
                    processed_data.update(self._process_tag_value(tag['value']))
                elif tag['name'] == '客群分析':
                    processed_data.update(self._process_tag_value(tag['value']))

        # 处理结构分析数据
        elif group_code == 'HXMB_ZZHX_RCFX_JGFX':
            self._process_structure_analysis(tag_group.get('tags', []), processed_data)

    def _process_structure_analysis(self, tags, processed_data):
        """
        处理结构分析数据
        
        Args:
            tags: 结构分析相关的标签数据
            processed_data: 用于存储处理后的数据的字典
        """
        for tag in tags:
            # 处理职级统计数据
            if tag['name'] == '职级统计':
                # 按P、M、B三类分组统计
                p_levels = {}
                m_levels = {}
                b_levels = {}

                for item in tag['value']:
                    level = item[0]['value']  # 职级名称，如 P1、M1、B1
                    count = int(item[1]['value'])  # 对应的人数

                    if 'P' in level:
                        p_levels[level] = count
                    elif 'M' in level:
                        m_levels[level] = count
                    elif 'B' in level:
                        b_levels[level] = count

                processed_data['职级分布'] = {
                    "P序列": p_levels,
                    "M序列": m_levels,
                    "B序列": b_levels
                }
            elif tag['name'] in ['年龄分析', '全日制最高学历统计', '工作稳定性', '人员类型汇总']:
                key_mapping = {
                    '年龄分析': '年龄分布',
                    '全日制最高学历统计': '学历分布',
                    '工作稳定性': '工作稳定性',
                    '人员类型汇总': '人员类型'
                }
                processed_data[key_mapping[tag['name']]] = self._process_distribution_data(tag['value'])

    def get_overview_info(self):
        """
        获取组织概览信息
        
        Returns:
            dict: 组织概览数据
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
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
        """
        获取人效分析数据
        
        Returns:
            dict: 人效分析数据
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
        if data:
            return {
                "人均利润": data.get("人均利润"),
                "人均毛利": data.get("人均毛利"),
                "人均收入": data.get("人均收入")
            }
        return None

    def get_team_performance(self):
        """
        获取团队业绩数据
        
        Returns:
            dict: 包含团队业绩各项指标的字典，如：
                {
                    "日均余额": value,
                    "营业净收入": value,
                    "人效": value,
                    "存款增量": value,
                    "贷款增量": value,
                    "贷款规模": value
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
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
        """
        获取客群分析数据
        
        Returns:
            dict: 包含客群分析各项指标的字典，如：
                {
                    "总客群数": value,
                    "高价值客群数": value,
                    "大中客群数": value,
                    "基础客群数": value,
                    "长尾客群数": value
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
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
        """
        获取年龄分布数据
        
        Returns:
            dict: 年龄分布数据，如：
                {
                    "18-25岁": count,
                    "26-35岁": count,
                    ...
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
        if data:
            return data.get("年龄分布")
        return None

    def get_education_distribution(self):
        """
        获取学历分布数据
        
        Returns:
            dict: 学历分布数据，如：
                {
                    "博士研究生": count,
                    "硕士研究生": count,
                    "大学本科": count,
                    ...
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
        if data:
            return data.get("学历分布")
        return None

    def get_position_level_distribution(self):
        """
        获取职级分布数据
        
        Returns:
            dict: 职级分布数据，按序列分组，如：
                {
                    "P序列": {"P1": count, "P2": count, ...},
                    "M序列": {"M1": count, "M2": count, ...},
                    "B序列": {"B1": count, "B2": count, ...}
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
        if not data:
            return None
        return data.get('职级分布')

    def get_political_status_distribution(self):
        """
        获取政治面貌分布数据
        
        Returns:
            dict: 政治面貌分布数据，如：
                {
                    "中共党员": count,
                    "共青团员": count,
                    "群众": count,
                    ...
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
        if not data or not data.get('tagList'):
            return None

        for tag_group in data['tagList']:
            if tag_group.get('code') == 'HXMB_ZZHX_RCFX_JGFX':
                for tag in tag_group.get('tags', []):
                    if tag['name'] == '政治面貌统计':
                        political_data = {}
                        for item in tag['value']:
                            status = item[0]['value']  # 政治面貌
                            count = item[1]['value']  # 对应的人数
                            political_data[status] = count
                        return political_data
        return None

    def get_work_stability_distribution(self):
        """
        获取工作稳定性分布数据
        
        Returns:
            dict: 工作稳定性分布数据，如：
                {
                    "1年及以下": count,
                    "1-3年": count,
                    "4-6年": count,
                    ...
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
        if data:
            return data.get("工作稳定性")
        return None

    def get_employee_type_distribution(self):
        """
        获取人员类型汇总数据
        
        Returns:
            dict: 人员类型分布数据，如：
                {
                    "全日制合同工": count,
                    "非全日制员工": count,
                    "退休返聘人员": count,
                    ...
                }
            None: 获取失败时返回None
        """
        data = self.portrait_of_organization_info()
        if data:
            return data.get("人员类型")
        return None


if __name__ == '__main__':
    """
    主函数：用于测试和展示数据
    
    功能：
    1. 获取组织画像数据
    2. 格式化展示各维度数据
    3. 提供数据可视化展示
    """
    request = Request()
    data = request.portrait_of_organization_info()

    if data:
        def get_str_width(s):
            """计算字符串的显示宽度，中文字符计为2，其他字符计为1"""
            width = 0
            for c in s:
                width += 2 if '\u4e00' <= c <= '\u9fff' else 1
            return width

        # 收集所有可能的键值
        all_keys = [
            # 组织概览
            "总人数", "正式工总人数", "男女比例", "平均年龄", "平均司龄", 
            "管理岗人数", "平均汇报深度", "平均管理幅度", "试用期人数", 
            "党员比例", "校招生比例", "近一年新员工比例", "近一年离职率", 
            "官兵比",
            # 人效分析
            "人均利润", "人均毛利", "人均收入",
            # 团队业绩
            "日均余额", "营业净收入", "人效", "存款增量", "贷款增量", "贷款规模",
            # 客群分析
            "总客群数", "高价值客群数", "大中客群数", "基础客群数", "长尾客群数"
        ]

        # 添加分布数据中的键值
        if data.get("年龄分布"):
            all_keys.extend(data["年龄分布"].keys())
        if data.get("学历分布"):
            all_keys.extend(data["学历分布"].keys())
        if data.get("工作稳定性"):
            all_keys.extend(data["工作稳定性"].keys())
        if data.get("人员类型"):
            all_keys.extend(data["人员类型"].keys())
        if data.get("职级分布"):
            for levels in data["职级分布"].values():
                all_keys.extend(levels.keys())

        # 计算最长键值的显示宽度
        max_width = max(get_str_width(key) for key in all_keys)
        # 为了美观，给最长键值加上一些空格
        max_width += 0

        def format_key(key):
            """格式化键值，使其显示宽度一致"""
            current_width = get_str_width(key)
            padding = max_width - current_width
            return key + ' ' * padding

        # 组织概览
        print("\n" + "="*50)
        print("组织概览".center(50))
        print("="*50)
        overview_data = {
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
        for key, value in overview_data.items():
            print(f"{format_key(key)}: {value}")

        # 人效分析
        print("\n" + "="*50)
        print("人效分析".center(50))
        print("="*50)
        efficiency_data = {
            "人均利润": data.get("人均利润"),
            "人均毛利": data.get("人均毛利"),
            "人均收入": data.get("人均收入")
        }
        for key, value in efficiency_data.items():
            print(f"{format_key(key)}: {value}")

        # 团队业绩
        print("\n" + "="*50)
        print("团队业绩".center(50))
        print("="*50)
        performance_data = {
            "日均余额": data.get("日均余额"),
            "营业净收入": data.get("营业净收入"),
            "人效": data.get("人效"),
            "存款增量": data.get("存款增量"),
            "贷款增量": data.get("贷款增量"),
            "贷款规模": data.get("贷款规模")
        }
        for key, value in performance_data.items():
            print(f"{format_key(key)}: {value}")

        # 客群分析
        print("\n" + "="*50)
        print("客群分析".center(50))
        print("="*50)
        customer_data = {
            "总客群数": data.get("总客群数"),
            "高价值客群数": data.get("高价值客群数"),
            "大中客群数": data.get("大中客群数"),
            "基础客群数": data.get("基础客群数"),
            "长尾客群数": data.get("长尾客群数")
        }
        for key, value in customer_data.items():
            print(f"{format_key(key)}: {value}")

        # 年龄分布
        if data.get("年龄分布"):
            print("\n" + "="*50)
            print("年龄分布".center(50))
            print("="*50)
            for age_range, count in data["年龄分布"].items():
                print(f"{format_key(age_range)}: {count}人")

        # 学历分布
        if data.get("学历分布"):
            print("\n" + "="*50)
            print("学历分布".center(50))
            print("="*50)
            for edu_level, count in data["学历分布"].items():
                print(f"{format_key(edu_level)}: {count}人")

        # 职级分布
        if data.get('职级分布'):
            print("\n" + "="*50)
            print("职级分布".center(50))
            print("="*50)
            for series, levels in data['职级分布'].items():
                print(f"\n{format_key(series)}:")
                print("-"*30)
                sorted_levels = sorted(levels.items(), key=lambda x: x[0])
                for level, count in sorted_levels:
                    print(f"{format_key(level)}: {count}人")
        else:
            print("\n" + "="*50)
            print("职级分布".center(50))
            print("="*50)
            print("未获取到职级分布数据")

        # 工作稳定性
        if data.get("工作稳定性"):
            print("\n" + "="*50)
            print("工作稳定性".center(50))
            print("="*50)
            for tenure, count in data["工作稳定性"].items():
                print(f"{format_key(tenure)}: {count}人")

        # 人员类型
        if data.get("人员类型"):
            print("\n" + "="*50)
            print("人员类型汇总".center(50))
            print("="*50)
            for emp_type, count in data["人员类型"].items():
                print(f"{format_key(emp_type)}: {count}人")
