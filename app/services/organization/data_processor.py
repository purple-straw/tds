"""
数据处理相关的工具类
"""


class OrganizationDataProcessor:
    @staticmethod
    def process_tag_value(tag_value):
        """处理标签值，提取名称和数量"""
        return {
            item[0]['value'].replace('(万)', '').replace('(亿)', '').replace('(户)', ''): item[1]['value']
            for item in tag_value
        }

    @staticmethod
    def process_distribution_data(tag_value):
        """处理分布数据"""
        return {item[0]['value']: item[1]['value'] for item in tag_value}

    @staticmethod
    def process_position_levels(tag_value):
        """处理职级数据"""
        p_levels = {}
        m_levels = {}
        b_levels = {}

        for item in tag_value:
            level = item[0]['value']
            count = int(item[1]['value'])

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

    @staticmethod
    def process_new_data(data):
        """处理新的数据类型"""
        # 新的数据处理逻辑
        pass
