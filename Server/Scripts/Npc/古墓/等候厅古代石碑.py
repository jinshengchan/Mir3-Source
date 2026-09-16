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
	str = ""
	
	if(Menu == 1):
		Sender.TeleportByMapIndex(1638,198,200)		#飞地图ID X坐标 Y坐标

	elif(Menu == 2):
		Sender.TeleportByMapIndex(1639,198,200)		#飞地图ID X坐标 Y坐标

	elif(Menu == 3):
		Sender.TeleportByMapIndex(1640,198,200)		#飞地图ID X坐标 Y坐标

	elif(Menu == 4):
		Sender.TeleportByMapIndex(1641,198,200)		#飞地图ID X坐标 Y坐标

	elif(Menu == 5):
		Sender.TeleportByMapIndex(1642,198,200)		#飞地图ID X坐标 Y坐标

#主菜单	
	else:
		str = """如古墓1出现的石碑一样，这里的石碑充满了神秘。
		可以从这里传送到下一个地方。

		前往古墓<font color=\"0xffcc00cc\">2-1</font>层 [传送:1]
		前往古墓<font color=\"0xffcc00cc\">2-2</font>层 [传送:2]
		前往古墓<font color=\"0xffcc00cc\">2-3</font>层 [传送:3]
		前往古墓<font color=\"0xffcc00cc\">2-4</font>层 [传送:4]
		前往古墓<font color=\"0xffcc00cc\">2-5</font>层 [传送:5]

		[不传送:0]
		
		"""	
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(406,"OnClick",OnClick)

