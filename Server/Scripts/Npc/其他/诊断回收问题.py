# -*- coding: utf-8 -*-
"""
诊断回收功能问题
"""

import os
import csv

def diagnose_recycle_issue():
    """诊断回收功能问题"""
    print("=== 诊断回收功能问题 ===")
    
    # 1. 检查CSV文件
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    print("1. 检查CSV文件:")
    print("   - 文件路径: {}".format(csv_file_path))
    print("   - 文件存在: {}".format(os.path.exists(csv_file_path)))
    
    if os.path.exists(csv_file_path):
        file_size = os.path.getsize(csv_file_path)
        print("   - 文件大小: {} 字节".format(file_size))
    
    # 2. 测试CSV加载
    print("\n2. 测试CSV加载:")
    equipment_list = []
    rewards_dict = {}
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
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
        
        print("   ✅ CSV加载成功")
        print("   - 装备数量: {}".format(len(equipment_list)))
        print("   - 奖励字典大小: {}".format(len(rewards_dict)))
        
    except Exception as e:
        print("   ❌ CSV加载失败: {}".format(e))
        return False
    
    # 3. 检查便捷传送.py文件
    print("\n3. 检查便捷传送.py文件:")
    teleport_file = os.path.join(os.path.dirname(__file__), "便捷传送.py")
    print("   - 文件路径: {}".format(teleport_file))
    print("   - 文件存在: {}".format(os.path.exists(teleport_file)))
    
    if os.path.exists(teleport_file):
        file_size = os.path.getsize(teleport_file)
        print("   - 文件大小: {} 字节".format(file_size))
        
        # 检查是否包含CSV加载代码
        try:
            with open(teleport_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'load_recycle_config_from_csv' in content:
                    print("   ✅ 包含CSV加载函数")
                else:
                    print("   ❌ 不包含CSV加载函数")
                
                if 'RECYCLE_EQUIPMENT, RECYCLE_REWARDS = load_recycle_config_from_csv()' in content:
                    print("   ✅ 包含CSV配置加载调用")
                else:
                    print("   ❌ 不包含CSV配置加载调用")
                    
        except Exception as e:
            print("   ❌ 读取便捷传送.py失败: {}".format(e))
    
    # 4. 检查日志文件
    print("\n4. 检查日志文件:")
    log_file = "equipment_recycler.log"
    print("   - 日志文件: {}".format(log_file))
    print("   - 文件存在: {}".format(os.path.exists(log_file)))
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print("   - 日志行数: {}".format(len(lines)))
                if lines:
                    print("   - 最后一行: {}".format(lines[-1].strip()))
        except Exception as e:
            print("   ❌ 读取日志文件失败: {}".format(e))
    
    # 5. 模拟回收逻辑
    print("\n5. 模拟回收逻辑:")
    print("   - 回收列表长度: {}".format(len(equipment_list)))
    print("   - 奖励字典长度: {}".format(len(rewards_dict)))
    
    # 检查一些常见装备
    test_equipment = ["匕首", "井中月", "银蛇", "无极棍", "逍遥扇"]
    print("   - 测试装备检查:")
    for equipment in test_equipment:
        if equipment in equipment_list:
            reward = rewards_dict[equipment]
            print("     ✅ {} - {}金币 ({})".format(equipment, reward['gold'], reward['type']))
        else:
            print("     ❌ {} - 不在回收列表中".format(equipment))
    
    print("\n=== 诊断完成 ===")
    return True

if __name__ == "__main__":
    diagnose_recycle_issue()
    input("按回车键退出...") 