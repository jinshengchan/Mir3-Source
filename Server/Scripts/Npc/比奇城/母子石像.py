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
		say = """......
			
			[结束:0]"""
	elif (Menu == 100):
		say = """请一定要帮帮我… 啊？太无情了！
			
			[结束:0]"""
	elif (Menu == 101):
		say = """呜呜…… 不久前我的孩子在夜市被商人给抢走了。
			一定要帮我找回孩子啊！
			不知道他把孩子带走到底想干什么……一定要……拜托您了！
			
			[我没有这闲工夫。:102]
			[知道了，我去帮你找回孩子:103]"""
	elif (Menu == 102):
		say = """这样啊……呜呜……天下之大，竟然没有同情失去孩儿母亲心的侠客吗？……
			
			[结束:0]"""
	elif (Menu == 103):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==56):
			PlayerSetV(Sender,BV_NQ_MAIN,57)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """多谢了……听说夜市的商人在 452 : 297 ，请一定要帮我找回孩子啊！
				
				[结束:0]"""
	elif (Menu == 104):
		say = """多谢了……听说夜市的商人在 452 : 297 ，请一定要帮我找回孩子啊！
			
			[结束:0]"""
	elif (Menu == 105):
		say = """啊…这样啊…呜呜- 难道那个商人已经把我那可怜的孩子给卖了吗？呜呜……
			
			[不过倒是听说那个商人最近得到了一块童子模样的寿石。:106]"""
	elif (Menu == 106):
		say = """哦? 童子模样的寿石? 对！那个寿石就是我孩子啊！！ 
			拜托您一定要帮我找回那个寿石啊！！！
			
			（这是怎么回事？说石头是自己的孩子？）
			
			[对不起，我有点不太明白你说的话。:107]"""	
	elif (Menu == 107):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==59):
			PlayerSetV(Sender,BV_NQ_MAIN,60)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """现在还不能为你解释！
				不管怎么样，那个寿石就是我的孩子！
				帮我找回那个寿石我一定不忘您的大恩大德。
				请帮我把它找回来吧！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==56):
			say = """这位侠客，请一定要帮帮我啊！
				
				[（装作没看见走过去）:100]
				[什么事情啊？:101]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==57):
			say = """听说夜市的商人在 452 : 297 ，请一定要帮我找回孩子啊！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==58):
			say = """还没有找到我孩子吗?
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==59):
			say = """还没有找到我孩子吗?
				
				[很遗憾，现在连一点线索都还没找到。:105]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==60):
			say = """还没有找到我孩子吗?
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==61):
			if(Sender.GetItemCount('童子像') < 1):
				say = """还没有找到我孩子吗?
					
					[结束:0]"""
			else:
				Sender.TakeItem('童子像',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊啊, 终于找回我的孩子了。真是太感谢了。这个虽然微薄，但也是我的一片心意！
					
					[结束:0]"""
		else:
			say = """（这石头的样子真奇怪......）
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(263,"OnClick",OnClick)
