# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
import collections
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
	
	if(Menu == 1):
		Sender.TeleportByMapIndex(24,363,212)
		return
	else:
		say = """在矿山采矿，一定要处处小心啊，指不定哪里就会冒出来可怕的怪物。。。
			如果你害怕了，就回村里去吧！
			
			[移动至毒蛇山谷:1]
			[结束:0]"""	
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(275,"OnClick",OnClick)