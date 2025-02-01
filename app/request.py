"""
@Project ：tds_dev 
@File    ：request.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/21 0021 20:36 
"""

from app.base.base_request import BaseRequest
from utils.log_control import INFO, ERROR
from app.config.api_config import API_ORGANIZATION_INFO, ORGANIZATION_INFO_DATA
from app.config.data_mapping import CODE_TO_NAME, EFFICIENCY_NAME_MAPPING, DISPLAY_CONFIG
import requests
import json


class Request(BaseRequest):
    def __init__(self):
        super().__init__()

    def portrait_of_organization_info(self):
        """获取组织画像信息"""
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
                
                # 打印完整的原始数据
                INFO.logger.info("原始数据结构:")
                for tag_group in data.get('tagList', []):
                    INFO.logger.info(f"\n标签组: {tag_group.get('name')} - {tag_group.get('code')}")
                    for tag in tag_group.get('tags', []):
                        INFO.logger.info(f"  标签: {tag.get('name')}")
                        if tag.get('name') == '职级统计' or tag.get('name') == '职级分布':
                            INFO.logger.info(f"  职级数据: {json.dumps(tag, ensure_ascii=False, indent=2)}")
                
                processed_data = {}
                
                if data.get('tagList'):
                    for tag_group in data['tagList']:
                        self._process_tag_group(tag_group, processed_data)
                
                # 打印处理后的数据
                INFO.logger.info("处理后的数据:")
                INFO.logger.info(f"职级分布: {json.dumps(processed_data.get('职级分布'), ensure_ascii=False, indent=2)}")
                
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
                    for item in tag['value']:
                        name = item[0]['value']
                        value = item[1]['value']
                        if '(万)' in name:
                            name = name.replace('(万)', '')
                        elif '(亿)' in name:
                            name = name.replace('(亿)', '')
                        processed_data[name] = value
                elif tag['name'] == '客群分析':
                    for item in tag['value']:
                        name = item[0]['value'].replace('(户)', '')
                        value = item[1]['value']
                        processed_data[name] = value
        
        elif group_code == 'HXMB_ZZHX_RCFX_JGFX':
            for tag in tag_group.get('tags', []):
                INFO.logger.info(f"处理标签: {tag.get('name')}")
                
                if tag['name'] == '职级统计':
                    INFO.logger.info(f"找到职级数据: {tag}")
                    # 按P、M、B三类分组统计
                    p_levels = {}
                    m_levels = {}
                    b_levels = {}
                    
                    for item in tag.get('value', []):
                        try:
                            level = item[0]['value']  # 职级名称，如 P1、M1、B1
                            count = int(item[1]['value'])  # 对应的人数，确保转换为整数
                            INFO.logger.info(f"处理职级: {level} = {count}")
                            
                            if 'P' in level:
                                p_levels[level] = count
                            elif 'M' in level:
                                m_levels[level] = count
                            elif 'B' in level:
                                b_levels[level] = count
                        except (IndexError, KeyError, ValueError) as e:
                            ERROR.logger.error(f"处理职级数据出错: {e}, 数据: {item}")
                            continue
                    
                    processed_data['职级分布'] = {
                        "P序列": p_levels,
                        "M序列": m_levels,
                        "B序列": b_levels
                    }
                    INFO.logger.info(f"职级分布数据: {processed_data['职级分布']}")
                
                elif tag['name'] == '年龄分析':
                    age_dist = {}
                    for item in tag['value']:
                        age_range = item[0]['value']
                        count = item[1]['value']
                        age_dist[age_range] = count
                    processed_data['年龄分布'] = age_dist
                
                elif tag['name'] == '全日制最高学历统计':
                    edu_dist = {}
                    for item in tag['value']:
                        edu_level = item[0]['value']
                        count = item[1]['value']
                        edu_dist[edu_level] = count
                    processed_data['学历分布'] = edu_dist
                
                elif tag['name'] == '工作稳定性':
                    stability_dist = {}
                    for item in tag['value']:
                        tenure = item[0]['value']
                        count = item[1]['value']
                        stability_dist[tenure] = count
                    processed_data['工作稳定性'] = stability_dist
                
                elif tag['name'] == '人员类型汇总':
                    type_dist = {}
                    for item in tag['value']:
                        emp_type = item[0]['value']
                        count = item[1]['value']
                        type_dist[emp_type] = count
                    processed_data['人员类型'] = type_dist
                
                elif tag['name'] == '政治面貌统计':
                    political_dist = {}
                    for item in tag['value']:
                        status = item[0]['value']
                        count = item[1]['value']
                        political_dist[status] = count
                    processed_data['政治面貌'] = political_dist

    def get_position_level_distribution(self):
        """获取职级分布数据"""
        data = self.portrait_of_organization_info()
        if not data or not data.get('tagList'):
            return None
        
        # 从结构分析中提取职级统计数据
        for tag_group in data['tagList']:
            if tag_group.get('code') == 'HXMB_ZZHX_RCFX_JGFX':
                for tag in tag_group.get('tags', []):
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
                        
                        return {
                            "P序列": p_levels,
                            "M序列": m_levels,
                            "B序列": b_levels
                        }
        return None


if __name__ == '__main__':
    request = Request()
    data = request.portrait_of_organization_info()
    
    if data:
        # 使用配置文件中的展示配置打印数据
        # 组织概览
        print(f"\n{DISPLAY_CONFIG['overview']['title']}")
        for field in DISPLAY_CONFIG['overview']['fields']:
            print(f"{field}: {data.get(field)}")

        # 人效分析
        print(f"\n{DISPLAY_CONFIG['efficiency']['title']}")
        for field in DISPLAY_CONFIG['efficiency']['fields']:
            print(f"{field}: {data.get(field)}")

        # 团队业绩
        print(f"\n{DISPLAY_CONFIG['performance']['title']}")
        for field in DISPLAY_CONFIG['performance']['fields']:
            print(f"{field}: {data.get(field)}")

        # 客群分析
        print(f"\n{DISPLAY_CONFIG['customer']['title']}")
        for field in DISPLAY_CONFIG['customer']['fields']:
            print(f"{field}: {data.get(field)}")

        # 职级分布
        position_dist = request.get_position_level_distribution()
        if position_dist:
            print(f"\n{DISPLAY_CONFIG['position']['title']}")
            for series in DISPLAY_CONFIG['position']['series']:
                levels = position_dist.get(series, {})
                if levels:
                    print(f"\n{series}:")
                    sorted_levels = sorted(levels.items(), key=lambda x: x[0])
                    for level, count in sorted_levels:
                        print(f"{level}: {count}人")

        # 处理其他分布数据
        for dist in DISPLAY_CONFIG['distributions']:
            if data.get(dist['key']):
                print(f"\n{dist['title']}")
                for key, count in data[dist['key']].items():
                    print(f"{key}: {count}人") 