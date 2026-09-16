# -*- coding: utf-8 -*-
#载入模块SYS
import sys
import datetime
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import Server
import NpcEvent
import Server.Envir.SEnvir as SEnvir
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
		Sender.TeleportByMapIndex(1,451,390)   #把玩家传送回比奇
		return
#主菜单
	else:
		say = """[回比奇:1]
		
		[关闭:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(350,"OnClick",OnClick)