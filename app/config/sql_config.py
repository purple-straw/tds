"""
SQL查询配置模块

此模块包含所有用于数据对比的SQL查询语句
"""

# 总人数
TOTAL_NUMBER_OF_PEOPLE = """
SELECT count(*) from per_main pm """

# 人员主表的数据
PERSONNEL_MAIN_TABLE_SQL = """
SELECT * from per_main pm 

"""
# 职级
RANK_OF_RANK = """
SELECT 
    level,
    COUNT(*) as count
FROM per_main 
WHERE level IS NOT NULL 
GROUP BY level
ORDER BY level
"""

# 男女人数比例
GENDER_RATIO_SQL = """
SELECT gender, name from per_main pm 
"""

# 组织概览查询
ORGANIZATION_OVERVIEW_SQL = """
SELECT 
    total_count as '总人数',
    formal_count as '正式工总人数',
    gender_ratio as '男女比例',
    avg_age as '平均年龄',
    avg_tenure as '平均司龄',
    manager_count as '管理岗人数',
    avg_report_depth as '平均汇报深度',
    avg_manage_span as '平均管理幅度',
    probation_count as '试用期人数',
    party_member_ratio as '党员比例',
    campus_ratio as '校招生比例',
    new_emp_ratio as '近一年新员工比例',
    turnover_ratio as '近一年离职率',
    manager_staff_ratio as '官兵比'
FROM organization_overview 
WHERE date = CURRENT_DATE
"""

# 人效分析查询
EFFICIENCY_ANALYSIS_SQL = """
SELECT 
    profit_per_capita as '人均利润',
    gross_profit_per_capita as '人均毛利',
    income_per_capita as '人均收入'
FROM efficiency_analysis
WHERE date = CURRENT_DATE
"""

# 团队业绩查询
TEAM_PERFORMANCE_SQL = """
SELECT 
    daily_balance as '日均余额',
    net_income as '营业净收入',
    efficiency as '人效',
    deposit_increment as '存款增量',
    loan_increment as '贷款增量',
    loan_scale as '贷款规模'
FROM team_performance
WHERE date = CURRENT_DATE
"""

# 客群分析查询
CUSTOMER_ANALYSIS_SQL = """
SELECT 
    total_customers as '总客群数',
    high_value_customers as '高价值客群数',
    medium_customers as '大中客群数',
    basic_customers as '基础客群数',
    long_tail_customers as '长尾客群数'
FROM customer_analysis
WHERE date = CURRENT_DATE
"""

# 年龄分布查询
AGE_DISTRIBUTION_SQL = """
SELECT 
    age_range as '年龄段',
    count as '人数'
FROM age_distribution
WHERE date = CURRENT_DATE
"""

# 学历分布查询
EDUCATION_DISTRIBUTION_SQL = """
SELECT 
    education_level as '学历',
    count as '人数'
FROM education_distribution
WHERE date = CURRENT_DATE
"""

# 职级分布查询
POSITION_LEVEL_SQL = """
SELECT 
    level_code as '职级',
    count as '人数'
FROM position_level_distribution
WHERE date = CURRENT_DATE
"""

# 工作稳定性查询
WORK_STABILITY_SQL = """
SELECT 
    tenure_range as '工作年限',
    count as '人数'
FROM work_stability
WHERE date = CURRENT_DATE
"""

# 人员类型查询
EMPLOYEE_TYPE_SQL = """
SELECT 
    emp_type as '人员类型',
    count as '人数'
FROM employee_type_distribution
WHERE date = CURRENT_DATE
"""

# 添加或修改数据库表的查询语句
EMPLOYEE_TABLE_QUERY = """
SELECT 
    id,
    name,
    level,
    gender,
    per_code as department,
    manage_name,
    join_work_date,
    status
FROM per_main 
ORDER BY id
"""

# 平均年龄查询
AVERAGE_AGE_SQL = """
SELECT 
    AVG(
        TIMESTAMPDIFF(
            YEAR,  
            STR_TO_DATE(birthday, '%Y-%m-%d'), 
            CURRENT_DATE
        )
    ) as avg_age
FROM per_main 
WHERE birthday IS NOT NULL
"""

# 将所有查询组织到一个字典中
COMPARISON_QUERIES = {
    "organization_overview": ORGANIZATION_OVERVIEW_SQL,
    "efficiency_analysis": EFFICIENCY_ANALYSIS_SQL,
    "team_performance": TEAM_PERFORMANCE_SQL,
    "customer_analysis": CUSTOMER_ANALYSIS_SQL,
    "age_distribution": AGE_DISTRIBUTION_SQL,
    "education_distribution": EDUCATION_DISTRIBUTION_SQL,
    "position_level": POSITION_LEVEL_SQL,
    "work_stability": WORK_STABILITY_SQL,
    "employee_type": EMPLOYEE_TYPE_SQL
}
