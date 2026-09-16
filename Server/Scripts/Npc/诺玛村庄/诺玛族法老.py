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

	if (Menu == 1):
		say = """人类和诺玛族之间正发生一场残酷无情的战争。
		只要诺玛统领还没有被消失，这场战争就永远不会划上终止符。
		
		[关闭:0]"""
	elif (Menu == 2):
		if (PlayerGetV(Sender,GV_PLAYER_LQYSDZM) > 0):
			say = """你已经领取过勇士的证明，无法重复领取。
			
			[关闭:0]"""
		elif (Sender.Level < 48):
			say = """你的等级没有达到48级，无法领取。
			
			[关闭:0]"""
		else:
			if (GetInventoryCount(Sender) >= 2):
				PlayerSetV(Sender,GV_PLAYER_LQYSDZM,99)
				Sender.GiveItem("勇士的证明",1)
				Sender.GiveItemsByStat([{'name':'淬炼石','bound':True,'count':1,},])
				say = """领取成功。
				
				[关闭:0]"""
			else:
				say ="""你的包裹没有空格。
				
				[离开:0]"""
	elif (Menu == 3):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """你快点挑啊？
		
		[关闭:0]"""
#主菜单
	else:
		say = """我就是你要找的诺玛族法老……
			年轻人，我知道有一天你会出现在我面前的！
			
			[交谈:1]
			
			[领取勇士的证明:2]
			
			[关闭:0]"""

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

NpcEvent.add_listener(376,"OnClick",OnClick)

