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
		say = """哦？竟有此等事情，施主可否详细道来呢？
			.......
			噢！听说半兽人以半兽勇士为中心集结势力，可突然间又安静了下来，我正感到十分奇怪呢，原来都是这位年轻的施主您解决的啊！真是了不起啊！
			哦……那个带着灵魂护卫摄人魂魄进行研究的道士偷走了不死牌？
			咳……这个家伙终于闹出了大事儿啊！
			
			[他是谁呢？:2]"""
	elif (Menu == 2):
		say = """首先要说的是……现在我要给施主讲的故事是我们道馆的耻辱，原本不该跟外人说的…所以请您答应老纳，别随便把这些话故意传到其他不相关的人那儿！
			
			[好的，我答应您！:3]"""
	elif (Menu == 3):
		say = """这是很久以前的事儿了！
			有个聪明的年青人进入我们道馆门下。由于才能和悟性十分出众，所以得到了门派中元老们的特别器重。
			甚至到了打算让他做继任馆主的程度。可是谁想到那个家伙加入我们道门却另有居心！他对什么济世求道、 上仙药手之类的东西毫不关心。
			最后他终于不顾禁令拿了几卷古书和灵魂护卫逃走了。
			因此本馆将他开除出门派并且下了追杀令，可是直到现在还没能找到他。那个堕落道士叫 署箭。
			这次的事儿一定是他搞得鬼！
			
			[那么他觊觎的是长生不老的力量？:4]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==127):
			PlayerSetV(Sender,BV_NQ_MAIN,128)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """就是啊！一心想要长生不老的这个家伙完全能做出这种事儿来。
				唉……本来应该是由本馆解决的事儿却引发了如此祸端，贫道真是惭愧至极啊！
				您回比奇省的时候请转告一下，现在本馆将会尽全力帮助解决这件事情的！
				
				[结束:0]"""
	elif (Menu == 5):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==135):
			PlayerSetV(Sender,BV_NQ_MAIN,136)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """知道了！
				我们会继续派人去寻找那家伙有可能的藏身之处，同时研究破解那个不死牌的方法。
				如果再有什么动静的话请继续来告诉我们。
				如果我们这边发现了什么线索也会马上跟比奇省联络的！
				
				[结束:0]"""
	elif (Menu == 6):
		say = """是这样啊……以前施主能够破除困魔咒是因为有半块不死牌在身。
			可是目前署箭那个家伙带着完整的不死牌呆在困魔咒里，如果不破解困魔咒的话是进不去的。
			嗯……不过也不是没有办法的。
			
			[是什么办法呢？:7]"""
	elif (Menu == 7):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==140):
			PlayerSetV(Sender,BV_NQ_MAIN,141)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """贫道得知如果有矿山出现的怪物们中僧侣僵尸骨和雷电僵尸骨的话，或许可以造出破解署箭施下魔法的护身符来！
				虽然很辛苦，但还是请您去矿山找僧侣僵尸骨和雷电僵尸骨来吧！
				
				[结束:0]"""
	elif (Menu == 8):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==143):
			PlayerSetV(Sender,BV_NQ_MAIN,144)
			Sender.GiveItem('毁灭护身符',1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """呼……已经做完了！有了这个就可以破解署箭设下的不死牌困魔咒了。
				一定要让这个我们道门之耻——署箭最后死在不是手下，而是您的手里啊！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==127):
			say = """贫道乃执客院住持书堂玄震！
				请问施主是为何事而来？
				
				[我是来找在比奇省衙门偷走不死牌的那个道士的！:1]"""
		elif(127 < PlayerGetV(Sender,BV_NQ_MAIN) < 135):
			say = """为了抓住署箭那个家伙，我们会紧密配合的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==135):
			say = """啊！署箭那个混蛋家伙做出了这种坏事儿？ 
				
				[那个家伙藏了起来，不知是不是又在准备挑出什么事端呢:5]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==136):
			say = """请去比奇省转告一下吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==140):
			say = """快请进，有什么新的消息吗？ 
				
				[找到了署箭的下落，可由于用不死牌设下了困魔咒而进不去:6]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==141):
			if (Sender.GetItemCount('僧侣僵尸骨') < 1):
				PlayerSetV(Sender,BV_NQ_KILLMON,1)
				PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
				say = """需要僧侣僵尸骨和雷电僵尸骨！
					
					[结束:0]"""
			else:
				Sender.TakeItem('僧侣僵尸骨',1)
				PlayerSetV(Sender,BV_NQ_KILLMON,1)
				PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """找到了僧侣僵尸骨，还需要雷电僵尸骨！
					
					[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==142):
			if (Sender.GetItemCount('雷电僵尸骨') < 1):
				PlayerSetV(Sender,BV_NQ_KILLMON,1)
				PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """需要僧侣僵尸骨和雷电僵尸骨！
					
					[结束:0]"""
			else:
				Sender.TakeItem('雷电僵尸骨',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """嗯……看来需要的东西都带来了啊！
					贫道也已经做好了其他的准备就等着施主来呢！
					现在我要集中精力制造护身符，请施主稍候片刻！
					
					[知道了！:8]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==143):
			say = """嗯……看来需要的东西都带来了啊！
				贫道也已经做好了其他的准备就等着施主来呢！
				现在我要集中精力制造护身符，请施主稍候片刻！
				
				[知道了！:8]"""
		elif(143 < PlayerGetV(Sender,BV_NQ_MAIN) < 146):
			say = """那个家伙是我们道门的羞耻啊！相信施主您会替我们处理他的！
				一定要让这个我们道门之耻——署箭最后死在不是手下，而是您的手里啊！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) > 145):
			say = """一切最后都能够这样真是十分幸运啊！。
				但是还有要拜托施主的事情…… 有关 署箭,那个堕落道士的事儿一定要保守秘密啊。
				
				[结束:0]"""
		else:
			say = """所谓事必归正嘛！一切都会按照它的顺理恢复正常的。
			
			[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(278,"OnClick",OnClick)
