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
		if (Sender.Gold < 1000):
			say = """你没有足够的金币，无法传送。
				
				[离开:0]"""
		else:
			SubGold(Sender,1000)
			Sender.TeleportByMapIndex(7,416,177)
			return
	elif(Menu == 2):
		if (Sender.Gold < 2500):
			say = """你没有足够的金币，无法传送。
				
				[离开:0]"""
		else:
			SubGold(Sender,2500)
			Sender.TeleportByMapIndex(27,435,81)
			return
#主菜单	
	else:
		say = """六面神石

		[移动至道馆所需金钱：1000金币:1]

		[移动至绿洲所需金钱：2500金币:2]
		"""
		
		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(18,"OnClick",OnClick)