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

#跳转菜单1
	if (Menu == 1):
		say = """没必要告诉你吧！
			
			[为什么把叫做黄晶的学者赶走呢？:2]"""
	elif (Menu == 2):
		say = """...
			......
			好像在哪儿见过你……你不就是那个打败了骷髅精灵和半兽勇士后得到了什么古代护身符的人吗？
			
			[嗯，是我，不过:3]"""
	elif (Menu == 3):
		say = """哈哈哈……这真是太好了！
			那么我有一个提议，你看如何？
			我是个对你的经历非常感兴趣的人，如果你能够详细的把你是如何破解半兽人诡计的过程讲给我听的话，我就会离开这儿让那个学者进行研究，怎么样？
			
			[好吧！我都告诉你！:4]"""
	elif (Menu == 4):
		say = """....
			.....
			噢噢！这么说不死牌已经完整了啊！那个时候我好像在半兽洞穴1层的什么地方见过你。那么不死牌怎么处理了呢？ 
			
			[被放在比奇省衙门保管起来了！:5]"""
	elif (Menu == 5):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 120):
			PlayerSetV(Sender,BV_NQ_MAIN,121)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """原来如此……可要好好看管才是啊！别让居心不良的人给偷走……
				哈哈哈
				那么我会按照约定离开这里，告诉那个学者来这儿好好调查吧！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==120):
			say = """对不起，我现在正在进行重要的研究，请别来妨碍我，最好走开！
				
				[你在这儿要做什么呢？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==121):
			say = """没想到在附近竟有这种宝物，我要另外进行试验……嘿嘿嘿
				
				[结束:0]"""
		else:
			say = """唔……我现在有点忙，如果没有什么特别事儿的话就不要来打扰我！
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(272,"OnClick",OnClick)
