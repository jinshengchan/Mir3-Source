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
		say = """请你离开，红名无法传送。
		
		[结束:0]"""	
#飞	
	elif(Menu == 1):
		Sender.TeleportByMapIndex(103,31,373)
		return		
#主菜单	
	else:
		say = """到矿石采矿可以挣钱，你也想挣大钱？那就准备好鹤嘴锄去
		矿石吧。如果你不知道怎么去矿石，我可以把你移动过去。

		[移动至矿山:1]
		[结束:0]"""	
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(84,"OnClick",OnClick)