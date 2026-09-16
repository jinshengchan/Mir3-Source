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
import random
from Defines import *
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from 主线任务奖励 import *
from Map.Battle import *
from Map.攻杀剑法 import *
import time
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
	map = SEnvir.GetMap(Sender.Character.CurrentMap)
	
	if(PlayerGetV(Sender,BV_NQ_SJKILL)==5003):
		PlayerSetV(Sender,BV_NQ_SJKILL,5004)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		SEnvir.DelayCall("Map.Teleport.DelayTeleport",10,(Sender,map))
		Sender.Connection.ReceiveChat(" 10 秒后将退出地图。",MessageType.System)
		say = """总算解决了，回去找霸王幽灵吧。"""
	elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5008):
		PlayerSetV(Sender,BV_NQ_SJKILL,5009)
		if (GetInventoryCount(Sender) >= 1):
			Sender.GiveItem('遗骸',1)
		else:
			Sender.PYMailSend("任务", "系统", "邮件发送任务道具", [('遗骸',1,False)])
			Sender.Connection.ReceiveChat("由于你的包裹没有空间，任务道具已发送邮件！", MessageType.System)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """（梅山侠的朋友终于可以得到安息了……
		咦，这是什么东西？遗骸？）"""
	elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5012):
		PlayerSetV(Sender,BV_NQ_SJKILL,5013)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = ''
	else:
		say = """（可以回去交差了。）
		
		[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(368,"OnClick",OnClick)