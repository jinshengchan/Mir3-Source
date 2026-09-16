# -*- coding: utf-8 -*-
"""
测试Python 2.7兼容性
"""

import sys
import os
import csv

print("=== Python兼容性测试 ===")
print("Python版本: {}".format(sys.version))
print("当前工作目录: {}".format(os.getcwd()))

# 测试CSV读取
try:
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    print("CSV文件路径: {}".format(csv_file_path))
    
    if os.path.exists(csv_file_path):
        print("CSV文件存在")
        
        # 测试读取
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                count += 1
                if count <= 3:  # 只显示前3行
                    print("第{}行: {} - {}金币".format(count, row['装备名称'], row['回收价格']))
            
            print("总共读取了 {} 行数据".format(count))
    else:
        print("CSV文件不存在")
        
except Exception as e:
    print("测试失败: {}".format(e))

print("=== 测试完成 ===") 