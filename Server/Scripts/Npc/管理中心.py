# -*- coding: utf-8 -*-
#载入模块SYS
import sys
import datetime
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import Server
import NpcEvent
import collections
import Server.Envir.SEnvir as SEnvir
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
import random
from Player.泡点 import *
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import Npc.鉴定稀世装备 as EquipmentIdentification
import Npc.兑换鉴定石 as IdentificationStoneExchange
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

# =============================================================================
# 定义商品配置字典
# =============================================================================
MERCHANT_CONFIG = {   
    # 特色称号配置
    'special_titles': {
        81: {'name': '幽灵船长', 'buff_id': 122, 'global_var': 'GV_PLAYER_BUFF1', 'description': '强元素雷+1，强元素暗黑+1，生命值+1%'},
        82: {'name': '诺玛苦僧', 'buff_id': 123, 'global_var': 'GV_PLAYER_BUFF2', 'description': '灵魂0-2，自然0-2，破坏0-3'},
        83: {'name': '撸牛博士', 'buff_id': 124, 'global_var': 'GV_PLAYER_BUFF3', 'description': '经验加成+10，背包负重+300'},
        84: {'name': '黑度烧客', 'buff_id': 125, 'global_var': 'GV_PLAYER_BUFF4', 'description': '攻击元素火+2，经验加成+20%，火墙伤害+10%'},
        85: {'name': '祖玛阁主', 'buff_id': 126, 'global_var': 'GV_PLAYER_BUFF5', 'description': '生命值+2%，暴击几率+1%，魔法躲避+1%'},
        86: {'name': '矿洞猎手', 'buff_id': 127, 'global_var': 'GV_PLAYER_BUFF6', 'description': '采矿成功率+50%'},
        87: {'name': '动物园长', 'buff_id': 128, 'global_var': 'GV_PLAYER_BUFF7', 'description': '宠物背包+10格，宠物负重+200'},
        801: {'name': '战天斗地', 'buff_id': 129, 'global_var': 'GV_PLAYER_BUFF8', 'class_required': 'Warrior', 'description': '破坏2-5，攻击速度+1'},
        802: {'name': '道骨仙风', 'buff_id': 130, 'global_var': 'GV_PLAYER_BUFF9', 'class_required': 'Taoist', 'description': '灵魂0-5，物防0-5，魔防0-5'},
        803: {'name': '法海无边', 'buff_id': 131, 'global_var': 'GV_PLAYER_BUFF10', 'class_required': 'Wizard', 'description': '自然0-5，生命+100，回蓝+20%'},
        804: {'name': '傲视群雄', 'buff_id': 133, 'global_var': 'GV_PLAYER_BUFF11', 'level_required': 60, 'description': '攻击速度+2，生命值+2%，暴击几率+2%，暴击伤害+2%，全系列魔法0-5，破坏0-2'}
    },   
}


def handle_special_title_purchase(sender, title_id):
    """处理特色称号购买"""
    try:
        title_config = MERCHANT_CONFIG['special_titles'][title_id]
    except KeyError:
        return "未知的称号ID。\n\n[返回主菜单:999]"
    
    # 检查职业要求
    if 'class_required' in title_config:
        if title_config['class_required'] == 'Warrior':
            if sender.Class != sender.Class.Warrior:
                return "你不是战士，无法购买。\n\n[返回主菜单:999]"
        elif title_config['class_required'] == 'Wizard':
            if sender.Class != sender.Class.Wizard:
                return "你不是法师，无法购买。\n\n[返回主菜单:999]"
        elif title_config['class_required'] == 'Taoist':
            if sender.Class != sender.Class.Taoist:
                return "你不是道士，无法购买。\n\n[返回主菜单:999]"
    
    # 检查等级要求
    if 'level_required' in title_config:
        if sender.Level < title_config['level_required']:
            return "你等级没有达到" + str(title_config['level_required']) + "级，无法购买。\n\n[返回主菜单:999]"
    
    if sender.Gold < 2880000:
        return "金币不足，无法购买。\n\n[返回主菜单:999]"
    
    if PlayerGetV(sender, GV_PLAYER_BUFFCOUNT) > 0:
        return "你已经购买过BUFF，无法重复购买。\n\n[返回主菜单:999]"
    
    # 获取全局变量ID
    if title_config['global_var'] == 'GV_PLAYER_BUFF1':
        global_var_id = GV_PLAYER_BUFF1
    elif title_config['global_var'] == 'GV_PLAYER_BUFF2':
        global_var_id = GV_PLAYER_BUFF2
    elif title_config['global_var'] == 'GV_PLAYER_BUFF3':
        global_var_id = GV_PLAYER_BUFF3
    elif title_config['global_var'] == 'GV_PLAYER_BUFF4':
        global_var_id = GV_PLAYER_BUFF4
    elif title_config['global_var'] == 'GV_PLAYER_BUFF5':
        global_var_id = GV_PLAYER_BUFF5
    elif title_config['global_var'] == 'GV_PLAYER_BUFF6':
        global_var_id = GV_PLAYER_BUFF6
    elif title_config['global_var'] == 'GV_PLAYER_BUFF7':
        global_var_id = GV_PLAYER_BUFF7
    elif title_config['global_var'] == 'GV_PLAYER_BUFF8':
        global_var_id = GV_PLAYER_BUFF8
    elif title_config['global_var'] == 'GV_PLAYER_BUFF9':
        global_var_id = GV_PLAYER_BUFF9
    elif title_config['global_var'] == 'GV_PLAYER_BUFF10':
        global_var_id = GV_PLAYER_BUFF10
    elif title_config['global_var'] == 'GV_PLAYER_BUFF11':
        global_var_id = GV_PLAYER_BUFF11
    else:
        return "未知的全局变量ID。\n\n[返回主菜单:999]"
    
    if GlobalGetV(global_var_id) > 0:
        return "你来晚一步，当前BUFF已被购买。\n\n[返回主菜单:999]"
    
    SubGold(sender, 2880000)
    sender.CustomBuffAdd(title_config['buff_id'])
    PlayerSetV(sender, GV_PLAYER_BUFFCOUNT, 1)
    GlobalSetV(global_var_id, 1)
    return "恭喜你购买成功，获得特色称号。\n\n[返回主菜单:999]"


def handle_special_title_remove(sender):
    """处理特色称号删除"""
    # 检查是否有buff
    #if PlayerGetV(sender, GV_PLAYER_BUFFCOUNT) == 0:
    #    return "你没有特色称号，无法删除。\n\n[返回主菜单:999]"
    
    # 遍历所有可能的buff_id，找到当前玩家拥有的buff
    current_buff_id = None
    current_global_var_id = None
    
    for title_id, title_config in MERCHANT_CONFIG['special_titles'].items():
        # 获取对应的全局变量ID
        if title_config['global_var'] == 'GV_PLAYER_BUFF1':
            global_var_id = GV_PLAYER_BUFF1
        elif title_config['global_var'] == 'GV_PLAYER_BUFF2':
            global_var_id = GV_PLAYER_BUFF2
        elif title_config['global_var'] == 'GV_PLAYER_BUFF3':
            global_var_id = GV_PLAYER_BUFF3
        elif title_config['global_var'] == 'GV_PLAYER_BUFF4':
            global_var_id = GV_PLAYER_BUFF4
        elif title_config['global_var'] == 'GV_PLAYER_BUFF5':
            global_var_id = GV_PLAYER_BUFF5
        elif title_config['global_var'] == 'GV_PLAYER_BUFF6':
            global_var_id = GV_PLAYER_BUFF6
        elif title_config['global_var'] == 'GV_PLAYER_BUFF7':
            global_var_id = GV_PLAYER_BUFF7
        elif title_config['global_var'] == 'GV_PLAYER_BUFF8':
            global_var_id = GV_PLAYER_BUFF8
        elif title_config['global_var'] == 'GV_PLAYER_BUFF9':
            global_var_id = GV_PLAYER_BUFF9
        elif title_config['global_var'] == 'GV_PLAYER_BUFF10':
            global_var_id = GV_PLAYER_BUFF10
        elif title_config['global_var'] == 'GV_PLAYER_BUFF11':
            global_var_id = GV_PLAYER_BUFF11
        else:
            continue
        
        # 检查是否是当前玩家购买的buff
        if GlobalGetV(global_var_id) > 0:
            current_buff_id = title_config['buff_id']
            current_global_var_id = global_var_id
            break
    
    if current_buff_id is None:
        return "未找到你的特色称号信息。\n\n[返回主菜单:999]"
    
    # 删除buff
    sender.CustomBuffRemove(current_buff_id)
    PlayerSetV(sender, GV_PLAYER_BUFFCOUNT, 0)
    GlobalSetV(current_global_var_id, 0)
    
    return "特色称号删除成功。\n\n[返回主菜单:999]"





def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	say="OK"
	Dict={}
	
	if (Menu == 1):
		return Npc.声望称号.OnClick([Self, Sender, 0, 6000])
	elif Menu in (6001, 6002, 6003):
		return Npc.声望称号.OnClick([Self, Sender, Menu, 6000])
	elif (Menu == 2):
		NPCObject = ServerUtils.GetNPCObject(4478)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.每日领取.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""

	elif (Menu == 51):
		StartPaoDian(Sender)
		if (Sender.Level < 22):
			say = """已经开始自动泡点。
			
			[关闭:0]"""
		else:
			say = """已经开始自动泡点，请勿离开安全区范围。
			
			[关闭:0]"""
	elif (Menu == 52):
		StopPaoDian(Sender)
		say = """你已经结束自动泡点。
		
		[关闭:0]"""


	elif (Menu == 4):
		if Sender.Class == Sender.Class.Wizard:
			say = """<font color=\"0xffffff00\">1、</font>杀死诺玛遗址的怪物会被累积
			<font color=\"0xffffff00\">2、</font>达到一定的数量加遗物可以兑换高级技能书籍
			<font color=\"0xffffff00\">3、你目前累积杀死诺玛遗址的怪物数量为：</font>{NMGWJS} <font color=\"0xff00ff00\">个</font>
			<font color=\"0xffffff00\">4、兑换书籍后会扣除对应的怪物累积数量</font>
			<font color=\"0xffffff00\">5、您可以兑换以下高级技能书籍（秘籍）：</font>
			
			<font color=\"0xff00ccff\">1000个诺玛怪物+1000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「十方斩」</font>   <font color=\"0xff00ff00\">「魄冰刺」</font>   <font color=\"0xff00ff00\">「灵魂分裂」</font>   <font color=\"0xff00ff00\">「鹰击」</font>  
			
			<font color=\"0xff00ccff\">2000个诺玛怪物+2000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「乾坤大挪移」</font><font color=\"0xff00ff00\">「怒神霹雳」</font> <font color=\"0xff00ff00\">「移花接玉」</font><font color=\"0xff00ff00\">「风之守护」</font>
			
			<font color=\"0xff00ccff\">3000个诺玛怪物+3000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「铁布衫」</font>  <font color=\"0xff00ff00\">「焰天火雨」</font>  <font color=\"0xff00ff00\">「 妙影无踪」</font> <font color=\"0xff00ff00\">「狂涛涌泉」</font>
			
			<font color=\"0xffFF00CC\">4000个诺玛怪物+2000个磨光片 兑换:</font>

			<font color=\"0xff00ff00\">「破血狂杀」</font>  <font color=\"0xff00ff00\">「凝血离魂」</font> <font color=\"0xff00ff00\">「阴阳法环」</font> <font color=\"0xff00ff00\">「最后抵抗」</font>


			[［魄冰刺］:211] [［怒神霹雳］:212] [［焰天火雨］:213] [［凝血离魂］:214]
			
			""".format(NMGWJS = PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT))
		elif Sender.Class == Sender.Class.Taoist:
			say = """<font color=\"0xffffff00\">1、</font>杀死诺玛遗址的怪物会被累积
			<font color=\"0xffffff00\">2、</font>达到一定的数量加遗物可以兑换高级技能书籍
			<font color=\"0xffffff00\">3、你目前累积杀死诺玛遗址的怪物数量为：</font>{NMGWJS} <font color=\"0xff00ff00\">个</font>
			<font color=\"0xffffff00\">4、兑换书籍后会扣除对应的怪物累积数量</font>
			<font color=\"0xffffff00\">5、您可以兑换以下高级技能书籍（秘籍）：</font>
			
			<font color=\"0xff00ccff\">1000个诺玛怪物+1000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「十方斩」</font>   <font color=\"0xff00ff00\">「魄冰刺」</font>   <font color=\"0xff00ff00\">「灵魂分裂」</font>   <font color=\"0xff00ff00\">「鹰击」</font>  
			
			<font color=\"0xff00ccff\">2000个诺玛怪物+2000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「乾坤大挪移」</font><font color=\"0xff00ff00\">「怒神霹雳」</font> <font color=\"0xff00ff00\">「移花接玉」</font><font color=\"0xff00ff00\">「风之守护」</font>
			
			<font color=\"0xff00ccff\">3000个诺玛怪物+3000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「铁布衫」</font>  <font color=\"0xff00ff00\">「焰天火雨」</font>  <font color=\"0xff00ff00\">「 妙影无踪」</font> <font color=\"0xff00ff00\">「狂涛涌泉」</font>
			
			<font color=\"0xffFF00CC\">4000个诺玛怪物+2000个磨光片 兑换:</font>

			<font color=\"0xff00ff00\">「破血狂杀」</font>  <font color=\"0xff00ff00\">「凝血离魂」</font> <font color=\"0xff00ff00\">「阴阳法环」</font> <font color=\"0xff00ff00\">「最后抵抗」</font>
			

			[［灵魂分裂］:311] [［移花接玉］:312] [［妙影无踪］:314] [［阴阳法环］:313]
			
			""".format(NMGWJS = PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT))
		elif Sender.Class == Sender.Class.Assassin:
			say = """<font color=\"0xffffff00\">1、</font>杀死诺玛遗址的怪物会被累积
			<font color=\"0xffffff00\">2、</font>达到一定的数量加遗物可以兑换高级技能书籍
			<font color=\"0xffffff00\">3、你目前累积杀死诺玛遗址的怪物数量为：</font>{NMGWJS} <font color=\"0xff00ff00\">个</font>
			<font color=\"0xffffff00\">4、兑换书籍后会扣除对应的怪物累积数量</font>
			<font color=\"0xffffff00\">5、您可以兑换以下高级技能书籍（秘籍）：</font>
			
			<font color=\"0xff00ccff\">1000个诺玛怪物+1000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「十方斩」</font>   <font color=\"0xff00ff00\">「魄冰刺」</font>   <font color=\"0xff00ff00\">「灵魂分裂」</font>   <font color=\"0xff00ff00\">「鹰击」</font>  
			
			<font color=\"0xff00ccff\">2000个诺玛怪物+2000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「乾坤大挪移」</font><font color=\"0xff00ff00\">「怒神霹雳」</font> <font color=\"0xff00ff00\">「移花接玉」</font><font color=\"0xff00ff00\">「风之守护」</font>
			
			<font color=\"0xff00ccff\">3000个诺玛怪物+3000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「铁布衫」</font>  <font color=\"0xff00ff00\">「焰天火雨」</font>  <font color=\"0xff00ff00\">「 妙影无踪」</font> <font color=\"0xff00ff00\">「狂涛涌泉」</font>
			
			<font color=\"0xffFF00CC\">4000个诺玛怪物+2000个磨光片 兑换:</font>

			<font color=\"0xff00ff00\">「破血狂杀」</font>  <font color=\"0xff00ff00\">「凝血离魂」</font> <font color=\"0xff00ff00\">「阴阳法环」</font> <font color=\"0xff00ff00\">「最后抵抗」</font>

			
			[［鹰击］:411] [［狂涛涌泉］:413] [［风之守护］:412] [［最后抵抗］:414]
			
			""".format(NMGWJS = PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT))			
		else:
			say = """<font color=\"0xffffff00\">1、</font>杀死诺玛遗址的怪物会被累积
			<font color=\"0xffffff00\">2、</font>达到一定的数量加遗物可以兑换高级技能书籍
			<font color=\"0xffffff00\">3、你目前累积杀死诺玛遗址的怪物数量为：</font>{NMGWJS} <font color=\"0xff00ff00\">个</font>
			<font color=\"0xffffff00\">4、兑换书籍后会扣除对应的怪物累积数量</font>
			<font color=\"0xffffff00\">5、您可以兑换以下高级技能书籍（秘籍）：</font>
			
			<font color=\"0xff00ccff\">1000个诺玛怪物+1000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「十方斩」</font>   <font color=\"0xff00ff00\">「魄冰刺」</font>   <font color=\"0xff00ff00\">「灵魂分裂」</font>   <font color=\"0xff00ff00\">「鹰击」</font>  
			
			<font color=\"0xff00ccff\">2000个诺玛怪物+2000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「乾坤大挪移」</font><font color=\"0xff00ff00\">「怒神霹雳」</font> <font color=\"0xff00ff00\">「移花接玉」</font><font color=\"0xff00ff00\">「风之守护」</font>
			
			<font color=\"0xff00ccff\">3000个诺玛怪物+3000个遗物 兑换:</font>

			<font color=\"0xff00ff00\">「铁布衫」</font>  <font color=\"0xff00ff00\">「焰天火雨」</font>  <font color=\"0xff00ff00\">「 妙影无踪」</font> <font color=\"0xff00ff00\">「狂涛涌泉」</font>
			
			<font color=\"0xffFF00CC\">4000个诺玛怪物+2000个磨光片 兑换:</font>

			<font color=\"0xff00ff00\">「破血狂杀」</font>  <font color=\"0xff00ff00\">「凝血离魂」</font> <font color=\"0xff00ff00\">「阴阳法环」</font> <font color=\"0xff00ff00\">「最后抵抗」</font>
			

			[［十方斩］:111] [［乾坤大挪移］:112] [［铁布衫］:113] [［破血狂杀］:114]
			
			""".format(NMGWJS = PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT))
	elif Menu in []:
           say = handle_nuoma_book_purchase(Sender, Menu)
    
    # =============================================================================
    # 特色称号系统
    # =============================================================================		
	elif (Menu == 5):
           say = """这里有各类特色称号，需要288万金币购买一个，
单BUFF只能单玩家获得，时效一星期。

<font color="0xff00ff00">称号属性介绍：</font>

幽灵船长：<font color="0xff00ff00">强元素雷+1，强元素暗黑+1，生命值+1%</font>
诺玛苦僧：<font color="0xff00ff00">灵魂0-2，自然0-2，破坏0-3</font>
撸牛博士：<font color="0xff00ff00">经验加成+10，背包负重+300</font>
黑度烧客：<font color="0xff00ff00">攻击元素火+2，经验加成+20%，火墙伤害+10%</font>
祖玛阁主：<font color="0xff00ff00">生命值+2%，暴击几率+1%，魔法躲避+1%</font>
矿洞猎手：<font color="0xff00ff00">采矿成功率+50%</font>
动物园长：<font color="0xff00ff00">宠物背包+10格，宠物负重+200</font>
战天斗地：<font color="0xff00ff00">破坏2-5，攻速+1</font>
道骨仙风：<font color="0xff00ff00">灵魂0-5，物防0-5，魔防0-5</font>
法海无边：<font color="0xff00ff00">自然0-5，生命+100，回蓝+20%</font>
傲视群雄：<font color="0xff00ff00">攻速+2，生命值+2%，暴击几率+2%，暴击伤害+2%，全系列魔法0-5，破坏0-2</font>

[幽灵船长:81]    [诺玛苦僧:82]    [撸牛博士:83]    [黑度烧客:84]
[祖玛阁主:85]    [矿洞猎手:86]    [动物园长:87]

[战天斗地（战士专用）:801]    [道骨仙风（道士专用）:802]
[法海无边（法师专用）:803]    [傲视群雄（60级专用）:804]

[删除特色称号:805]"""
			
        elif Menu in MERCHANT_CONFIG['special_titles']:
            say = handle_special_title_purchase(Sender, Menu)
    
        elif Menu == 805:
            say = handle_special_title_remove(Sender)			
			
	elif (Menu == 111):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 1000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
					
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 1000):
			say = """你的道具数量不足，请继续努力。			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 1000)
			Sender.TakeItem("遗物",1000)
			Sender.GiveItem("十方斩（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 112):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 2000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 2000)
			Sender.TakeItem("遗物",2000)
			Sender.GiveItem("乾坤大挪移（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 113):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 3000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 3000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 3000)
			Sender.TakeItem("遗物",3000)
			Sender.GiveItem("铁布衫（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 114):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 4000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("魔光片") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 4000)
			Sender.TakeItem("魔光片",2000)
			Sender.GiveItem("破血狂杀（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""

	elif (Menu == 115):
#判断需要的金币	
		if (Sender.Gold < 100000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("魔光片") < 4000):
			say ="""你没有足够的材料。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,100000000)
			Sender.TakeItem("魔光片",4000)
			Sender.GiveItem("君临步（秘籍）",1)
			say = """恭喜你兑换成功。

			[离开:0]"""

	elif (Menu == 211):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 1000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 1000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 1000)
			Sender.TakeItem("遗物",1000)
			Sender.GiveItem("魄冰刺（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 212):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 2000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 2000)
			Sender.TakeItem("遗物",2000)
			Sender.GiveItem("怒神霹雳（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 213):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 3000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 3000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 3000)
			Sender.TakeItem("遗物",3000)
			Sender.GiveItem("焰天火雨（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 214):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 4000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("魔光片") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 4000)
			Sender.TakeItem("魔光片",2000)
			Sender.GiveItem("凝血离魂（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 215):
#判断需要的金币	
		if (Sender.Gold < 100000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("魔光片") < 4000):
			say ="""你没有足够的材料。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,100000000)
			Sender.TakeItem("魔光片",4000)
			Sender.GiveItem("旋风墙",1)
			say = """恭喜你兑换成功。

			[离开:0]"""

	elif (Menu == 311):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 1000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 1000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 1000)
			Sender.TakeItem("遗物",1000)
			Sender.GiveItem("灵魂分裂（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 312):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 2000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 2000)
			Sender.TakeItem("遗物",2000)
			Sender.GiveItem("移花接玉（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 313):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 4000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("魔光片") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 4000)
			Sender.TakeItem("魔光片",2000)
			Sender.GiveItem("阴阳法环（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 314):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 3000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 3000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 3000)
			Sender.TakeItem("遗物",3000)
			Sender.GiveItem("妙影无踪（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""



	elif (Menu == 315):
#判断需要的金币	
		if (Sender.Gold < 100000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("魔光片") < 4000):
			say ="""你没有足够的材料。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,100000000)
			Sender.TakeItem("魔光片",4000)
			Sender.GiveItem("焰魔召唤术",1)
			say = """恭喜你兑换成功。

			[离开:0]"""

	elif (Menu == 411):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 1000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 1000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 1000)
			Sender.TakeItem("遗物",1000)
			Sender.GiveItem("鹰击（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 412):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 2000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 2000)
			Sender.TakeItem("遗物",2000)
			Sender.GiveItem("风之守护（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 413):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 3000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("遗物") < 3000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 3000)
			Sender.TakeItem("遗物",3000)
			Sender.GiveItem("狂涛涌泉（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 414):
		if (PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) < 4000):
			say = """你杀死的诺玛怪物数量不足，请继续努力。
			
		
			[离开:0]"""
		elif (Sender.GetItemCount("魔光片") < 2000):
			say = """你的道具数量不足，请继续努力。
			
		
			[离开:0]"""
		else:
			PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) - 4000)
			Sender.TakeItem("魔光片",2000)
			Sender.GiveItem("最后抵抗（秘籍）",1)
			say = """恭喜你兑换成功。
			
		
			[离开:0]"""
	elif (Menu == 15):
		NPCObject = ServerUtils.GetNPCObject(355)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.首饰熔炼.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 20):
		say = """<font color=\"0xff00ff00\">1元宝</font>       [兑换:201]     <font color=\"0xff00ff00\">太阳水x50</font>
		<font color=\"0xff00ff00\">5元宝</font>       [兑换:202]     <font color=\"0xff00ff00\">太阳水x250</font>
		<font color=\"0xff00ff00\">1元宝</font>       [兑换:203]     <font color=\"0xff00ff00\">强效太阳水x3</font>
		<font color=\"0xff00ff00\">10元宝</font>      [兑换:204]     <font color=\"0xff00ff00\">强效太阳水x30</font>
		<font color=\"0xff00ff00\">100元宝</font>     [兑换:205]     <font color=\"0xff00ff00\">万年雪霜x100</font>
		
		<font color=\"0xff00ff00\">50赏金</font>      [兑换:206]     <font color=\"0xff00ff00\">强效太阳水x1</font>
		<font color=\"0xff00ff00\">50赏金</font>      [兑换:207]     <font color=\"0xff00ff00\">万年雪霜x1</font>
		<font color=\"0xff00ff00\">100赏金</font>     [兑换:208]     <font color=\"0xff00ff00\">强效太阳水x2</font>
		<font color=\"0xff00ff00\">100赏金</font>     [兑换:209]     <font color=\"0xff00ff00\">万年雪霜x2</font>
		"""
	elif (Menu == 201):
		if (Sender.GameGold < 1):
			say= """你没有足够的金币，无法兑换

			[离开:0]"""
		else:
			SubGameGold(Sender,1)
			Sender.GiveItem("太阳水（绑定）",50)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 202):
		if (Sender.GameGold < 5):
			say= """你没有足够的金币，无法兑换

			[离开:0]"""
		else:
			SubGameGold(Sender,5)
			Sender.GiveItem("太阳水（绑定）",250)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 203):
		if (Sender.GameGold < 1):
			say= """你没有足够的金币，无法兑换

			[离开:0]"""
		else:
			SubGameGold(Sender,1)
			Sender.GiveItem("强效太阳水（绑定）",3)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 204):
		if (Sender.GameGold < 10):
			say= """你没有足够的金币，无法兑换

			[离开:0]"""
		else:
			SubGameGold(Sender,1)
			Sender.GiveItem("强效太阳水（绑定）",30)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 205):
		if (Sender.GameGold < 100):
			say= """你没有足够的金币，无法兑换

			[离开:0]"""
		else:
			SubGameGold(Sender,100)
			Sender.GiveItem("万年雪霜（绑定）",100)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 206):
		if (Sender.HuntGold < 50):
			say= """你没有足够的赏金，无法兑换

			[离开:0]"""
		else:
			SubHuntGold(Sender,50)
			Sender.GiveItem("强效太阳水（绑定）",1)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 207):
		if (Sender.HuntGold < 50):
			say= """你没有足够的赏金，无法兑换

			[离开:0]"""
		else:
			SubHuntGold(Sender,50)
			Sender.GiveItem("万年雪霜（绑定）",1)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 208):
		if (Sender.HuntGold < 100):
			say= """你没有足够的赏金，无法兑换

			[离开:0]"""
		else:
			SubHuntGold(Sender,100)
			Sender.GiveItem("强效太阳水（绑定）",2)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 209):
		if (Sender.HuntGold < 100):
			say= """你没有足够的赏金，无法兑换

			[离开:0]"""
		else:
			SubHuntGold(Sender,100)
			Sender.GiveItem("万年雪霜（绑定）",2)
			say="""兑换成功

			[继续购买药水:20]

			[离开:0]"""
	elif (Menu == 13):
		say = """兑换的书都是秘籍，需要花点小钱50W.
		
		夜明珠1000兑换→[十方斩:145]
		夜明珠1000兑换 →[移形换位:134]
		夜明珠1000兑换→[强魔震法:138]
			
		蚂蚁卵1000兑换→[阴阳法环:131]
		蚂蚁卵1000兑换→[焰天火雨:135]
		蚂蚁卵1000兑换→[回生术:139]

		号角1000兑换→[深渊:1000]
		号角1000兑换→[神机妙算:1001]
		号角1000兑换→[鬼灵步:1002]
		号角1000兑换→[残月之乱:1003]

		
		[关闭:0]"""
		#僵尸骨头1000兑换→[野蛮冲撞:132]
		#僵尸骨头1000兑换→[冰沙掌:133]
		#僵尸骨头1000兑换→[群体治愈术:136]
		#僵尸骨头1000兑换→[超强召唤骷髅:137]
		#僵尸骨头1000兑换→[翔空剑法:143]
		#僵尸骨头1000兑换→[召唤神兽:144]
	elif (Menu == 131):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("蚂蚁卵") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("阴阳法环（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("蚂蚁卵",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 132):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("僵尸骨头") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("野蛮冲撞（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("僵尸骨头",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 133):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("僵尸骨头") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("冰沙掌（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("僵尸骨头",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 134):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("夜明珠") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("移形换位（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("夜明珠",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 135):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("蚂蚁卵") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("焰天火雨（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("蚂蚁卵",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 136):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("僵尸骨头") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("群体治愈术（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("僵尸骨头",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 137):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("僵尸骨头") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("超强召唤骷髅（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("僵尸骨头",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 138):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("夜明珠") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("强魔震法（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("夜明珠",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 139):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("蚂蚁卵") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("回生术（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("蚂蚁卵",1000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 140):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("遗物") < 50):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("灵魂分裂（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("遗物",50)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 141):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("遗物") < 50):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("魄冰刺（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("遗物",50)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 142):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("遗物") < 50):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("十方斩（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("遗物",50)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 143):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("僵尸骨头") < 100):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("翔空剑法（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("僵尸骨头",10000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 144):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("僵尸骨头") < 100):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("召唤神兽（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("僵尸骨头",10000)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 145):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("夜明珠") < 1000):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("十方斩（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("夜明珠",100)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
	elif (Menu == 1000):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("号角") < 100):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("深渊（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("号角",100)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""        
	elif (Menu == 1001):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("号角") < 100):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("神机妙算（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("号角",100)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""  
	elif (Menu == 1002):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("号角") < 100):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("鬼灵步（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("号角",100)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""  
	elif (Menu == 1003):
		if (Sender.Gold < 100000):
			say = """你没有足够的金币，无法兑换

			[离开:0]"""
		elif(Sender.GetItemCount("号角") < 100):
			say ="""你的材料不足，请准备好足够的材料在来。

			[离开:0]"""
		else:
			if (Sender.GiveItem("残月之乱（秘籍）",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("号角",100)
				say ="""兑换秘籍成功。
			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""  



                

	elif (Menu == 25):
		NPCObject = ServerUtils.GetNPCObject(213)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.军衔进阶.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 27):
		NPCObject = ServerUtils.GetNPCObject(223)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.装备刻名.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 28):
		NPCObject = ServerUtils.GetNPCObject(143)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.潘夜岛.碎片阿翠.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 34):
		NPCObject = ServerUtils.GetNPCObject(225)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.道馆技能付费鉴定.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 29):
		NPCObject = ServerUtils.GetNPCObject(199)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.一键特修.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 35):
		NPCObject = ServerUtils.GetNPCObject(191)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.新手武器制炼石.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 36):
		NPCObject = ServerUtils.GetNPCObject(190)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.新手首饰冶炼石.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 37):            
		NPCObject = ServerUtils.GetNPCObject(352)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.双倍.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 38):
		NPCObject = ServerUtils.GetNPCObject(215)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return EquipmentIdentification.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 39):
		NPCObject = ServerUtils.GetNPCObject(216)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return IdentificationStoneExchange.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 30):
		NPCObject = ServerUtils.GetNPCObject(219)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.生锈首饰.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 300):
		NPCObject = ServerUtils.GetNPCObject(354)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.元宝回收.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""
	elif (Menu == 301):
		NPCObject = ServerUtils.GetNPCObject(66)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.泡点中.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""	
	elif (Menu == 302):
		NPCObject = ServerUtils.GetNPCObject(54)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.义贤.OnClick(newArgs)
		else:
			say = """未找到指定的NPC"""	
		
			
#主菜单
	else:
		say = """[碎片分解:28]              [材料换书:13]              [军衔进阶:25] 
		
		[元宝经验:2]      [付费鉴定:34]      [元宝回收:300]
 		
		[首饰熔炼:15]       [装备刻名:27]    [技能书兑换:4]
		
		[生锈首饰:30]        [声望称号:1]   [特色称号:5]  [每日双倍:37]  

		[装备鉴定:38]        [鉴定石分解:39]

		[一键特修:29]              [马店:302]               [在线泡点:301]  """

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Enums里的空类
types =[ItemType.Nothing]

def Refine(Sender,RefineName):
	requirements = REFINE_REQUIREMENTS[RefineName]

	if (Sender.Gold < requirements['Gold']):
			return """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
	if(requirements['Item']):
		for m,n in requirements['Item'].items():
			if (Sender.GetItemCount(m)<n):
				return """你的材料不足。
				请准备好足够的材料在来。

				[离开:0]"""
	if (requirements['Item']):
		for m,n in requirements['Item'].items():
			Sender.TakeItem(m,n)
		SubGold(Sender,requirements['Gold'])
		Sender.GiveItem(RefineName,1)
		return """祝贺你，锻造成功。

		[离开:0]"""


NpcEvent.add_listener(335,"OnClick",OnClick)
NpcEvent.add_listener(134,"OnClick",OnClick)

