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
		if(PlayerGetV(Sender,BV_NQ_MAIN)==90):
			PlayerSetV(Sender,BV_NQ_MAIN,91)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """他自从去调查天然洞穴走后就直到现在还没有回来！已经过了说好回来的日子好几天了，连个信儿都没有，所以我每天都是惶惑不安的独自度过的……
				呜呜……真担心他出了什么事儿，实在是坚持不住了啊！
				您一定要去把我在天然洞穴的丈夫平安的找回来啊！如果您遇到了我丈夫的话，可能您就会知道您想要知道的事情的！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==90):
			say = """啊……您是来找云发的……
				呜……呜……
				
				[出什么事儿了吗？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==91):
			say = """啊！老天爷啊……到底把我的丈夫……
				啊…… 只能拜托您了……如果您能把他平安的带回来我一定会好好报答您的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==92):
			say = """遇到我的丈夫了？啊！太感谢了！
				他一切平安啊，他要找的助手就是护卫武士嘉登先生啊！ 
				快去找嘉登先生吧！洞中没有护卫武士只有他自己……这可不行啊！
				快快去找嘉登先生吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==93):
			say = """顺利见到嘉登先生了啊！
				谢谢……但是……啊…他要完成研究啊！
				那我就只能耐心等他回来了！不管怎么样既然知道他一切都好，我就放心多了！
				
				[结束:0]"""
		elif(93 < PlayerGetV(Sender,BV_NQ_MAIN) < 102):
			say = """不管怎么样既然知道他一切都好，我就放心多了！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==102):
			say = """您说比奇城城主大人下令让云发回来？
				现在马上就能见到云发了！谢谢你告诉我啊……
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==103):
			say = """现在马上就能见到云发了！谢谢你告诉我啊……
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==104):
			PlayerSetV(Sender,BV_NQ_MAIN,105)
			Sender.GiveItem('太阳水',20)
			GiveGold(Sender,5000)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """欢迎光临！
				多亏您帮忙我的丈夫才能平安无事的回来！
				真心的感谢您！
				这些虽然不是什么贵重的东西，但是代表了我的一片心意！
				家夫就在屋子里，我带您进去吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) > 104):
			say = """这个人继续工作的时候我也不能放心的睡大觉啊！
				
				[结束:0]"""
		else:
			say = """巧妇难为无米之炊啊！…… 唉……
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(266,"OnClick",OnClick)
