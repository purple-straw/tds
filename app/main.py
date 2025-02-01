"""
主程序入口
"""
from app.services.organization.organization_service import OrganizationService
from app.utils.data_utils import format_output


def main():
    # 创建服务实例
    service = OrganizationService()
    
    # 对比总人数
    total_comparison = service.compare_total_people()
    print("\n" + "="*50)
    print("总人数对比".center(50))
    print("="*50)
    if "error" not in total_comparison:
        print(f"API总人数: {total_comparison['api_total']}")
        print(f"数据库总人数: {total_comparison['db_total']}")
        print(f"对比结果: {'匹配' if total_comparison['matched'] else '不匹配'}")
    else:
        print(f"对比失败: {total_comparison['error']}")
    
    # 对比职级分布
    rank_comparison = service.compare_rank_distribution()
    print("\n" + "="*50)
    print("职级分布对比".center(50))
    print("="*50)
    if "error" not in rank_comparison:
        print("\nAPI数据:")
        for level, count in rank_comparison['api_data'].items():
            print(f"  {level}: {count}")
            
        print("\n数据库数据:")
        for level, count in rank_comparison['db_data'].items():
            print(f"  {level}: {count}")
            
        if rank_comparison['comparison']:
            print("\n差异:")
            for level, diff in rank_comparison['comparison'].items():
                print(f"  {level}:")
                print(f"    API值: {diff['api_value']}")
                print(f"    DB值: {diff['db_value']}")
        else:
            print("\n无差异")
    else:
        print(f"对比失败: {rank_comparison['error']}")


if __name__ == '__main__':
    main()
