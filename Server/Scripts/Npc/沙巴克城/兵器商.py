# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
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
	say = "" 

	say = """这里是卖攻城时专用武器的子弹的地方。。
		
		[购买投石车:1]
		[购买弩车:2]
		
		[托付攻城兵器:3]
		[找回攻城兵器:4]
		
		[出售攻城兵器:5]
		[购买箭，石头:6]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(93,"OnClick",OnClick)