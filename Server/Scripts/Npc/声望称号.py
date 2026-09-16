# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import clr

clr.AddReference("Library")
from Library import *
import collections
import NpcEvent

from Utils.PlayerUtils import *

#定义称号和需要的声望值
FAME_TITLES = [{'江湖初出': 200}, {'新进高手': 1000}, {'江湖侠客': 2000}, {'武林名宿': 4000}, {'仁义大侠': 6000}, 
{'善仁英雄': 10000}, {'尊扬义侠': 15000}, {'英雄豪杰': 20000}, {'武林至尊': 50000}]

######################################################
# 本函数为程序调用的固定格式 函数名和参数数量不要修改
# OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################

def findNextFameTitle(player, current_title):       #查找下一个称号
	if current_title == '无':
		return FAME_TITLES[0]

	i = 0
	for dic in FAME_TITLES:
		for name, price in dic.iteritems():
			if name == current_title:
				return FAME_TITLES[i+1] if i + 1 < len(FAME_TITLES) else None
		i = i + 1


def upgradeTitle(player):    #提升称号
	current_item = player.Equipment[EQUIPMENT_SLOTS['声望称号']] if check_item_equipped(player, '声望称号') else None
	current_title = current_item.Info.ItemName if current_item else '无'
	next_title_dict = findNextFameTitle(player, current_title)     #查询声望称号
	if next_title_dict is None:
		return False, '当前称号无法继续进阶，请联系管理员检查。'

	next_title_name = next_title_dict.keys()[0]         #查询称号名称
	next_title_price = next_title_dict[next_title_name]        #声望值
	if player.Prestige < next_title_price:
		return False, '你的声望不足，无法完成本次进阶。'

	if not any(item is None for item in player.Inventory):
		return False, '人物背包没有空位，请至少留出一个空位后再试。'

	deleteEquip(player, '声望称号')            #删除当前的声望称号
	createThenPutOnEquipment(player, next_title_name, '声望称号')    #给予升级的称号并自动装备到声望槽
	new_item = player.Equipment[EQUIPMENT_SLOTS['声望称号']]
	if new_item is None or new_item.Info.ItemName != next_title_name:
		if current_title != '无':
			createThenPutOnEquipment(player, current_title, '声望称号')
		return False, '称号创建失败，未扣除声望，请联系管理员检查物品数据。'

	player.Prestige = player.Prestige - next_title_price               #声望值剩余=当前声望减去升级需要的声望点
	return True, '称号升级成功，当前称号为（ {} ），剩余声望（ {} ）点。'.format(next_title_name, player.Prestige)


def OnClick(args):
	Self = args[0]
	Sender = args[1]
	menu_offset = args[3] if len(args) > 3 else 0
	Menu = args[2] - menu_offset if menu_offset and args[2] >= menu_offset else args[2]
	Dict = {}

	if (Menu == 1):
		if check_item_equipped(Sender, '声望称号'):
			say = """你当前佩戴的声望称号是（ {} ）
			你拥有声望（ {} ）点
			
			[声望称号进阶:2]""".format(Sender.Equipment[EQUIPMENT_SLOTS['声望称号']].Info.ItemName, Sender.Prestige)   #判断声望称号  判断声望值
		else:
			if Sender.Prestige < 200:               #如果声望值小于200点
				say = """让我看看。。。
				你还没有获得这个世界的声望荣誉。
				享有良好声誉后，你就可以获得头衔来证明你的地位。
				来吧，我可以帮助你获得你想要的荣誉。
				
				顺便说一句，你现在的声望是（ {} ）点。
				
				[关闭:0]""".format(Sender.Prestige)              #显示有多少点声望
			else:
				say = """你没有佩戴声望称号，
				但是有足够的声望可以兑换一个，
				要继续吗？
				
				[声望称号进阶:2]
				
				[关闭:0]"""

	# 声望称号进阶
	elif (Menu == 2):
		current_title = Sender.Equipment[EQUIPMENT_SLOTS['声望称号']].Info.ItemName if check_item_equipped(Sender, '声望称号') else '无'
		if current_title == '武林至尊':
			say = """你的声望称号已经达到巅峰了
			
			[关闭:0]"""
		else:
			next_title_dict = findNextFameTitle(Sender, current_title)    #查询声望称号
			if next_title_dict is None:
				say = """当前佩戴的不是有效声望称号，请联系管理员检查。
				
				[关闭:0]"""
			else:
				next_title_name = next_title_dict.keys()[0]                #声望称号名称
				next_title_price = next_title_dict[next_title_name]          #声望值
			
				if Sender.Prestige < next_title_price:             #如果当前声望值小于升级要求的声望
					say = """你当前佩戴的声望称号是（ {} ）
					升级为（ {} ）需要（ {} ）点声望，
					你当前拥有的声望为（ {} ）
					
					[关闭:0]""".format(current_title, next_title_name, next_title_price, Sender.Prestige)   #显示声望称号  显示升级需要的点数   显示自身的声望点
				else:
					say = """你当前佩戴的声望称号是（ {} ）
					是否花费（ {} ）点声望升级为（ {} ）
					
					[升级:3]
					[关闭:0]""".format(current_title, next_title_price, next_title_name)         #显示当前称号     显示升级的点数    显示下级的称号

	# 确认升级
	elif (Menu == 3):
		success, message = upgradeTitle(Sender)
		say = message
		if success:
			say = say + """
			
			[继续进阶:2]
			[关闭:0]"""
		
#主菜单
	else:
		say = """享有良好声誉后，你就可以获得头衔来证明你的地位。
		来吧，我可以帮助你获得你想要的荣誉。
		
		[关于声望称号:1]
		
		[关闭:0]"""

	if menu_offset:
		for menu_id in (1, 2, 3):
			say = say.replace(':{0}]'.format(menu_id), ':{0}]'.format(menu_offset + menu_id))

	Dict['Say'] = say  # 定义聊天框对话内容
	return Dict

NpcEvent.add_listener(210, "OnClick", OnClick)
