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
#红名-传送流放岛	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
		
		[关闭:0]"""
#跳转菜单1仓库				
	elif (Menu == 1):
		MainQuestRewards(Sender)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """云发先生平安无事啊！担心死我了，真是万幸啊！
这儿比较安全，我马上就去把他接过来！

[云发先生也正在等着你呢！:0]"""
	elif (Menu == 2):
		say = """那就拜托啦！
遇到他的话就告诉他我在这儿！


[结束:0]"""

	elif(PlayerGetV(Sender,BV_NQ_MAIN)==92):
		say = """我是来这里调查矿产分布的学者的助手兼护卫武士。
但是由于应付怪兽的袭击把学者先生给丢了！
到底在哪呢？……千万不要出什么事儿啊！

[告诉嘉登关于云发先生的情况:1]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==93):
		say = """云发先生平安无事，这真是万幸啊！

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN) > 93):
		say = """云发先生平安无事，这真是万幸啊！

[结束:0]"""
#主菜单
	else:
		say = """我的名字是嘉登。 我虽然是名不见经传的浪人，但是只用钱是收买不了我的。

[结束:0]"""


	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(270,"OnClick",OnClick)