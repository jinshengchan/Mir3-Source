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
#红名判断
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
#跳转菜单1
	elif (Menu == 1):
		say = """崔大哥知道关于比奇省的历史！
			崔大哥一会就会回来的。
			
			[结束:0]"""
	elif (Menu == 2):
		PlayerSetV(Sender,BV_NQ_MAIN,67)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """说起比奇省的历史...
			知道吗，我们的祖先就是讨伐半兽人族地区而派遣出的远征队啊！
			我们的祖先经过残酷的战斗终于击溃了怪物们。
			一想到只要再继续坚持战斗一下就可以把怪物们斩草除根，然后可以回到故乡，就都非常高兴。
			可是没想到这时突然发生了始料未及的灾难。这里发生了大地震。
			原本可以翻过山脉回到家乡的路由于这次大地震导致地壳变动，完全的被隔断了！
			有的人痛哭流涕，有的人茫然失措。所有人都慌了手脚。
			但是一位优秀的将领重新振作精神，开始在这个地区寻找求生之路。
			他指挥着他的部下们在赶走半兽人族的地区找到了一片肥沃的土地建立了新的城市。这就是现在的比奇省。
			好了，我已经把知道的基本上全都告诉你啦……我也要走啦！
			
			[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==65):
			say = """听说有人找我，是你吗？
				鄙人就是崔某，有什么事儿吗？
				
				[询问比奇省的历史:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==66):
			say = """听说有人找我，是你吗？
				鄙人就是崔某，有什么事儿吗？
				
				[询问比奇省的历史:2]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==67):
			say = """我知道的只有这些了，你再找别的卫士问问吧。
				
				[结束:0]"""
		else:
			say = """要我帮忙吗？
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(257,"OnClick",OnClick)
