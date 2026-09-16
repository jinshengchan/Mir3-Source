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
#跳转菜单1首饰	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library里的NPCDialogType买卖类
		str = """光闪闪的古物件，琳琅满目，你看看吧。
		
		[返回:99]
		[关闭:0]"""                              
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为NPCDialogType里的修理类
		str = """你好，修理首饰很麻烦。。。
		你直接买新的就好啦。
        
		[返回:99]
		[关闭:0]"""	
	elif (Menu == 3):
		str = """听说那个巨大的石门又出现了。我想在石门消失之前过去看看。
			
		[关闭:0]"""	
#跳转菜单4卖				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的修理类
		str = """闲置不用的物品我出高价回收。
		
		[返回:99]
		[关闭:0]"""			
#主菜单
	else:
		str = """既然来了就看看吧。没什么了不起的。

		[查看:1] 商店首饰
		[出售:4] 首饰
		[修理:2] 首饰
		[交谈:3]
		
		[关闭:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict
#类型为 Library.ItemType里的首饰类			
types =[ItemType.Necklace,ItemType.Ring,ItemType.Bracelet]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goodslist=[
('灯笼项链',float(1)),
('白色虎齿项链',float(1)),
('金项链',float(1)),
('传统项链',float(1)),
('指环',float(1)),
('牛角戒指',float(1)),
('蓝色水晶戒指',float(1)),
('铁手镯',float(1)),
('银手镯',float(1)),
('小手镯',float(1)),
('皮制手套',float(1)),
('钢手镯',float(1)),
('大手镯',float(1)),
]

goods = collections.OrderedDict(goodslist)		

NpcEvent.add_listener(305,"OnClick",OnClick)

