"""
@Project ：tds_dev 
@File    ：data_mapping.py
@IDE     ：PyCharm 
@Author  ：靓仔
@Date    ：2025/1/21
"""

# 组织概览字段映射
CODE_TO_NAME = {
    'ZZ_ZRS': '总人数',
    'ZZ_ZSGZRS': '正式工总人数',
    'ZZ_NVBL': '男女比例',
    'ZZ_PJNL': '平均年龄',
    'ZZ_PJSL': '平均司龄',
    'ZZ_GLGRS': '管理岗人数',
    'PJHBSD': '平均汇报深度',
    'PJGLFD': '平均管理幅度',
    'SYQRS': '试用期人数',
    'ZZ_DYBL': '党员比例',
    'ZZ_XZSBL': '校招生比例',
    'ZZ_JYNXYGBL': '近一年新员工比例',
    'ZZ_JYNLIZL': '近一年离职率',
    'ZZ_GLGBL': '官兵比'
}

# 新增的映射关系
NEW_CODE_MAPPING = {
    'NEW_CODE_1': '新字段1',
    'NEW_CODE_2': '新字段2',
}

# 人效分析字段映射
EFFICIENCY_NAME_MAPPING = {
    '人均利润（万）': '人均利润',
    '人均毛利（万）': '人均毛利',
    '人均收入（万）': '人均收入'
}

# 职级序列配置
POSITION_LEVELS = {
    "P": "P序列",
    "M": "M序列",
    "B": "B序列"
}

# 数据展示配置
DISPLAY_CONFIG = {
    "overview": {
        "title": "=== 组织概览 ===",
        "fields": [
            "总人数", "正式工总人数", "男女比例", "平均年龄", "平均司龄",
            "管理岗人数", "平均汇报深度", "平均管理幅度", "试用期人数",
            "党员比例", "校招生比例", "近一年新员工比例", "近一年离职率", "官兵比"
        ]
    },
    "efficiency": {
        "title": "=== 人效分析 ===",
        "fields": ["人均利润", "人均毛利", "人均收入"]
    },
    "performance": {
        "title": "=== 团队业绩 ===",
        "fields": ["日均余额", "营业净收入", "人效", "存款增量", "贷款增量", "贷款规模"]
    },
    "customer": {
        "title": "=== 客群分析 ===",
        "fields": ["总客群数", "高价值客群数", "大中客群数", "基础客群数", "长尾客群数"]
    },
    "distributions": [
        {"key": "年龄分布", "title": "=== 年龄分布 ==="},
        {"key": "学历分布", "title": "=== 学历分布 ==="},
        {"key": "工作稳定性", "title": "=== 工作稳定性 ==="},
        {"key": "人员类型", "title": "=== 人员类型汇总 ==="}
    ],
    "position": {
        "title": "=== 职级分布 ===",
        "series": ["P序列", "M序列", "B序列"]
    }
} 