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
		str = """。。。我希望你能帮我找点感冒药。
		我不知道怎么感冒了。。。
			
		[关闭:0]"""		
#主菜单
	else:	
		str = """你怎么那样看着我？呵呵，你是不是遇到了我弟弟。
	
		[交谈:1]
		
		[关闭:0]"""
  
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(307,"OnClick",OnClick)