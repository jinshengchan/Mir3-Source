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
		str = """请你离开，红名无法传送。
		
		[关闭:0]"""	
	elif(Menu == 1):
		if (Sender.Gold < 18000):
			str = """你没有足够的金币，无法传送。
				
				[关闭:0]"""	
		else:
			SubGold(Sender,18000)
			Sender.TeleportByMapIndex(7,419,176)	#飞地图ID X坐标 Y坐标
			return
	elif(Menu == 2):
		if (Sender.Gold < 6000):
			str = """你没有足够的金币，无法传送。
				
				[关闭:0]"""				
		else:
			SubGold(Sender,12000)
			Sender.TeleportByMapIndex(490,127,45)	
			return				
#主菜单	
	else:
		str = """『六面神石』
		
		可传送区域
		　　　<font color=\"0xffEE00EE\">道馆　    18,000金币</font>
		　　　<font color=\"0xffEE00EE\">本国领土  12,000金币</font>
		传送吗？

		[去道馆:1]
		[本国领土:2]
		
		[不传送:0]
		
		"""	
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(321,"OnClick",OnClick)	