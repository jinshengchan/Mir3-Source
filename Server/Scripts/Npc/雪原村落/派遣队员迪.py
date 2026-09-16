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
	
	if (Menu == 1):
		str = """情况变得很严重。
		邪恶的力量变得很强大，我们无法出击。
		从雪原到月河渊的路大部分被堵住了，需要人帮我进入通道寻找新的道路。
		你愿意协助我吗？
		
		[交谈:2]
			
		[关闭:0]"""

	elif(Menu == 11):
		Sender.TeleportByMapIndex(720,33,10)	#飞地图ID X坐标 Y坐标
		return
			
	elif (Menu == 2):
		str = """没有需要你做的事情。
		
		[关闭:0]"""	
#主菜单
	else:	
		str = """你能和我谈谈吗？
	
		[什么事情:1]
		[算了:0]"""

#		[传送到月河通道:11]

	Dict['Say']=str                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(328,"OnClick",OnClick)