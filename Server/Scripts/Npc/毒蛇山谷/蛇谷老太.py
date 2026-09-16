# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
import collections
clr.AddReference("Library")
from Library import *
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
	elif(Menu == 1):
		say = """不久前我孙女儿被蛇给咬了。
			可是不知道是被什么蛇给咬了，什么解毒药都不好使啊！虽然现在找了非常贵的药草使病状不再恶化，但不知道还能维持多久……
			一定要帮老人家我的小孙女儿找来药啊！
			
			[好的！:3]"""
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==110):
			PlayerSetV(Sender,BV_NQ_MAIN,111)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """谢谢你能帮助我啊！
				真的非常感谢……
				
				[结束:0]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==113):
			if (Sender.GetItemCount('千年毒蛇胆汁') < 1):
				say = """药呢？药被你藏在哪里了？？？
					
					[结束:0]"""
			else:
				Sender.TakeItem('千年毒蛇胆汁',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """好的！真是太感谢了……
					这个镯子是我的一点儿心意……
					
					[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==110):
			say = """喂！年轻人！
				救人一命胜造七级浮屠，帮我这个老人一个忙吧！
				
				[有什么事儿吗？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==111):
			say = """还没有找到我们珍珍的药啊？ 
				天哪！珍珍啊……珍珍……
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==112):
			say = """还没有找到我们珍珍的药啊？ 
				天哪！珍珍啊……珍珍……
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==113):
			if (Sender.GetItemCount('千年毒蛇胆汁') < 1):
				say = """还没有找到我们珍珍的药啊？ 
					天哪！珍珍啊……珍珍……
					
					[结束:0]"""
			else:
				say = """啊！你说给我们的珍珍把药找来了？
					金中医说服了这个就能救回珍珍的命？呜呜，真是太感谢你了！
					我一辈子都不会忘了你这个年轻人的恩情的！我会日夜为你这个年轻人祈祷祝你好运的！ 
					
					[还是赶快去让珍珍服下这药吧！:4]"""
		else:
			say = """没有看到我的珍珍吗？这孩子到底跑哪儿去了？
				
				[结束:0]"""	
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(281,"OnClick",OnClick)