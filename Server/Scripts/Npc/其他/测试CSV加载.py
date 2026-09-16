# -*- coding: utf-8 -*-
"""
测试CSV加载功能
"""

import os
import csv

def test_csv_loading():
    """测试CSV文件加载"""
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    print("=== 测试CSV加载功能 ===")
    print("CSV文件路径: {}".format(csv_file_path))
    print("文件是否存在: {}".format(os.path.exists(csv_file_path)))
    
    if not os.path.exists(csv_file_path):
        print("❌ CSV文件不存在！")
        return False
    
    equipment_list = []
    rewards_dict = {}
    
    try:
        # 尝试多种编码读取CSV文件
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
        
        for encoding in encodings:
            try:
                print("尝试使用 {} 编码读取...".format(encoding))
                with open(csv_file_path, 'r', encoding=encoding) as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        equipment_name = row['装备名称'].strip()
                        gold_amount = int(row['回收价格'])
                        equipment_type = row.get('装备类型', '').strip()
                        
                        if equipment_name and gold_amount > 0:
                            equipment_list.append(equipment_name)
                            rewards_dict[equipment_name] = {
                                "gold": gold_amount,
                                "type": equipment_type
                            }
                
                print("✅ 成功使用 {} 编码读取CSV文件".format(encoding))
                print("📊 加载统计:")
                print("  - 装备数量: {}".format(len(equipment_list)))
                print("  - 奖励字典大小: {}".format(len(rewards_dict)))
                
                # 显示前5个装备作为示例
                print("📋 前5个装备示例:")
                for i, equipment in enumerate(equipment_list[:5]):
                    reward = rewards_dict[equipment]
                    print("  {}. {} - {}金币 ({})".format(i+1, equipment, reward['gold'], reward['type']))
                
                return True
                
            except Exception as e:
                print("❌ 使用 {} 编码读取失败: {}".format(encoding, e))
                continue
        
        print("❌ 无法使用任何编码读取CSV文件")
        return False
        
    except Exception as e:
        print("❌ 读取CSV文件时出错: {}".format(e))
        return False

if __name__ == "__main__":
    success = test_csv_loading()
    if success:
        print("\n✅ CSV加载测试成功！")
    else:
        print("\n❌ CSV加载测试失败！")
    
    input("按回车键退出...") 