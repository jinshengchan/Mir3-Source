# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
from System import DateTime
import NpcEvent
import random
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
	Dict={}

	if (Menu == 1):
		random_select = [1, 2, 2, 3, 4]  # 每次增加属性的概率，如第一个为1/1，第二个为1/2，最多11个元素
		# 装备列表
		random_equip = [EquipmentSlot.Weapon, EquipmentSlot.Necklace, EquipmentSlot.BraceletL, EquipmentSlot.BraceletR,
						EquipmentSlot.RingL, EquipmentSlot.RingR, EquipmentSlot.Armour, EquipmentSlot.Helmet,
						EquipmentSlot.Shoes, EquipmentSlot.Torch, EquipmentSlot.Shield]
		RandomAddProp([Sender, random_select, random_equip])
		return

	else:
		str = """<font color=0xffcc0099>年轻人，来到这就是莫大的机缘，我可以依次从武器到项链手镯戒指衣服头盔鞋火炬盾牌为止增加随机属性，如果没有装备，将会浪费下面部位提升机会。</font>
		
		[谢谢仙人指点:1] 我要变得更强

		[关闭:0]
	
	"""

	Dict['Say']=str                         #定义聊天框对话内容
	return Dict


def RandomAddProp(params):
	Sender = params[0]
	random_select = params[1]
	random_equip = params[2]
	if len(random_select) == 0:  # 加点结束退出
		Sender.TeleportByMapIndex(2,40,33)
		return
	if len(random_equip) == 0:  # 不存在装备可以加点退出
		Sender.Connection.ReceiveChat("装备不存在，无法增加属性。", MessageType.System)
		Sender.TeleportByMapIndex(2,40,33)
		return
	equip_select = random.randint(0, len(random_equip) - 1)  # 随机选择装备
	select = random.randint(1, random_select[0])  # 判断加点成功几率
	if select == 1:
		if Sender.Equipment[int(random_equip[equip_select])]:
			luck = random.randint(1, 100)
			if luck <= 1:  # 极品加点，概率目前为1/100
				#Sender.Connection.ReceiveChat(str(luck), MessageType.System)
				try:  # 武器加点
					Sender.ItemStatsChangeRefresh(int(random_equip[equip_select]), Stat.MaxDC, 5, StatSource.Enhancement)  # 数字代表加点数，下同
					Sender.ItemStatsChangeRefresh(int(random_equip[equip_select]), Stat.MaxMC, 5, StatSource.Enhancement)
					Sender.ItemStatsChangeRefresh(int(random_equip[equip_select]), Stat.MaxSC, 5, StatSource.Enhancement)
				except:  # 其他装备加点
					Sender.ItemStatsChangeRefresh(random_equip[equip_select], Stat.MaxDC, 2, StatSource.Enhancement)
					Sender.ItemStatsChangeRefresh(random_equip[equip_select], Stat.MaxMC, 2, StatSource.Enhancement)
					Sender.ItemStatsChangeRefresh(random_equip[equip_select], Stat.MaxSC, 2, StatSource.Enhancement)
			else:  # 普通加点
				try:  # 武器
					Sender.ItemStatsChangeRefresh(int(random_equip[equip_select]), Stat.MaxDC, 2, StatSource.Enhancement)
					Sender.ItemStatsChangeRefresh(int(random_equip[equip_select]), Stat.MaxMC, 2, StatSource.Enhancement)
					Sender.ItemStatsChangeRefresh(int(random_equip[equip_select]), Stat.MaxSC, 2, StatSource.Enhancement)
				except:  # 其他装备
					Sender.ItemStatsChangeRefresh(random_equip[equip_select], Stat.MaxDC, 1, StatSource.Enhancement)
					Sender.ItemStatsChangeRefresh(random_equip[equip_select], Stat.MaxMC, 1, StatSource.Enhancement)
					Sender.ItemStatsChangeRefresh(random_equip[equip_select], Stat.MaxSC, 1, StatSource.Enhancement)
			random_select.pop(0)
			random_equip.pop(equip_select)
			RandomAddProp([Sender, random_select, random_equip])
		else:
			random_equip.pop(equip_select)
			RandomAddProp([Sender, random_select, random_equip])
	else:
			Sender.Connection.ReceiveChat("加点结束。", MessageType.System)
			RandomAddProp([Sender, [], []])

NpcEvent.add_listener(337,"OnClick",OnClick)