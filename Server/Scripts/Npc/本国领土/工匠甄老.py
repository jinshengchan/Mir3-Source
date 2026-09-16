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
	
	str = """现在的雪原领地，以前这里人迹罕至。
	我的身体以前很强壮，在这寒冷的地方变得骨瘦如柴。
	喂，你去过神宫冰宫吗？那里比这里更险峻吓人。。。
	呵呵，对忙碌的人来说，我只是诉苦而已。
	
	[关闭:0]"""
  
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict

#NpcEvent.add_listener(310,"OnClick",OnClick)