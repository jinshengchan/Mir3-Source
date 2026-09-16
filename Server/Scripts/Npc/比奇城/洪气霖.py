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
		PlayerSetV(Sender,BV_NQ_MAIN,41)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """啊~.. 就那件事儿？呃……又不是我有钱不想给，我只是没钱而已……
			
			[要么去干活偿还，要么就去乞讨来支付住宿费。:11]
			
			[你欠下住宿费就由我来付吧！:12] """
	elif (Menu == 11):
		PlayerSetV(Sender,BV_NQ_MAIN,42)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """这…… 这个无情的世界啊！有了人才有钱，有了钱才有人！
			
			[结束:0]"""
	elif (Menu == 12):
		PlayerSetV(Sender,BV_NQ_MAIN,43)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """虽然我现在落的如此窘境……您却还给我留下最后的自尊，多谢了！
			
			[结束:0]"""
	elif (Menu == 13):
		say = """白花…！也就是说白花她现在还活着！！！
			
			[夫人让我拿这个指环给你看:14] 
			如果你还没有变心的话就让你去找她"""
	elif (Menu == 14):
		if Sender.GetItemCount('玉指环') < 1:
			say = """曾经的海誓山盟怎么能变……！ 
				真不知该如何表达我内心对您的感激之情了！
				啊，可是这个指环您要怎么办呢？这可是我和她的定情信物啊！能还给我吗?
				
				[结束:0]"""
		else:
			Sender.TakeItem('玉指环',1)
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """曾经的海誓山盟怎么能变……！
				真不知该如何表达我内心中对女侠您的感激之情了！
				啊，收下这个吧！这本来是我们家族的传家之宝，但现在已经家门零落还要这传家宝又有什么用呢？
				别谦让，请收下吧！
				
				我收拾一下马上就去！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==40):
			say = """呃.. 什么? 呃啊呃啊……是不是来这儿嘲弄我来了? 呃..
				
				[我受旅馆主人之托而来，听说您在这儿白吃白住了一个多月吧？:1]
				
				[看你醉醺醺的样子……简直就没法儿说话，我还是走吧！:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==41):
			say = """啊~.. 就那件事儿？呃……又不是我有钱不想给，我只是没钱而已……
				
				[要么去干活偿还，要么就去乞讨来支付住宿费。:11]
				
				[你欠下住宿费就由我来付吧！:12] """		
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==43):
			say = """那么就麻烦您帮我垫付一下住店钱吧...
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==44):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """……呃，真是太感谢了！
				我落的如此惨状，过去我也曾是堂堂的商坛主人呢！
				我不能如此厚颜地接受别人的帮助……请收下这个吧！
				只要看到这个，几个还记得我的比奇省商人们会照应你的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==47):
			say = """听说棉布店有一个女子和我是同乡？ 难道……不会的，这是不可能的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==48):
			if (Sender.GetItemCount('玉指环') < 1):
				say = """那个在棉布店工作的女子好像就是我妻子啊！哦…难道没有什么要转交给我的东西吗？
					
					[结束:0]"""
			else:
				say = """天啊, 这个玉指环不是我作为定情信物送给妻子的吗？侠客，请快快告诉我，你是从哪儿得到这个指环的?
					
					[是从棉布店的苏白花夫人那得到的:13]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) > 49):
			say = """虽然我现在落的如此窘境……您却还给我留下最后的自尊，多谢了！
				
				[结束:0]"""
		else:
			say = """我落的如此惨状，过去我也曾是堂堂的商坛主人呢！
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(264,"OnClick",OnClick)
