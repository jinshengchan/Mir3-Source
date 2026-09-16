# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
import Globals
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
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
		str = """我不愿意和你这样的人进行交易。
		
		[关闭:0]"""	
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		str = """你好，这里有简单的补给药品。
		
		[关闭:0]"""	
	elif (Menu == 2):
		str = """辛亏道士们消除了这里的邪气，否则我们都不敢到可怕的村子外面去。
			
		[关闭:0]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的修理类
		str = """闲置不用的物品我出高价回收。
		
		[返回:99]
		[关闭:0]"""			
#物品回购
	elif (Menu == 9):
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		str = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
#主菜单
	else:
		str = """欢迎光临，你需要买点什么？
		
		[查看:1] 商店药品
		[出售:3] 药品
		[交谈:2]
		
		[回购:]
		
		[关闭:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数			
goodslist=[
('金创药（小）',float(1)),
('魔法药（小）',float(1)),
('金创药（中）',float(1)),
('魔法药（中）',float(1)),
('金创药（大）',float(1)),
('魔法药（大）',float(1)),
('急救丸（大）',float(1)),
('清心丸（大）',float(1)),
('太阳水',float(1)),]

goods = collections.OrderedDict(goodslist)

NpcEvent.add_listener(40,"OnClick",OnClick)