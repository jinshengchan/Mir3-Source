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
		say = """这声音……咦……你是谁啊？
			哦！不不，我好像认识你啊！我听到了你在洞穴中的话。打败半兽勇士得到不死牌的不就是你吗？ 
			
			[你是怎么知道的？:2]"""
	elif (Menu == 2):
		say = """我都听见了，我在葫芦瓶里全都……那个坏道士和你的话我全都听见了！
			
			[你说是在葫芦瓶里？:3]"""
	elif (Menu == 3):
		say = """我骑着马在散步的时候那个道士出现了。
			我一眼就看出那个道士没安什么好心眼儿，就骑着马慌忙逃跑，可是还是在半兽洞穴附近被抓到了。
			那个家伙念了些什么奇怪的咒语我就被装进了葫芦瓶。不知多久后我才知道被关进了葫芦瓶里！
			
			[原来你的灵魂被装进了葫芦瓶里啊！:4]"""
	elif (Menu == 4):
		say = """对！他看起来好像是要拿我的灵魂做某种实验。我在葫芦瓶里听到的话很多，可是我的见识太少一句都听不明白！
			不过现在倒是明白了一点儿，那家伙好像为了去做什么事儿把这个葫芦瓶扔下离开了。因为要得到更贵重的东西，所以不需要这个了~！
			
			[那是什么呢？:5]"""
	elif (Menu == 5):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==125):
			PlayerSetV(Sender,BV_NQ_MAIN,126)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """不死牌！
				那个混蛋道士所觊觎的东西就是 不死牌 。
				通过和您的对话得知了不死牌下落的那个道士，现在正要潜入衙门去盗取不死牌呢！
				如果让他得逞的话又不知会发生什么样的灾难呢，所以赶快去衙门看看吧！
				
				[结束:0]"""
	elif (Menu == 4):
		say = """对！他看起来好像是要拿我的灵魂做某种实验。我在葫芦瓶里听到的话很多，可是我的见识太少一句都听不明白！
			不过现在倒是明白了一点儿，那家伙好像为了去做什么事儿把这个葫芦瓶扔下离开了。因为要得到更贵重的东西，所以不需要这个了~！
			
			[那是什么呢？:5]"""
#主菜单
	else:
		if(108 < PlayerGetV(Sender,BV_NQ_MAIN) < 125):
			say = """......
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==125):
			say = """嗯... 嗯...
				
				[王小姐，你醒过来了吗？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) > 125):
			say = """谢谢你帮助我啊！
				
				[结束:0]"""
		else:
			say = """......
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(260,"OnClick",OnClick)
