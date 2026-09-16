# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
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


	say = """这里是比奇城堡，我是行政官员。
		
		[结束:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
		

NpcEvent.add_listener(66,"OnClick",OnClick)