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
#跳转菜单1修理				
	elif (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.SpecialRepair   #类型为Library.Enums里的修理类
		str = """我可以帮你收费便宜的普通修理，也可以完美的特修，
		你自己选择。
		
		[返回:99]
		[关闭:0]"""	
	elif (Menu == 2):
		str = """听说有些特殊的道具，可以完美的特修武器。这真是个好事情。。。
			
		[关闭:0]"""			
#主菜单
	else:
		str = """特殊修理需要特殊的材料，所以留意武器上的特修时间。
		在特修限定时间内，无法再次特修武器，所以留意你的武器持久度。
		
		[修理:1] 武器
		[交谈:2]
		
		[关闭:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict	

#类型为 Enums里的武器类			
types =[ItemType.Weapon]

NpcEvent.add_listener(366,"OnClick",OnClick)