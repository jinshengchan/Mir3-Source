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
		str = """像你这种双手沾满鲜血的人，我是不会理会的。
		
		[关闭:0]"""	
        elif(Menu == 1):
		if (Sender.Gold < 50000):
			str = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,50000)
			Sender.TeleportByMapIndex(702,42,133)	
			return

#主菜单	
	else:
		str = """你将被传送到一个有桃花盛开的地方，
相传那是一个很美丽的地方，但是那个地方有一群来自
森林深处的怪物把守。

		[传送桃花:1] （金币 50000） 
		

		[关闭:0]"""	
		
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(268,"OnClick",OnClick)	