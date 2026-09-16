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
		str = """慢慢挑选不着急，物品有很多。
		
		[返回:5]
		[关闭:0]"""
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		str = """我可以帮你收费便宜的普通修理，也可以完美的特修，
		你自己选择。
		
		[返回:5]
		[关闭:0]"""	
	elif (Menu == 3):
		str = """有人在雪原看到一个巨大的石阵。
			
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
		str = """本来我们只和武林人士进行交易，但是很多路人和游客都受到怪物的袭击，所以将军下命令，对所有人开放交易。
		你在这里小心点，脾气比较好的话，是会获得客人的待遇。
		
		[查看:1] 商店武器
		[出售:4] 武器
		[修理:2] 武器
		[交谈:3]
		
		[关闭:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的武器类			
types =[ItemType.Weapon]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goodslist=[
('青铜斧',float(1)),
('斩马刀',float(1)),
('修罗',float(1)),
('半月',float(1)),
('降魔',float(1)),
('海魂',float(1)),
('偃月',float(1)),
]

goods = collections.OrderedDict(goodslist)

NpcEvent.add_listener(301,"OnClick",OnClick)