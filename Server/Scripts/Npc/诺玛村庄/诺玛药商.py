# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
from Npc.商店列表 import *
from 变量.默认变量 import *
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
	say = ""

#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[关闭:0]"""	
#跳转菜单1商品
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """你快点挑啊？
		挑好了我才能去继续练级。
		
		[关闭:0]"""
#跳转菜单3卖
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的修理类
		say = """闲置不用的物品我出高价回收。
		
		[返回:99]
		[关闭:0]"""
	elif (Menu == 5):
		index = PlayerGetV(Sender,GV_PLAYER_NMDIEMAP)
		x = PlayerGetV(Sender,GV_PLAYER_NMDIEMAPX)
		y = PlayerGetV(Sender,GV_PLAYER_NMDIEMAPY)
		Sender.TeleportByMapIndex(index,x + 1,y + 1)
		return
#主菜单
	else:
		say = """见到你真好。这里四处都是怪物，我很担心。。。
		我想把药水卖完之后，赶快离开这儿。
		虽然比村庄贵一些，可是你来之前，我都给人家卖3倍的价格，
		你到其他地方买不到这个价格。
		
		[查看:1] 商店药品
		
		[离开:5]
		
		[关闭:0]"""#.format(PlayerGetV(Sender,GV_PLAYER_NMDIEMAP),PlayerGetV(Sender,GV_PLAYER_NMDIEMAPX),PlayerGetV(Sender,GV_PLAYER_NMDIEMAPY))
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Enums里的普通类
types =[ItemType.Nothing]
goodslist=[
('金创药（小）',float(2 * Local_Store_PriceRate)),
('金创药（中）',float(2 * Local_Store_PriceRate)),
('金创药（大）',float(2 * Local_Store_PriceRate)),
('魔法药（小）',float(2 * Local_Store_PriceRate)),
('魔法药（中）',float(2 * Local_Store_PriceRate)),
('魔法药（大）',float(2 * Local_Store_PriceRate)),
('万年雪霜',float(2 * Local_Store_PriceRate)),
]
goods = collections.OrderedDict(goodslist)

NpcEvent.add_listener(374,"OnClick",OnClick)

