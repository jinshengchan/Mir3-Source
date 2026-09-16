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
		
		[离开:0]"""
#飞	
	elif(Menu == 1):
		if (Sender.Gold < 500):
			say = """你没有足够的金币，无法传送。
				
				[离开:0]"""
		else:
			SubGold(Sender,500)
			Sender.TeleportByMapIndex(27,435,81)
			return
#主菜单	
	else:
		say = """六面神石

		[移动至绿洲所需金钱：500金币:1]
		"""
		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(25,"OnClick",OnClick)
NpcEvent.add_listener(300,"OnClick",OnClick)
