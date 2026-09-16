# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import MapEvent
import random
from Defines import *
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from Map.进门条件列表 import *
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
	map = SEnvir.GetMap(Sender.Character.CurrentMap)
	Dict={}
#跳转菜单1
	if map.MonsterCount > 0:
		say = """呵呵呵，不知天高地厚的家伙！
			
			[结束:0]"""
	elif (Menu == 1):
		if(Sender.GetItemCount('灵魂明珠') < 1):
			say = """难道您不知道灵魂明珠的去向吗？
				
				[结束:0]"""
		else:
			say = """我是道馆的道士。听说您在寻找破坏灵魂明珠的办法，所以特地赶来帮助你的。
				
				[哦……是这样啊！:2]"""
	elif (Menu == 2):
		say = """那个灵魂明珠是非常危险的东西，我要把它带回道馆和众位道友用道力来净化一下。把那个灵魂明珠交给我吧！
			
			[好的。:3]"""
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==166):
			if(Sender.GetItemCount('灵魂明珠') < 1):
				say = """好像您没有带着灵魂明珠啊！
				
				[结束:0]"""
			else:
				Sender.TakeItem('灵魂明珠',1)
				PlayerSetV(Sender,BV_NQ_KILLMON,1)
				PlayerSetV(Sender,BV_NQ_KILLNUM,0)
				PlayerSetV(Sender,BV_NQ_MAIN,167)
				if map.MonsterCount > 0:
					map.ClearAllMonsters()
				map.CreateMon(17,19,8,100035,6)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """哈哈哈，嘿嘿嘿……得到灵魂明珠了！
				
				[啊！我被骗了！:0]"""
	# elif (Menu == 7):
		# say = """呵呵呵…也曾经是过人……但在伟大的沃玛神赐予我新的不死之躯和强大力量之后，现在……我已经成为了超越人类的存在！！
			
			# [说什么大话啊！我一定要亲手除掉你这个混蛋！:8]"""
	elif (Menu == 8):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==169):
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			if map.MonsterCount > 0:
				map.ClearAllMonsters()
			map.CreateMon(17,19,8,100038,1)
			map.CreateMon(17,19,8,100035,3)
			map.CreateMon(17,19,8,100033,3)
			say = """呵呵呵，不知天高地厚的家伙！
				
				[结束:0]"""
#主菜单
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==166):
		say = """快请进。是带着灵魂明珠的人吧！
			
			[您是谁？:1]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==167):
		PlayerSetV(Sender,BV_NQ_KILLMON,1)
		PlayerSetV(Sender,BV_NQ_KILLNUM,0)
		if map.MonsterCount > 0:
			map.ClearAllMonsters()
		map.CreateMon(17,19,8,100035,6)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """呵呵呵…你这个不知天高地厚的人又来了啊！
			
			[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==168):
		PlayerSetV(Sender,BV_NQ_KILLMON,1)
		PlayerSetV(Sender,BV_NQ_KILLNUM,0)
		if map.MonsterCount > 0:
			map.ClearAllMonsters()
		map.CreateMon(17,19,8,100033,6)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """呵呵呵…你这个不知天高地厚的人又来了啊！
			
			[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==169):
		say = """呵呵呵……被我的力量吓跑的你又回来了啊！
			嘿…让你见识一下超越人类的我的厉害！！
			
			[说什么大话啊！我一定要亲手除掉你这个混蛋！:8]"""
	else:
		say = """......
			
			[结束:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(284,"OnClick",OnClick)
