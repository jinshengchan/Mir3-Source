# -*- coding: utf-8 -*-
"""
测试物品名称是否存在
"""

import sys
sys.path.append('Scripts/Utils')
from SimpleItemHelper import GetItemInfo, GetItemImageTag
from Globals import *

def test_item_names():
    """
    测试不同的物品名称
    """
    # 可能的物品名称列表
    test_names = [
        "屠龙", "屠龙刀", "屠龙剑",
        "Slaying", "Dragon Slayer", "DragonSlayer",
        "TuLong", "tulong", "TULONG",
        "屠龙武器", "屠龙兵器"
    ]
    
    print("=== 测试物品名称 ===")
    
    found_items = []
    
    for name in test_names:
        item_info = GetItemInfo(name)
        if item_info is not None:
            print("找到物品: {} -> ItemName: {}, Image: {}".format(name, item_info.ItemName, item_info.Image))
            found_items.append(name)
        else:
            print("未找到物品: {}".format(name))
    
    print("\n=== 找到的物品列表 ===")
    for item in found_items:
        print("- {}".format(item))
        img_tag = GetItemImageTag(item)
        print("  图像标签: {}".format(img_tag))
    
    if not found_items:
        print("没有找到任何物品！")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_item_names()