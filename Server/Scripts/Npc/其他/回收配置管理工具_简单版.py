# -*- coding: utf-8 -*-
"""
装备回收配置管理工具 - 简单可视化版本
支持CSV和Python配置文件之间的相互转换
"""

import csv
import os
import sys
import time

# 导入回收配置
try:
    from 回收配置 import RECYCLE_EQUIPMENT, RECYCLE_REWARDS
except ImportError:
    print("无法导入回收配置，请确保回收配置.py文件存在")
    RECYCLE_EQUIPMENT = []
    RECYCLE_REWARDS = {}

def print_header():
    """打印工具标题"""
    print("=" * 60)
    print("          装备回收配置管理工具 - 简单版")
    print("=" * 60)
    print()

def print_success(message):
    """打印成功信息"""
    print("✅ {}".format(message))

def print_error(message):
    """打印错误信息"""
    print("❌ {}".format(message))

def print_info(message):
    """打印信息"""
    print("ℹ️  {}".format(message))

def print_warning(message):
    """打印警告信息"""
    print("⚠️  {}".format(message))

def read_csv_with_encoding(csv_file_path):
    """
    尝试多种编码读取CSV文件
    """
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(csv_file_path, 'r', encoding=encoding) as file:
                content = file.read()
                # 测试是否能正确解析
                file.seek(0)
                reader = csv.DictReader(file)
                rows = list(reader)
                if rows:
                    print_info("成功使用 {} 编码读取CSV文件".format(encoding))
                    return rows, encoding
        except Exception as e:
            continue
    
    print_error("无法读取CSV文件，尝试了所有编码: {}".format(encodings))
    return None, None

def generate_csv_from_python_config():
    """
    从Python配置生成CSV文件
    """
    print_info("正在从Python配置生成CSV文件...")
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    try:
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['装备名称', '回收价格', '装备类型'])
            
            for equipment, reward_info in RECYCLE_REWARDS.items():
                gold = reward_info.get('gold', 0)
                equipment_type = reward_info.get('type', '')
                writer.writerow([equipment, gold, equipment_type])
        
        print_success("成功生成CSV文件: {}".format(csv_file_path))
        print_success("共写入 {} 个装备配置".format(len(RECYCLE_EQUIPMENT)))
        
    except Exception as e:
        print_error("生成CSV文件时出错: {}".format(e))

def generate_python_from_csv_config():
    """
    从CSV文件生成Python配置文件
    """
    print_info("正在从CSV文件生成Python配置文件...")
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    python_file_path = os.path.join(os.path.dirname(__file__), "回收配置_从CSV生成.py")
    
    if not os.path.exists(csv_file_path):
        print_error("CSV文件不存在: {}".format(csv_file_path))
        return False
    
    try:
        # 使用多种编码尝试读取CSV文件
        rows, encoding = read_csv_with_encoding(csv_file_path)
        if not rows:
            return False
        
        equipment_list = []
        rewards_dict = {}
        
        for row in rows:
            equipment_name = row['装备名称'].strip()
            gold_amount = int(row['回收价格'])
            equipment_type = row.get('装备类型', '').strip()
            
            if equipment_name and gold_amount > 0:
                equipment_list.append(equipment_name)
                rewards_dict[equipment_name] = {
                    "gold": gold_amount,
                    "type": equipment_type
                }
        
        # 生成Python配置文件
        python_content = "# -*- coding: utf-8 -*-\n"
        python_content += '"""\n'
        python_content += "装备回收配置文件 - 从CSV生成\n"
        python_content += '"""\n\n'
        python_content += "# 装备回收配置\n"
        python_content += "RECYCLE_EQUIPMENT = [\n"
        
        # 添加装备列表
        for equipment in equipment_list:
            python_content += '    "{}",\n'.format(equipment)
        
        python_content += "]\n\n"
        python_content += "# 装备回收奖励配置\n"
        python_content += "RECYCLE_REWARDS = {\n"
        
        # 添加奖励配置
        for equipment, reward_info in rewards_dict.items():
            gold = reward_info.get('gold', 0)
            equipment_type = reward_info.get('type', '')
            python_content += '    "{}": {{"gold": {}, "type": "{}"}},\n'.format(
                equipment, gold, equipment_type
            )
        
        python_content += "}\n"
        
        # 写入Python文件
        with open(python_file_path, 'w', encoding='utf-8') as file:
            file.write(python_content)
        
        print_success("成功生成Python配置文件: {}".format(python_file_path))
        print_success("共处理 {} 个装备".format(len(equipment_list)))
        print_info("Python文件已保存为: 回收配置_从CSV生成.py")
        
        return True
        
    except Exception as e:
        print_error("生成Python配置文件时出错: {}".format(e))
        return False

def validate_csv_config():
    """
    验证CSV配置文件
    """
    print_info("正在验证CSV配置文件...")
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    if not os.path.exists(csv_file_path):
        print_error("CSV文件不存在: {}".format(csv_file_path))
        return False
    
    try:
        # 使用多种编码尝试读取CSV文件
        rows, encoding = read_csv_with_encoding(csv_file_path)
        if not rows:
            return False
        
        equipment_count = 0
        total_gold = 0
        errors = []
        
        for row_num, row in enumerate(rows, start=2):
            equipment_name = row.get('装备名称', '').strip()
            gold_str = row.get('回收价格', '').strip()
            equipment_type = row.get('装备类型', '').strip()
            
            if not equipment_name:
                errors.append("第{}行: 装备名称为空".format(row_num))
                continue
            
            try:
                gold = int(gold_str)
                if gold < 0:
                    errors.append("第{}行: 回收价格不能为负数 ({}: {})".format(row_num, equipment_name, gold))
                    continue
            except ValueError:
                errors.append("第{}行: 回收价格格式错误 ({}: {})".format(row_num, equipment_name, gold_str))
                continue
            
            equipment_count += 1
            total_gold += gold
        
        print_success("CSV文件验证完成:")
        print_info("- 装备数量: {}".format(equipment_count))
        print_info("- 总回收价值: {:,} 金币".format(total_gold))
        
        if errors:
            print_warning("- 发现 {} 个错误:".format(len(errors)))
            for error in errors:
                print("  {}".format(error))
            return False
        else:
            print_success("- 配置文件验证通过")
            return True
            
    except Exception as e:
        print_error("验证CSV文件时出错: {}".format(e))
        return False

def show_csv_info():
    """
    显示CSV文件信息
    """
    print_info("正在读取CSV文件信息...")
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    if not os.path.exists(csv_file_path):
        print_error("CSV文件不存在: {}".format(csv_file_path))
        return
    
    try:
        # 使用多种编码尝试读取CSV文件
        rows, encoding = read_csv_with_encoding(csv_file_path)
        if not rows:
            return
        
        equipment_count = 0
        total_gold = 0
        type_stats = {}
        
        for row in rows:
            equipment_name = row.get('装备名称', '').strip()
            gold_str = row.get('回收价格', '').strip()
            equipment_type = row.get('装备类型', '').strip()
            
            if equipment_name and gold_str:
                try:
                    gold = int(gold_str)
                    equipment_count += 1
                    total_gold += gold
                    
                    if equipment_type:
                        type_stats[equipment_type] = type_stats.get(equipment_type, 0) + 1
                    else:
                        type_stats['未分类'] = type_stats.get('未分类', 0) + 1
                except ValueError:
                    continue
        
        print_success("CSV文件信息:")
        print_info("- 装备总数: {}".format(equipment_count))
        print_info("- 总回收价值: {:,} 金币".format(total_gold))
        print_info("- 平均回收价格: {:,} 金币".format(total_gold // equipment_count if equipment_count > 0 else 0))
        
        if type_stats:
            print_info("- 装备类型分布:")
            for eq_type, count in sorted(type_stats.items()):
                print("    {}: {} 个".format(eq_type, count))
            
    except Exception as e:
        print_error("读取CSV文件信息时出错: {}".format(e))

def main():
    """
    主函数 - 执行所有操作并显示结果
    """
    print_header()
    
    print("正在执行所有操作...")
    print()
    
    # 1. 验证CSV文件
    print("=" * 40)
    print("1. 验证CSV文件")
    print("=" * 40)
    validate_csv_config()
    print()
    
    # 2. 显示CSV信息
    print("=" * 40)
    print("2. 显示CSV文件信息")
    print("=" * 40)
    show_csv_info()
    print()
    
    # 3. 生成CSV文件
    print("=" * 40)
    print("3. 生成CSV文件")
    print("=" * 40)
    generate_csv_from_python_config()
    print()
    
    # 4. 生成Python文件
    print("=" * 40)
    print("4. 生成Python文件")
    print("=" * 40)
    generate_python_from_csv_config()
    print()
    
    # 5. 最终验证
    print("=" * 40)
    print("5. 最终验证")
    print("=" * 40)
    validate_csv_config()
    print()
    
    print("=" * 60)
    print_success("所有操作完成！")
    print("=" * 60)
    
    # 等待3秒后退出
    print_info("程序将在3秒后退出...")
    time.sleep(3)

if __name__ == "__main__":
    main() 