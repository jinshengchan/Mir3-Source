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
#跳转菜单1衣服	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		str = """我们有很多种护甲，你想买吗？
		
		[返回:99]
		[关闭:0]"""        
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		str = """请放心吧，
		我会修理好这些护具的。
		
		[返回:99]
		[关闭:0]"""	
	elif (Menu == 3):
		str = """哈哈，为了怡美，好不容易来到了这里。
		因为怪物的袭击，这里变得非常荒凉。
		剩下的希望就是多赚点钱，好送怡美去道馆学习。
		想说一堆怡美的事情，可惜很多人都不想听，所以就不说了。
			
		[关闭:0]"""	
#跳转菜单4卖				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		str = """闲置不用的物品我出高价回收。
		
		[返回:99]
		[关闭:0]"""			
#主菜单
	else:
		str = """你好，不知道这些护具是否适合你。。。
		如果有需要，请参考价格购买。
		我们有很多种护甲，你想买吗？
		
		[查看:1] 商店护具
		[出售:4] 护具
		[修理:2] 护具		
		[交谈:3]
		
		[关闭:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的衣服头盔鞋子盾牌类			
types =[ItemType.Armour,ItemType.Helmet,ItemType.Shoes,ItemType.Shield]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goodslist=[
('青铜头盔',float(1)),
('魔法头盔',float(1)),
('布衣（男）',float(1)),
('布衣（女）',float(1)),
('轻型盔甲（男）',float(1)),
('轻型盔甲（女）',float(1)),
('灵魂战衣（男）',float(1)),
('灵魂战衣（女）',float(1)),
('重盔甲（男）',float(1)),
('重盔甲（女）',float(1)),
('魔法长袍（男）',float(1)),
('魔法长袍（女）',float(1)),
]

goods = collections.OrderedDict(goodslist)

NpcEvent.add_listener(320,"OnClick",OnClick)