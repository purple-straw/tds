"""
通用数据处理工具
"""


class DisplayConfig:
    """显示配置"""
    SEPARATOR_LENGTH = 60
    SECTION_SEPARATOR = "=" * SEPARATOR_LENGTH
    SUB_SEPARATOR = "-" * 30

    SECTIONS = {
        "overview": "组织概览",
        "efficiency": "人效分析",
        "performance": "团队业绩",
        "customer": "客群分析",
        "年龄分布": "年龄分布",
        "学历分布": "学历分布",
        "工作稳定性": "工作稳定性",
        "人员类型": "人员类型汇总"
    }


class FormatOutput:
    def __init__(self):
        self.config = DisplayConfig()
        self.max_width = 0

    def _initialize_max_width(self, data):
        """初始化最大宽度"""
        all_keys = self._collect_all_keys(data)
        self.max_width = max(self.get_str_width(key) for key in all_keys) + 4

    def _collect_all_keys(self, data):
        """收集所有键值"""
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
        for key in ["年龄分布", "学历分布", "工作稳定性", "人员类型"]:
            if data.get(key):
                all_keys.extend(data[key].keys())

        if data.get("职级分布"):
            for levels in data["职级分布"].values():
                all_keys.extend(levels.keys())

        return all_keys

    def get_str_width(self, s):
        """计算字符串的显示宽度"""
        width = 0
        for c in s:
            width += 2 if '\u4e00' <= c <= '\u9fff' else 1
        return width

    def format_key(self, key, max_width):
        """格式化键值"""
        current_width = self.get_str_width(key)
        padding = max_width - current_width
        return key + ' ' * padding

    def print_organization_info(self, data):
        """打印组织信息"""
        self._initialize_max_width(data)

        # 打印各个部分
        self._print_overview(data)
        self._print_efficiency(data)
        self._print_performance(data)
        self._print_customer(data)
        self._print_distributions(data)

    def _print_overview(self, data):
        """打印组织概览"""
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
        self.print_section(self.config.SECTIONS["overview"], overview_data)

    def print_section(self, title, data_dict, with_unit=False, sort_keys=False):
        """打印一个数据部分"""
        print("\n" + "=" * 60)
        print(title.center(60))
        print("=" * 60)

        items = data_dict.items()
        if sort_keys:
            items = sorted(items, key=lambda x: x[0])

        for key, value in items:
            if value is None:
                value = "-"
            if with_unit:
                print(f"{self.format_key(key, self.max_width)}: {value}人")
            else:
                print(f"{self.format_key(key, self.max_width)}: {value}")

    def _print_efficiency(self, data):
        """打印人效分析"""
        efficiency_data = {
            "人均利润": data.get("人均利润"),
            "人均毛利": data.get("人均毛利"),
            "人均收入": data.get("人均收入")
        }
        self.print_section(self.config.SECTIONS["efficiency"], efficiency_data)

    def _print_performance(self, data):
        """打印团队业绩"""
        performance_data = {
            "日均余额": data.get("日均余额"),
            "营业净收入": data.get("营业净收入"),
            "人效": data.get("人效"),
            "存款增量": data.get("存款增量"),
            "贷款增量": data.get("贷款增量"),
            "贷款规模": data.get("贷款规模")
        }
        self.print_section(self.config.SECTIONS["performance"], performance_data)

    def _print_customer(self, data):
        """打印客群分析"""
        customer_data = {
            "总客群数": data.get("总客群数"),
            "高价值客群数": data.get("高价值客群数"),
            "大中客群数": data.get("大中客群数"),
            "基础客群数": data.get("基础客群数"),
            "长尾客群数": data.get("长尾客群数")
        }
        self.print_section(self.config.SECTIONS["customer"], customer_data)

    def _print_distributions(self, data):
        """打印年龄分布、学历分布、工作稳定性、人员类型"""
        for key, value in data.items():
            if key in ["年龄分布", "学历分布", "工作稳定性", "人员类型"]:
                self.print_section(self.config.SECTIONS[key], value, True)

        # 职级分布
        if data.get('职级分布'):
            print("\n" + "=" * 50)
            print("职级分布".center(50))
            print("=" * 50)
            for series, levels in data['职级分布'].items():
                print(f"\n{self.format_key(series, self.max_width)}:")
                print("-" * 30)
                sorted_levels = sorted(levels.items(), key=lambda x: x[0])
                for level, count in sorted_levels:
                    print(f"{self.format_key(level, self.max_width)}: {count}人")


format_output = FormatOutput()

"""
数据处理工具模块
"""

def compare_lists(list1, list2):
    """
    比较两个列表，返回list2中与list1不同的元素
    
    Args:
        list1: 基准列表
        list2: 需要比较的列表
        
    Returns:
        dict: 包含比较结果的字典，格式如下：
            {
                'matched': [...],  # list2中与list1匹配的元素
                'unmatched': [...],  # list2中与list1不匹配的元素
                'missing': [...],  # list1中有但list2中没有的元素
                'extra': [...]  # list2中有但list1中没有的元素
            }
    """
    # 转换为集合以便比较
    set1 = set(list1)
    set2 = set(list2)
    
    # 找出匹配和不匹配的元素
    matched = set1.intersection(set2)
    missing = set1 - set2
    extra = set2 - set1
    
    return {
        'matched': sorted(list(matched)),
        'missing': sorted(list(missing)),
        'extra': sorted(list(extra))
    }


def print_comparison_results(results, title="比较结果"):
    """
    格式化打印比较结果
    
    Args:
        results: compare_lists函数返回的结果字典
        title: 比较结果的标题
    """
    print(f"\n{'='*50}")
    print(f"{title}".center(50))
    print('='*50)
    
    if results['matched']:
        print("\n匹配的元素:")
        for item in results['matched']:
            print(f"  - {item}")
            
    if results['missing']:
        print("\n缺失的元素 (在列表1中存在但在列表2中不存在):")
        for item in results['missing']:
            print(f"  - {item}")
            
    if results['extra']:
        print("\n额外的元素 (在列表2中存在但在列表1中不存在):")
        for item in results['extra']:
            print(f"  - {item}")
