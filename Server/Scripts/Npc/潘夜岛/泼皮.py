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
		say = """我不愿意和你这样的人进行交易。
		
		[结束:0]"""	
	elif (Menu == 1):
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.RootSell  #类型为Library.Enums里的卖类		
		say = """你要出售什么？
			
		[前一步:99]"""
#主菜单
	else:
		say = """欢迎光临，请卖给我蚂蚁卵或者骷髅骨之类的材料。
	    
		[出售:1]材料
		
		[结束:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的无类			
types =[ItemType.Nothing]

NpcEvent.add_listener(142,"OnClick",OnClick)