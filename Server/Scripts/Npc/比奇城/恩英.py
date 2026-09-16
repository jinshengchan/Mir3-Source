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
		say = """你需要什么东西？
		
		[前一步:99]"""	
#跳转菜单2卖				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把要出售的物品交给我。
		
		[前一步:99]"""			
#物品回购
	elif Menu == 5:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
#主菜单
	else:
		say = """欢迎光临，这里出售一些简单的药品。
		
		[购买:1]药品
		[出售:2]药品
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数			
goods = collections.OrderedDict(yaodiangoodslist)

NpcEvent.add_listener(77,"OnClick",OnClick)



