# -*- coding: utf-8 -*-
"""
安全的CSV编辑器
避免编码问题，提供友好的编辑界面
"""

import csv
import os
import sys

def read_csv_safely(file_path):
    """
    安全读取CSV文件，尝试多种编码
    """
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'utf-16']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                # 验证内容是否正确
                if '装备名称' in content and '回收价格' in content:
                    print("成功使用 {} 编码读取文件".format(encoding))
                    return content, encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print("使用 {} 编码读取时出错: {}".format(encoding, e))
            continue
    
    raise Exception("无法使用任何编码读取文件")

def write_csv_safely(file_path, content):
    """
    安全写入CSV文件，确保UTF-8编码
    """
    try:
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            file.write(content)
        print("文件已安全保存为UTF-8编码")
    except Exception as e:
        print("保存文件时出错: {}".format(e))

def backup_csv():
    """
    备份当前CSV文件
    """
    csv_file = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    backup_file = os.path.join(os.path.dirname(__file__), "回收配置_backup.csv")
    
    try:
        content, encoding = read_csv_safely(csv_file)
        with open(backup_file, 'w', encoding='utf-8') as file:
            file.write(content)
        print("已备份到: {}".format(backup_file))
        return True
    except Exception as e:
        print("备份失败: {}".format(e))
        return False

def restore_csv():
    """
    从备份恢复CSV文件
    """
    csv_file = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    backup_file = os.path.join(os.path.dirname(__file__), "回收配置_backup.csv")
    
    if not os.path.exists(backup_file):
        print("备份文件不存在")
        return False
    
    try:
        content, encoding = read_csv_safely(backup_file)
        write_csv_safely(csv_file, content)
        print("已从备份恢复文件")
        return True
    except Exception as e:
        print("恢复失败: {}".format(e))
        return False

def show_csv_content():
    """
    显示CSV文件内容
    """
    csv_file = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    try:
        content, encoding = read_csv_safely(csv_file)
        print("\n=== CSV文件内容预览 ===")
        lines = content.split('\n')
        for i, line in enumerate(lines[:10]):  # 只显示前10行
            print("{:3d}: {}".format(i+1, line))
        if len(lines) > 10:
            print("... 还有 {} 行".format(len(lines)-10))
        print("=" * 30)
    except Exception as e:
        print("读取文件失败: {}".format(e))

def fix_csv_encoding():
    """
    修复CSV文件编码问题
    """
    csv_file = os.path.join(os.path.dirname(__file__), "回收配置.csv")
    
    try:
        # 尝试读取文件
        content, encoding = read_csv_safely(csv_file)
        
        # 检查是否有乱码
        if 'װ' in content or 'ռ۸' in content:
            print("检测到乱码，尝试修复...")
            
            # 尝试从备份恢复
            if restore_csv():
                print("已从备份恢复文件")
                return True
            else:
                print("备份恢复失败，尝试重新生成...")
                # 重新生成CSV文件
                from 回收配置管理工具 import generate_csv_from_python_config
                generate_csv_from_python_config()
                print("已重新生成CSV文件")
                return True
        else:
            print("文件编码正常")
            return True
            
    except Exception as e:
        print("修复编码时出错: {}".format(e))
        return False

def main():
    """
    主函数
    """
    print("=== CSV编辑器 ===")
    print("1. 显示文件内容")
    print("2. 备份当前文件")
    print("3. 从备份恢复")
    print("4. 修复编码问题")
    print("5. 退出")
    
    while True:
        try:
            choice = input("\n请选择操作 (1-5): ").strip()
            
            if choice == '1':
                show_csv_content()
            elif choice == '2':
                backup_csv()
            elif choice == '3':
                restore_csv()
            elif choice == '4':
                fix_csv_encoding()
            elif choice == '5':
                print("退出编辑器")
                break
            else:
                print("无效选择，请输入1-5")
                
        except KeyboardInterrupt:
            print("\n退出编辑器")
            break
        except Exception as e:
            print("操作失败: {}".format(e))

if __name__ == "__main__":
    main() 