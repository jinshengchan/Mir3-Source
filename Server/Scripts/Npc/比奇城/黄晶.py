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
		say = """我叫黄晶，不久前接替了叫做云发的学者继续他的研究。
			可是去半兽洞穴2层的王陵调查的时候被一个不知哪儿来的道士赶了出来！
			我还是平生头一次遇到这种丝毫不讲道义并且不与官府的工作合作的道士呢！
			而且说话还十分不客气
			
			……真是……唉，算了。
			
			[我去跟他说说看吧！:2]"""
	elif (Menu == 2):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==119):
			PlayerSetV(Sender,BV_NQ_MAIN,120)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你会帮我去说？由于半兽人的骚动，占用了很多时间，所以要尽快再展开调查。
				可是由于那个家伙的妨碍真是把我郁闷死了！要是你能把那个混蛋道士弄出来的话，我会跟比奇省联系一下让您得到辛苦费的！
				
				[结束:0]"""
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==121):
			PlayerSetV(Sender,BV_NQ_MAIN,122)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """幸亏了你啊！
				竟然有他那种道士……真是……，不管怎么样我会跟比奇省联系一下，比奇城城主大人会给你辛苦费的！
				谢谢你帮助我的工作啊！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==119):
			say = """听说半兽洞穴连接着天然洞穴和半兽天然洞穴，并与比奇县矿山由连接通路相连着。
				唔……我现在有点忙，如果没有什么特别事儿的话就不要来打扰我！
				
				[不知道最近半兽洞穴里有没有什么异常的事情发生？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==120):
			say = """那个道士呆的王陵在半兽洞穴2层（225:175）。
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==121):
			say = """去办的事儿怎么样了？
				
				[嗯，我让他离开那儿了。您可以去进行调查了！:3]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==122):
			say = """托您的福，研究再次展开了！
				
				[结束:0]"""
		else:
			say = """听说半兽洞穴连接着天然洞穴和半兽天然洞穴，并与比奇县矿山由连接通路相连着。
				唔……我现在有点忙，如果没有什么特别事儿的话就不要来打扰我！
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(271,"OnClick",OnClick)
