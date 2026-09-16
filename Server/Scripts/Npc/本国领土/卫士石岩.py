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
		str = """你要去找那个石门？
		
		[继续交谈:2]
		
		[关闭:0]"""	
	elif (Menu == 2):
		str = """太危险了，我不想和你说。
	
		[关闭:0]"""
#主菜单
	else:	
		str = """我听说山上有个石门。父亲说那是个奇迹。
	
		[交谈:1]
		
		[关闭:0]"""
  
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(309,"OnClick",OnClick)