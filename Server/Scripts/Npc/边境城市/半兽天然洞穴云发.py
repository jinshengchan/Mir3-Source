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

#红名
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
#跳转菜单1
	elif (Menu == 1):
		say = """好，后会有期！
			
			[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN) < 100):
			say = """角笛……难道是角笛？去找找吧！显然是有关系的东西！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 100):
			say = """果然是角笛呀……不管怎么样真的要出大问题了……快去半兽洞穴调查一下吧！
				显然是通过魔法才能做到的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 101):
			say = """啊……虽然不希望是那样……到底是不死牌啊！快去比奇城城主大人那儿看看吧！ 
				虽然我也想跑去，可我这身子骨儿……去不了啊！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 102):
			PlayerSetV(Sender,BV_NQ_MAIN,103)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """要我中断调查马上回来？
				明白了，那么我现在马上回比奇省去。
				
				[那么比奇省再会！:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 103):
			say = """请马上出发， 我也马上要用卷离开了。
				
				[结束:0]"""
		else:
			say = """正在为不死牌该怎么处理的问题而苦恼之中。 虽然比奇城城主想要毁掉它，但岂不是太可惜了？这毕竟是很有研究价值的东西啊！…
				
				[结束:0]"""


	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(269,"OnClick",OnClick)