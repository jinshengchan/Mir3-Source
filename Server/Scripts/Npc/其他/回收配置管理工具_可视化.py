# -*- coding: utf-8 -*-
"""
装备回收配置管理工具 - 可视化版本
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
    print("          装备回收配置管理工具 - 可视化版本")
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

def wait_for_enter():
    """等待用户按回车键"""
    input("\n按回车键继续...")

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
        equipment_list = []
        rewards_dict = {}
        
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
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            equipment_count = 0
            total_gold = 0
            errors = []
            
            for row_num, row in enumerate(reader, start=2):
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

def add_equipment_to_csv():
    """
    向CSV文件添加新装备
    """
    print_info("正在添加新装备...")
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    try:
        # 获取用户输入
        equipment_name = input("请输入装备名称: ").strip()
        if not equipment_name:
            print_error("装备名称不能为空")
            return False
        
        gold_str = input("请输入回收价格: ").strip()
        try:
            gold_amount = int(gold_str)
            if gold_amount < 0:
                print_error("回收价格不能为负数")
                return False
        except ValueError:
            print_error("回收价格必须是整数")
            return False
        
        equipment_type = input("请输入装备类型 (可选，直接回车跳过): ").strip()
        
        # 检查装备是否已存在
        existing_equipment = set()
        if os.path.exists(csv_file_path):
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_equipment.add(row['装备名称'].strip())
        
        if equipment_name in existing_equipment:
            print_error("装备 '{}' 已存在于配置中".format(equipment_name))
            return False
        
        # 添加新装备
        with open(csv_file_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([equipment_name, gold_amount, equipment_type])
        
        print_success("成功添加装备: {} (回收价格: {} 金币, 类型: {})".format(
            equipment_name, gold_amount, equipment_type or '未设置'
        ))
        return True
        
    except Exception as e:
        print_error("添加装备时出错: {}".format(e))
        return False

def remove_equipment_from_csv():
    """
    从CSV文件中移除装备
    """
    print_info("正在移除装备...")
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    if not os.path.exists(csv_file_path):
        print_error("CSV文件不存在: {}".format(csv_file_path))
        return False
    
    try:
        equipment_name = input("请输入要移除的装备名称: ").strip()
        if not equipment_name:
            print_error("装备名称不能为空")
            return False
        
        # 读取现有数据
        rows = []
        found = False
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            
            for row in reader:
                if row['装备名称'].strip() == equipment_name:
                    found = True
                    continue  # 跳过要删除的装备
                rows.append(row)
        
        if not found:
            print_error("未找到装备: {}".format(equipment_name))
            return False
        
        # 重新写入文件
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)
        
        print_success("成功移除装备: {}".format(equipment_name))
        return True
        
    except Exception as e:
        print_error("移除装备时出错: {}".format(e))
        return False

def update_equipment_price():
    """
    更新CSV文件中装备的回收价格和类型
    """
    print_info("正在更新装备...")
    
    csv_file_path = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    if not os.path.exists(csv_file_path):
        print_error("CSV文件不存在: {}".format(csv_file_path))
        return False
    
    try:
        equipment_name = input("请输入要更新的装备名称: ").strip()
        if not equipment_name:
            print_error("装备名称不能为空")
            return False
        
        new_gold_str = input("请输入新的回收价格: ").strip()
        try:
            new_gold_amount = int(new_gold_str)
            if new_gold_amount < 0:
                print_error("回收价格不能为负数")
                return False
        except ValueError:
            print_error("回收价格必须是整数")
            return False
        
        new_equipment_type = input("请输入新的装备类型 (可选，直接回车跳过): ").strip()
        if not new_equipment_type:
            new_equipment_type = None
        
        # 读取所有行
        rows = []
        found = False
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            
            for row in reader:
                if row['装备名称'].strip() == equipment_name:
                    row['回收价格'] = str(new_gold_amount)
                    if new_equipment_type is not None:
                        row['装备类型'] = new_equipment_type
                    found = True
                rows.append(row)
        
        if not found:
            print_error("未找到装备: {}".format(equipment_name))
            return False
        
        # 重新写入文件
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)
        
        type_info = ", 类型: {}".format(new_equipment_type) if new_equipment_type is not None else ""
        print_success("成功更新装备: {} -> {} 金币{}".format(equipment_name, new_gold_amount, type_info))
        return True
        
    except Exception as e:
        print_error("更新装备时出错: {}".format(e))
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
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            equipment_count = 0
            total_gold = 0
            type_stats = {}
            
            for row in reader:
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

def show_main_menu():
    """
    显示主菜单
    """
    print_header()
    print("请选择要执行的操作:")
    print()
    print("1. 生成CSV文件 (从Python配置)")
    print("2. 生成Python文件 (从CSV配置)")
    print("3. 验证CSV文件")
    print("4. 添加新装备")
    print("5. 移除装备")
    print("6. 更新装备")
    print("7. 查看CSV文件信息")
    print("8. 退出程序")
    print()
    
    choice = input("请输入选项 (1-8): ").strip()
    return choice

def main():
    """
    主函数
    """
    while True:
        try:
            choice = show_main_menu()
            
            if choice == '1':
                print()
                generate_csv_from_python_config()
                wait_for_enter()
                
            elif choice == '2':
                print()
                generate_python_from_csv_config()
                wait_for_enter()
                
            elif choice == '3':
                print()
                validate_csv_config()
                wait_for_enter()
                
            elif choice == '4':
                print()
                add_equipment_to_csv()
                wait_for_enter()
                
            elif choice == '5':
                print()
                remove_equipment_from_csv()
                wait_for_enter()
                
            elif choice == '6':
                print()
                update_equipment_price()
                wait_for_enter()
                
            elif choice == '7':
                print()
                show_csv_info()
                wait_for_enter()
                
            elif choice == '8':
                print()
                print_info("感谢使用装备回收配置管理工具！")
                print_info("程序将在3秒后退出...")
                time.sleep(3)
                break
                
            else:
                print()
                print_warning("无效选项，请重新选择")
                wait_for_enter()
                
        except KeyboardInterrupt:
            print()
            print_info("程序被用户中断")
            break
        except Exception as e:
            print()
            print_error("程序运行出错: {}".format(e))
            wait_for_enter()

if __name__ == "__main__":
    main() 