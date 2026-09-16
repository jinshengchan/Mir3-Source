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

	Sender.TeleportByMapIndex(465,25,27)	#飞地图ID X坐标 Y坐标
	return

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(227,"OnClick",OnClick)