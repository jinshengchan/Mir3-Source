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
#跳转菜单1杂货	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """你想买什么？
		
		[前一步:99]"""
#跳转菜单4卖				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """你要卖什么？
		
		[前一步:99]"""
	elif (Menu == 5):
		say = """我们店里有地牢逃脱卷，
		随机传送卷和修复油等，还有只能从怪物那里得到的回城卷
		
		[前一步:99]"""		
#物品回购
	elif Menu == 6:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
#主菜单
	else:
		say = """欢迎光临，有什么事吗？
		
		[购买:1]物品
		[出售:4]物品
		[询问:5]有关商品的事
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Library.Enums里的其他类
types =[ItemType.Nothing]
goods = collections.OrderedDict(zahuodiangoodslist)

NpcEvent.add_listener(136,"OnClick",OnClick)
