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
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
		
		[关闭:0]"""
#主菜单
	else:
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.RootSell  #类型为Library.Enums里的买卖类		
		say = """欢迎光临，对，我就是买栗子的。如果你能给我找来那些
				味道又好，营养又好的栗子，我就送你一份大礼。
				你有栗子吗？
				
				[马上去给你找:0]
				"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的无类			
types =[ItemType.Nothing]
	
NpcEvent.add_listener(49,"OnClick",OnClick)
NpcEvent.add_listener(63,"OnClick",OnClick)
NpcEvent.add_listener(117,"OnClick",OnClick)
