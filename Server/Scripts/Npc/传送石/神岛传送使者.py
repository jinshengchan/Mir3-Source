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
		Sender.TeleportByMapIndex(1,371,335)
		return
	elif(Menu == 2):
		if (Sender.GetItemCount("传送石") < 1):
			say = """无法传送到目的地，
			没有启动法阵的传送石。

			[离开:0]"""		

		elif (Sender.GameGold < 200):
			say = """你没有足够的元宝，无法传送。
			[离开:0]"""
		else:
			SubGameGold(Sender,200)
			Sender.TakeItem("传送石",1)
			Sender.TeleportByMapIndex(1551,96,218)
			return

#主菜单
	else:
		if Sender.Character.Rebirth < 4 : # 等级判断
			say  = """请你离开。
			转生4级后，我可以送你去。
			
			[离开:0]"""
		else:
			say = """你将去一座神秘的海岛，做好准备了吗?
			
			[我准备好了:2]    
			
<font color=\"0xff00ff00\">进入奔马岛至少四级转生</font>
<font color=\"0xff00ff00\">打开传送法阵需要200元宝，1颗传送石</font>

			
			[我怕死我不去:0]"""

		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(377,"OnClick",OnClick)	