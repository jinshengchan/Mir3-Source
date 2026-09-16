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
		say = """那么应该快去找我的助手！虽然不久前我与他离散了，但他是个责任感很强的人，所以如果找不到我的话是不会出去的！ 
			因为我一点儿武功都不会，所以一下子不能从这个地方出去……你替我去找找他行吗？我的助手可能在 半兽天然洞穴 2层 的什么地方。
			
			[好的，我去找一下试试！:2]"""
	elif (Menu == 2):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==91):
			PlayerSetV(Sender,BV_NQ_MAIN,92)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """那就拜托啦！
				遇到他的话就告诉他我在这儿！
				
				[结束:0]"""
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==93):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """唔……看来使半兽人的骷髅复活的魔法和这个地方有着某种联系的可能性确实很大啊！
				那么可能半兽人有自己进入这个地方的办法。是固定的暗语还是特别的钥匙呢……？可能是要有特别的钥匙才行。
				或者…能够进入这个地方的关键好像还是在半兽人那儿……不知您能不能去比奇城城主大人那儿问问有没有半兽人的异常征兆！
				还有，我还要继续留在这儿， 如果还有什么要问的事儿的话，就来有嘉登看守的地方 找我吧！
				
				[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==91):
		say = """什么？你说我的老婆十分担心我？
			可这用魔法锁住的屋子…现在不是顾得上这个的时候……
			嗯，那么就不该在这儿这样费时间了啊！
			
			[那就赶快回去吧！:1]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==92):
		say = """那就拜托啦！
			遇到他的话就告诉他我在这儿！
			
			[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==93):
		say = """好不容易一行人又聚到一起了啊！谢谢啦！
			在半兽洞穴被魔法锁住的屋子……
			唔……魔法……半兽人……幸亏是和我最近研究的领域差不多的……
			
			[知道为什么进不去的理由了吗？:3]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==94):
		say = """或者…能够进入这个地方的关键好像还是在半兽人那儿。
			        不知道带着这种东西的半兽人在其他的地区会不会有什么动静，去比奇城城主大人那儿问问吧！ 
			还有，我还要继续留在这儿，如果还有什么要问的事儿的话，就来有嘉登看守的地方找我吧！
			唉……真想快点结束调查回到我妻子身边啊！ 
			
			[结束:0]"""
#主菜单
	else:
		say = """正在为不死牌该怎么处理的问题而苦恼之中。 虽然比奇城城主想要毁掉它，但岂不是太可惜了？这毕竟是很有研究价值的东西啊！…
			
			[结束:0]"""


	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(268,"OnClick",OnClick)