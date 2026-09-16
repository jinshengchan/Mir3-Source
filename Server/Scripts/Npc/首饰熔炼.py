# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
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
#首饰升级说明	
	if(Menu == 1):
		say = """要提升首饰属性，首先必须它对他进行精炼。
		将相同的首饰熔化，提升首饰的修炼值。
		一旦修炼值达到100%，您就可以对首饰属性进行提升。

		[返回:99]
		[离开:0]"""
#首饰熔炼		
	elif(Menu == 2):
		Dict['DialogType']= NPCDialogType.AccessoryRefineLevel
		say = """首先选择要升级的首饰。
		然后选择你想要融化使用的其他首饰。

		[返回:99]
		[离开:0]"""
#首饰提升		
	elif(Menu == 3):
		Dict['DialogType']= NPCDialogType.AccessoryRefineUpgrade
		say = """给我看看你已经升级好了，准备提升属性的首饰，
		这个过程不会失败，所以不要担心。

		[返回:99]
		[离开:0]"""
#首饰重置		
	elif(Menu == 4):
		Dict['DialogType']= NPCDialogType.AccessoryReset
		say = """给我看看你的首饰，他已经升级，可以重置了。

		这个过程不会失败，所以不要担心。

		[返回:99]
		[离开:0]"""
#主菜单		
	else:		
		say = """因此，你希望升级你的首饰。。。

		[关于:1] 首饰升级

		[熔炼:2] 首饰等级
		[提升:3] 首饰属性
		[重置:4] 首饰

		[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	

NpcEvent.add_listener(355,"OnClick",OnClick)