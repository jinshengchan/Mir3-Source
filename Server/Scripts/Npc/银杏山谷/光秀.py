# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import Server
import NpcEvent
from datetime import datetime   #增加时间判断
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
		
		[关闭:0]"""	
	elif (Menu == 2):
		say = """有传言说，无论他走到哪里，装饰品都会自动修复。
			
		[对话:3]"""	
	elif (Menu == 3):
		say = """今天没有什么可做的事情。
			
		[关闭:0]"""			
	elif (Menu == 4):
		say = """请选择你要修理的装备，我要做的就是维修。
		
		[武器:11]   [衣服:12]   [头盔:13]   [鞋子:14]   [盾牌:15]
		
		[项链:20]
		
		[手镯左:21]   [手镯右:22]
		
		[戒指左:23]   [戒指右:24]
		
		"""
#特修武器
	elif (Menu == 11):
		if (Sender.Equipment[int(EquipmentSlot.Weapon)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Weapon)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:110]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备武器。
			
			[返回:4]"""
	elif (Menu == 110):
		item = Sender.Equipment[int(EquipmentSlot.Weapon)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.Weapon), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修衣服
	elif (Menu == 12):
		if (Sender.Equipment[int(EquipmentSlot.Armour)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Armour)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:120]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备衣服。
			
			[返回:4]"""
	elif (Menu == 120):
		item = Sender.Equipment[int(EquipmentSlot.Armour)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.Armour), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修头盔
	elif (Menu == 13):
		if (Sender.Equipment[int(EquipmentSlot.Helmet)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Helmet)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:130]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备头盔。
			
			[返回:4]"""
	elif (Menu == 130):
		item = Sender.Equipment[int(EquipmentSlot.Helmet)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.Helmet), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修鞋子
	elif (Menu == 14):
		if (Sender.Equipment[int(EquipmentSlot.Shoes)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Shoes)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:140]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备鞋子。
			
			[返回:4]"""
	elif (Menu == 140):
		item = Sender.Equipment[int(EquipmentSlot.Shoes)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.Shoes), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修盾牌
	elif (Menu == 15):
		if (Sender.Equipment[int(EquipmentSlot.Shield)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Shield)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:150]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备盾牌。
			
			[返回:4]"""
	elif (Menu == 150):
		item = Sender.Equipment[int(EquipmentSlot.Shield)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.Shield), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修项链
	elif (Menu == 20):
		if (Sender.Equipment[int(EquipmentSlot.Necklace)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.Necklace)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:200]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备项链。
			
			[返回:4]"""
	elif (Menu == 200):
		item = Sender.Equipment[int(EquipmentSlot.Necklace)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.Necklace), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修手镯左
	elif (Menu == 21):
		if (Sender.Equipment[int(EquipmentSlot.BraceletL)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.BraceletL)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:210]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备手镯。
			
			[返回:4]"""
	elif (Menu == 210):
		item = Sender.Equipment[int(EquipmentSlot.BraceletL)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.BraceletL), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修手镯右
	elif (Menu == 22):
		if (Sender.Equipment[int(EquipmentSlot.BraceletR)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.BraceletR)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:220]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备手镯。
			
			[返回:4]"""
	elif (Menu == 220):
		item = Sender.Equipment[int(EquipmentSlot.BraceletR)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.BraceletR), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修戒指左
	elif (Menu == 23):
		if (Sender.Equipment[int(EquipmentSlot.RingL)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.RingL)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if ((item.Flags & UserItemFlags.Marriage) != UserItemFlags.Marriage): #是否结婚戒指判断
				if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
					if (Sender.Gold > cost): #判断身上的钱是否不足
						say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
						
								记得检查装备是否穿戴，只有穿戴装备才能特修。
								
						[现在特修:230]"""
					else:
						say = """你的金币不足无法修理。
						
						[返回:4]"""
				else:
					say = """该道具不需要修理。
					
					[返回:4]"""
			else:
					say = """结婚戒指无法特修。
					
					[返回:4]"""
		else:
			say = """你没有装备戒指。
			
			[返回:4]"""
	elif (Menu == 230):
		item = Sender.Equipment[int(EquipmentSlot.RingL)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.RingL), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
#特修戒指右
	elif (Menu == 24):
		if (Sender.Equipment[int(EquipmentSlot.RingR)]): #判断身上是否装备道具
			item = Sender.Equipment[int(EquipmentSlot.RingR)] #道具=身上装备的道具
			cost = item.RepairCost(True)
			coststr = str(cost)
			if (item.CurrentDurability < item.MaxDurability): #判断道具是否去持久需要修理
				if (Sender.Gold > cost): #判断身上的钱是否不足
					say = """特殊修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
					
							记得检查装备是否穿戴，只有穿戴装备才能特修。
							
					[现在特修:240]"""
				else:
					say = """你的金币不足无法修理。
					
					[返回:4]"""
			else:
				say = """该道具不需要修理。
				
				[返回:4]"""
		else:
			say = """你没有装备戒指。
			
			[返回:4]"""
	elif (Menu == 240):
		item = Sender.Equipment[int(EquipmentSlot.RingR)] #道具=身上装备的道具
		cost = item.RepairCost(True)
		coststr = str(cost)
		if (Sender.Gold > cost): #判断身上的钱是否不足
			SubGold(Sender,cost) #扣除修理的费用
			item.CurrentDurability = item.MaxDurability #执行特修
			Sender.DamageItem(GridType.Equipment, int(EquipmentSlot.RingR), 0); #刷新持久显示
			Sender.Connection.ReceiveChat("已经特修好了。",MessageType.System)
			say = """特殊修理完毕，修理费用为 <font color=\"0xff00ff00\">"""+ coststr +"""</font> 金币
			
			[重新查看特殊修理目录:4]"""
		else:
			 say = """你的金币不足无法修理。"""
##主菜单
	else:
		##特修两种写法，第一种是按NPC时间定义来指定特修
		##如果是分钟就写datetime.now().minute  秒就写datetime.now().second
		# hour = datetime.now().hour ###当前小时datetime.now().hour 范围是0-23   
		# if (hour >= 9 and hour < 10) or (hour >= 12 and hour < 13) or (hour >= 18 and hour < 22): ###早上9-10点 中午12-13点 晚上18-22点之间
			# say = """你跟我有共同语言吗？
			
			# [道具要特殊修理:4]
			
			# [关闭:0]"""
		# else:
		say = """我做特殊修理需要特殊材料，所以不能随时都可以修理。
		
		[道具要特殊修理:4]
		[交谈:2]
		
		[关闭:0]"""
		
	Dict['Say']=say                         #定义聊天框对话内容 
	return Dict	

#类型为 Enums里的武器 衣服 头盔 鞋子 盾牌 项链 戒指 手镯类			
types =[ItemType.Weapon,ItemType.Armour,ItemType.Helmet,ItemType.Shoes,ItemType.Shield,ItemType.Necklace,ItemType.Ring,ItemType.Bracelet]

NpcEvent.add_listener(138,"OnClick",OnClick)