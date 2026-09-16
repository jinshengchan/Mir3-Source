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
import MapEvent
import NpcEvent
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
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
	if (Menu == 1):
		say = """好像你误会什么了吧……
			不过反正像你这样的智商不高的人是理解不了的！呵呵呵，我是在建造一个没有痛苦没有战争的人间乐园啊！
			不过你是没有机会在这个乐园生活了！因为你就要死在这儿了！ 
			
			[哼！我可不怕你制造的怪物！:2]"""
	elif (Menu == 2):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==132):
			PlayerSetV(Sender,BV_NQ_MAIN,133)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			if map.MonsterCount > 0:
				map.ClearAllMonsters()
			map.CreateMon(16,13,5,100029,1)
			say = """呵呵呵，你的实力的确超出我的预料！
				所以我也为你特别准备了一下！这次不会让你失望的！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==132):
			say = """又是你？
				
				[你不能马上停止这邪恶勾当吗？:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==133):
			if (map.MonsterCount > 0 ):
				say = """你的对手就是它！
					
					[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,134)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				SEnvir.DelayCall("Map.Teleport.DelayTeleport",10,(Sender,map))
				Sender.Connection.ReceiveChat(" 10 秒后将自动传出本区域。",MessageType.System)
				say = """真是像蟑螂一样生命力顽强的家伙啊！
					不过你最好要明白，现在凭你的力量是不能把我怎么样的！
					
					[结束:0]"""
		else:
			say = """哦？看来你还是蛮有余力啊！
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(280,"OnClick",OnClick)
