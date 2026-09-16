# -*- coding: utf-8 -*-
#载入模块SYS引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import 额外奖励 as ExtraRewards
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import random
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
	say = "" 

	if (Menu == 1):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("万事通江湖任务")
		NPCObject = ServerUtils.GetNPCObject(294)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.万事通江湖任务.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"
	elif (Menu == 2):
		if(Sender.Level < 25):
			say = """你还不够强大，当你等级达到25级时再来吧。
			
			[结束:0]"""
		elif Sender.HasDaily:
			say = """你当前的每日任务还没做完呢！
			
			[结束:0]"""
		elif Sender.RemainingDailyCount < 1:
			say = """今天已经没有任务给你了，请明天再来
			
			[结束:0]"""
		else:
			Sender.GetDailyQuest()
			say = """任务给你了，打开任务界面查看
			
			[结束:0]"""
	elif (Menu == 3):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("万事通每日随机任务")
		NPCObject = ServerUtils.GetNPCObject(295)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.万事通每日任务.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"
	else:
		say = """江湖上的朋友都叫我万拍子。
			不是我吹，你不了解的武功或其它的任务我都可以给你解答。
			你有什么想问的吗？
			
			[询问一般的任务:1] （江湖任务）
			
			[对今日的任务进行了解:2]  （每日任务）
			
			[领取每日随机任务:3]  (随机任务)

			<font color=\"0xff00ff00\">特别说明:每日随机任务可以重置，但是重置需要花费不少钱哦！！</font>
			
			[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(50,"OnClick",OnClick)
NpcEvent.add_listener(75,"OnClick",OnClick)
NpcEvent.add_listener(79,"OnClick",OnClick)
NpcEvent.add_listener(123,"OnClick",OnClick)
NpcEvent.add_listener(130,"OnClick",OnClick)
