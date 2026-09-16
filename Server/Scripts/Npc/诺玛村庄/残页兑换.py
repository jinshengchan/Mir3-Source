# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
from Npc.商店列表 import *
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

def OnClick(args):
    Self = args[0]
    Sender = args[1]
    Menu = args[2]
    Dict = {}
    say = ""
    
    # 红名判断
    if Sender.Stats[Stat.PKPoint] > 199:
        say = """我不愿意和你这样的人进行交易。
        [结束:0]"""
    
        # 主菜单
    elif Menu == 1:
        say = """
        请选择要兑换的技能书：

        [凝血离魂（1000残页+1000万金币）:11]
        [阴阳法环（1000残页+1000万金币）:12]
        [破血狂杀（1000残页+1000万金币）:13]
        [焰天火雨（1000残页+1000万金币）:14]
        [妙影无踪（1000残页+1000万金币）:15]
        [铁布衫（500残页+500万金币）:16]
        [怒神霹雳（500残页+500万金币）:17]
        [魄冰刺（500残页+500万金币）:18]
        [云寂术（500残页+500万金币）:19]
        [十方斩（500残页+500万金币）:20]
        [移花接玉（500残页+500万金币）:21]
        [斗转星移（500残页+500万金币）:22]
        [乾坤大挪移（500残页+500万金币）:23]"""
    
    # 处理1000残页的技能书菜单(11-15)
    elif Menu in (11, 12, 13, 14, 15):
        books = {
            11: ("凝血离魂", 1000, 10000000),
            12: ("阴阳法环", 1000, 10000000),
            13: ("破血狂杀", 1000, 10000000),
            14: ("焰天火雨", 1000, 10000000),
            15: ("妙影无踪", 1000, 10000000)
        }
        name, pages, gold = books[Menu]
        say = """
        兑换{0}需要{0}（残页）{1}个，金币{2}万。
        
        [确认兑换:{3}1] 
        
        [取消:0]""".format(name, pages, gold/10000, Menu)
    
    # 处理500残页的技能书菜单(16-23)
    elif Menu in (16, 17, 18, 19, 20, 21, 22, 23):
        books = {
            16: ("铁布衫", 500, 5000000),
            17: ("怒神霹雳", 500, 5000000),
            18: ("魄冰刺", 500, 5000000),
            19: ("云寂术", 500, 5000000),
            20: ("十方斩", 500, 5000000),
            21: ("移花接玉", 500, 5000000),
            22: ("斗转星移", 500, 5000000),
            23: ("乾坤大挪移", 500, 5000000)
        }
        name, pages, gold = books[Menu]
        say = """
        兑换{0}需要{0}（残页）{1}个，金币{2}万。

        [确认兑换:{3}1] 

        [取消:0]""".format(name, pages, gold/10000, Menu)
    
    # 处理1000残页的兑换确认(111-151)
    elif Menu in (111, 121, 131, 141, 151):
        base_menu = Menu / 10
        books = {
            11: ("凝血离魂", 1000, 10000000),
            12: ("阴阳法环", 1000, 10000000),
            13: ("破血狂杀", 1000, 10000000),
            14: ("焰天火雨", 1000, 10000000),
            15: ("妙影无踪", 1000, 10000000)
        }
        name, pages, gold = books[base_menu]
        item_name = "{0}（残页）".format(name)
        
        if Sender.Gold < gold:
            say = """
            
            你没有足够的金币（需要{0}万金币）。

            [返回:{1}] 
            
            [离开:0]""".format(gold/10000, base_menu)

        elif Sender.GetItemCount(item_name) < pages:
            say = """
            
            您的{0}不足（需要{1}个）。

            [返回:{2}] 
            
            [离开:0]""".format(item_name, pages, base_menu)
        else:
            Sender.TakeItem(item_name, pages)  
            SubGold(Sender, gold)             
            Sender.GiveItem(name, 1)          
            say = """
            恭喜您，{0}兑换成功！

            [继续兑换:1] 
            
            [离开:0]""".format(name)
    
    # 处理500残页的兑换确认(161-231)
    elif Menu in (161, 171, 181, 191, 201, 211, 221, 231):
        base_menu = Menu / 10
        books = {
            16: ("铁布衫", 500, 5000000),
            17: ("怒神霹雳", 500, 5000000),
            18: ("魄冰刺", 500, 5000000),
            19: ("云寂术", 500, 5000000),
            20: ("十方斩", 500, 5000000),
            21: ("移花接玉", 500, 5000000),
            22: ("斗转星移", 500, 5000000),
            23: ("乾坤大挪移", 500, 5000000)
        }
        name, pages, gold = books[base_menu]
        item_name = "{0}（残页）".format(name)
        
        if Sender.Gold < gold:
            say = """
            你没有足够的金币（需要{0}万金币）。

            [返回:{1}] 
            
            [离开:0]""".format(gold/10000, base_menu)
        elif Sender.GetItemCount(item_name) < pages:
            say = """
            
            您的{0}不足（需要{1}个）。

            [返回:{2}] 
            
            [离开:0]""".format(item_name, pages, base_menu)
        else:
            Sender.TakeItem(item_name, pages)
            SubGold(Sender, gold)
            Sender.GiveItem(name, 1)
            say = """
            
            恭喜您，{0}兑换成功！

            [继续兑换:1]
            
            [离开:0]""".format(name)
    
    # 默认菜单
    else:
        say = """
        欢迎来到技能书兑换商店！

        我可以帮你用残页兑换完整的技能书。

        [查看可兑换书籍:1]

        [离开:0]"""
    
    Dict['Say'] = say
    return Dict

NpcEvent.add_listener(380, "OnClick", OnClick)