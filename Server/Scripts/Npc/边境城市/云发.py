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
		say = """所以只要把这个东西毁掉的话，半兽人就无法使用魔法了。
			不过这不死牌原本是由两半合二为一组成的，现在我们只有这半块儿，所以一定要找到那另外的半块儿！
			我觉得这所有的事情的幕后都是由那个最近聚集势力的半兽勇士搞得鬼。您要找到这剩下的半块儿不死牌的力量，那么一定能找到那个半兽勇士。
			关于半兽勇士的情报请去告诉比奇城城主大人。我来这里的时候收集了各处的情报，现在可以掌握大概的位置了。
			
			[知道了！我会在比奇省转告这些的！:2]"""
	elif (Menu == 2):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==105):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """那就再多辛苦一下啦！
			
			[结束:0]"""
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==105):
			say = """
				
				首先感谢您帮了我妻子的忙！
				要是没有您的话！我到现在还在天然洞穴中进退两难，让妻子为如此我担心。
				哦，对了，对不死牌的分析刚刚结束！
				这其实是古代的遗物，而并非是半兽人所制，只是偶然间流落到了半兽人手中！
				半兽人那样的家伙是造不出这样的东西的……
				
				[原来如此啊！:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==106):
			say = """骷髅精灵好像还拿着剩下的那半块儿不死牌！
				
				[结束:0]"""
		else:
			say = """
				
				我在工作，请勿打扰。
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(267,"OnClick",OnClick)
