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
		str = """哥哥的口才真好，总是说好听的。真的令我着迷。
			
		[关闭:0]"""		
#主菜单
	else:	
		str = """正如你所看到的，雪原被来自本国的军队占领。
		他们把村落霸占，作为他们的司令部。
	
		[交谈:1]
		
		[关闭:0]"""
  
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(323,"OnClick",OnClick)