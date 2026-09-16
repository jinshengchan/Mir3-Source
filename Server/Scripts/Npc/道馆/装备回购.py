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
import Server
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
	
	say = ''

	if (Menu == 110):
		say = """[回购武器:111]    [回购防具:112]
		
		[回购首饰:113]    [回购书籍:114]
		
		[回购其他:115]
		"""
	elif (Menu == 111):
		# types指定回购物品的类型
		Dict['Types'] = types1
		Dict['DialogType'] = NPCDialogType.BuyBack

		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
	elif (Menu == 112):
		# types指定回购物品的类型
		Dict['Types'] = types2
		Dict['DialogType'] = NPCDialogType.BuyBack
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
	elif (Menu == 113):
		# types指定回购物品的类型
		Dict['Types'] = types3
		Dict['DialogType'] = NPCDialogType.BuyBack
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
	elif (Menu == 114):
		# types指定回购物品的类型
		Dict['Types'] = types4
		Dict['DialogType'] = NPCDialogType.BuyBack
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
	elif (Menu == 115):
		# types指定回购物品的类型
		Dict['Types'] = types5
		Dict['DialogType'] = NPCDialogType.BuyBack
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
#主菜单
	else:
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
			[淘宝旧货:110]
			
			[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

#类型为 Library.Enums里的其他类
types1 =[ItemType.Weapon]  #武器
types2 =[ItemType.Armour,ItemType.Helmet,ItemType.Shoes]  #防具
types3 =[ItemType.Necklace,ItemType.Bracelet,ItemType.Ring]  #首饰
types4 =[ItemType.Book]  #书籍
types5 =[ItemType.Ore]  #杂货

NpcEvent.add_listener(333,"OnClick",OnClick)


