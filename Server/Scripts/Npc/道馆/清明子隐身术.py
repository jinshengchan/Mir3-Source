# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
from Defines import *
import random
clr.AddReference("Library")
from Library import *
import NpcEvent
from 主线任务奖励 import *
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
		PlayerSetV(Sender,GV_Taoist_Invisibility,2)
		Sender.TeleportByMapIndex(9,12,13)
		return

	else:
		PlayerSetV(Sender,GV_Taoist_Invisibility,2)
		say = """祝贺你，做得好！
			这里危险，请到外面去。
			
			[离开:1]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(321,"OnClick",OnClick)