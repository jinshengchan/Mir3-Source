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
	Dict={}
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[结束:0]"""	
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """请选择要购买的武器。
		
		[返回:5]
		[结束:0]"""
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.SpecialRepair   #类型为Library.Enums里的特修类
		say = """请把要修理的武器放上去。
		
		[前一步:99]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """闲置不用的物品我出高价回收。
		
		[返回:99]
		[关闭:0]"""
	elif (Menu == 4):
		item = Sender.Equipment[int(EquipmentSlot.Weapon)] #道具=身上装备的道具
		#判断手上是否有武器	
		if (not item):
			say = """你没有装备武器，无法特修。
			
			[结束:0]"""
		elif (not item.Info.CanRepair):
			say = """当前武器不能修理。
			
			[返回:4]"""
		else:
			cost = item.RepairCost(True)
			coststr = str(cost)
			say = """修理费用是"""+ coststr +"""。
			
			这个特修是只有带着物品的情况下才可以特修。请确认一下
			是否带着。
			
			[现在修理:41]
			[前一步:99]"""
#特修武器
	elif (Menu == 41):
		if (Sender.Equipment[int(EquipmentSlot.Weapon)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Weapon)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					SubGold(Sender,cost) #扣除修理的费用
					item.CurrentDurability = item.MaxDurability #执行特修
					Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.Weapon), 0) #刷新持久显示
					Sender.RefreshStats()
					say = """修理的很好。
					修理费用是"""+ coststr +"""。
					
					[结束:0]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备武器。
			
			[返回:4]"""
#主菜单
	else:
		say = """很高兴见到你，有什么事吗？
		
		[特殊修理:4]武器
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的武器类			
types =[ItemType.Weapon]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goods = collections.OrderedDict(wuqidiangoodslist)

NpcEvent.add_listener(56,"OnClick",OnClick)