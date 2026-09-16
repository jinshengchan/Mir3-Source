# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
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
	elif(Menu == 1):
		say = """看来你不了解给你证书的人。
			洪气霖一生坎坷，他家经营的店铺原本在比奇县一带很有名望，但自从他们家的货船失事以后，他们家族就没落了。
			虽然我知道洪家的处境很艰难，但我们也不能因此而蒙受损失啊，所以我们不能接受这种证书。
			
			[那这证书怎么办？:2]"""
	elif(Menu == 2):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 45):
			PlayerSetV(Sender,BV_NQ_MAIN,46)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """嗯..装饰品店 所蒙受的损失少一点，说不定他们会接受。
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 45):
			if(Sender.GetItemCount('气霖证书') < 1):
				say = """你好，要我帮忙吗？
					
					[结束:0]"""
			else:
				say = """对不起，本店不接受这种证书。
					
					[为什么？:1]"""
		else:
			say = """要我帮忙吗？
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(251,"OnClick",OnClick)
