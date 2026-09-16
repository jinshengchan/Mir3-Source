# -*- coding: utf-8 -*-
"""
测试CSV加载 - 简化版
模拟游戏引擎环境
"""

import sys
import os
import csv

def load_recycle_config_from_csv():
    """
    直接从CSV文件加载回收配置 - Python 2.7兼容版本
    """
    print("开始加载CSV回收配置...")
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    equipment_list = []
    rewards_dict = {}
    
    try:
        if os.path.exists(csv_file_path):
            # Python 2.7兼容的编码处理
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
            
            for encoding in encodings:
                try:
                    # Python 2.7兼容的文件打开方式
                    if sys.version_info[0] < 3:
                        # Python 2.7
                        with open(csv_file_path, 'rb') as file:
                            content = file.read()
                            # 尝试解码
                            try:
                                decoded_content = content.decode(encoding)
                            except UnicodeDecodeError:
                                continue
                            
                            # 手动解析CSV
                            lines = decoded_content.split('\n')
                            if len(lines) < 2:
                                continue
                                
                            # 跳过标题行
                            for line in lines[1:]:
                                line = line.strip()
                                if not line:
                                    continue
                                    
                                parts = line.split(',')
                                if len(parts) >= 2:
                                    equipment_name = parts[0].strip().strip('"')
                                    try:
                                        gold_amount = int(parts[1].strip().strip('"'))
                                        equipment_type = parts[2].strip().strip('"') if len(parts) > 2 else ''
                                        
                                        if equipment_name and gold_amount > 0:
                                            equipment_list.append(equipment_name)
                                            rewards_dict[equipment_name] = {
                                                "gold": gold_amount,
                                                "type": equipment_type
                                            }
                                    except ValueError:
                                        continue
                    else:
                        # Python 3+
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
                    
                    print("成功从CSV文件加载回收配置: {} 个装备 (编码: {})".format(len(equipment_list), encoding))
                    return equipment_list, rewards_dict
                    
                except Exception as e:
                    print("使用 {} 编码读取失败: {}".format(encoding, e))
                    continue
            
            print("无法读取CSV文件，尝试了所有编码")
            return [], {}
        else:
            print("CSV文件不存在: {}".format(csv_file_path))
            return [], {}
            
    except Exception as e:
        print("读取CSV文件时出错: {}".format(e))
        return [], {}

if __name__ == "__main__":
    print("=== 测试CSV加载 - 简化版 ===")
    print("Python版本: {}".format(sys.version))
    
    # 加载配置
    RECYCLE_EQUIPMENT, RECYCLE_REWARDS = load_recycle_config_from_csv()
    
    print("加载结果:")
    print("- 装备列表长度: {}".format(len(RECYCLE_EQUIPMENT)))
    print("- 奖励字典长度: {}".format(len(RECYCLE_REWARDS)))
    
    # 显示前5个装备
    print("\n前5个装备:")
    for i, equipment in enumerate(RECYCLE_EQUIPMENT[:5]):
        reward = RECYCLE_REWARDS[equipment]
        print("  {}. {} - {}金币 ({})".format(i+1, equipment, reward['gold'], reward['type']))
    
    print("\n=== 测试完成 ===") 