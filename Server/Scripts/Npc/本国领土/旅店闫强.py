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
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		str = """我不愿意和你这样的人进行交易。
		
		[关闭:0]"""	                            
#跳转菜单2仓库				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Storage   #类型为NPCDialogType里的仓库类
		str = """查看仓库中的物品。
        
		[返回:99]
		[关闭:0]"""	
	elif (Menu == 3):
		str = """有人在雪原看到一个巨大的石阵。
			
		[关闭:0]"""		
#主菜单
	else:	
		str = """欢迎光临。你有什么需要保管的？
	
		[管理:2] 仓库
		[交谈:3]
		
		[关闭:0]"""
  
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict

#类型为 Enums里的普通类			
types =[ItemType.Nothing]


NpcEvent.add_listener(314,"OnClick",OnClick)