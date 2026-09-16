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
import random
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
		say = """只要你经过一定历练，并且拥有合适的技能书，就可以直接学习啦！！！
			
			[结束:0]"""
#主菜单
	else:
		if Sender.Class == Sender.Class.Warrior:
			say = """贫道就是清明子，你听说过吗？
			呵呵呵，贫道最近在指导江湖的后生们。
			不过，你不是道士啊。
			你这个战士还是去找龙血先生吧。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Wizard:
			say = """贫道就是清明子，你听说过吗？
			呵呵呵，贫道最近在指导江湖的后生们。
			不过，你不是道士啊。
			你这个魔法师还是去找霹雳尊者吧。
			
			[结束:0]"""
		elif Sender.Class == Sender.Class.Assassin:
			say = """贫道就是清明子，你听说过吗？
			呵呵呵， 贫道最近在指导江湖的后生们。
			不过，你不是道士啊。
			你这个刺客还是去找你的导师吧。
			
			[结束:0]"""
		else:
			if(PlayerGetV(Sender,BV_NQ_MAIN)==26):
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """欢迎，我一看就知道你在学习道家方面的东西。
				看来你的实力已经得到了士官的认可，那么，这本武功秘籍就送给你吧。
				
				[结束:0]
				"""
			else:
				say = """欢迎，我一看就知道你在学习道家方面的东西。
					如果你在修炼中有什么解决不了的问题，不要犹豫，来找我就行了。
					
					[交谈:1]
					
					[结束:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(31,"OnClick",OnClick)