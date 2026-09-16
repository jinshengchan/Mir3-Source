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
	
	if (Menu == 1):
		say = """呵呵呵…也曾经是过人……但在伟大的沃玛神赐予我新的不死之躯和强大力量之后，现在……我已经成为了超越人类的存在！！

[说什么大话啊！我一定要亲手除掉你这个混蛋！:2]"""		
	elif (Menu == 2):
		map.ClearAllMonsters()
		map.ClearAllItems()
		PlayerSetV(Sender,BV_NQ_KILLMON,1)
		PlayerSetV(Sender,BV_NQ_KILLNUM,0)
		map.CreateMon(17,19,8,100038,1)
		map.CreateMon(17,19,8,100035,3)
		map.CreateMon(17,19,8,100033,3)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """呵呵呵，不知天高地厚的家伙！

[结束。:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==99):
		PlayerSetV(Sender,BV_NQ_MAIN,100)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """（虽然不知道是什么动物的犄角制成的，
			但这明显不是一件寻常的东西。）"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==100):
		if(Sender.GetItemCount('角笛') < 1):
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """（无论如何，没有角笛是无法完成任何事情的。。。
再去野外寻找一下吧。。。）"""
		else:
			Sender.TakeItem('角笛',1)
			MainQuestRewards(Sender)
			map.ClearAllMonsters()
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """（艰难的战斗。 
		无论如何，我们掌握了能使沃玛遗骨复活的魔法的精华部分）"""
		SEnvir.DelayCall("Map.Teleport.DelayTeleport",10,(Sender,map))
		Sender.Connection.ReceiveChat(" 10 秒后将离开当前地图。",MessageType.System)
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==107):
		if(Sender.GetItemCount('半块不死牌') < 1):
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_KILLNUM,0)
			say = """（无论如何，没有前半块不死牌是无法完成任何事情的。。。
再去寻找一下吧。。。）"""
		else:
			Sender.TakeItem('半块不死牌',1)
			MainQuestRewards(Sender)
			map.ClearAllMonsters()
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """（这个巨大的红骷髅到底是什么？
			估计半兽人暂时不具有威胁比奇省的实力。）"""
		SEnvir.DelayCall("Map.Teleport.DelayTeleport",10,(Sender,map))
		Sender.Connection.ReceiveChat(" 10 秒后将离开当前地图。",MessageType.System)
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==145):
		PlayerSetV(Sender,BV_NQ_MAIN,146)
		Sender.GiveItem('不死牌',1)
		say = """（呼~呼~。。。
			刚才太险了。。。
哎~~~
不管怎样，向城主大人报告吧。。。。）"""
		SEnvir.DelayCall("Map.Teleport.DelayTeleport",10,(Sender,map))
		Sender.Connection.ReceiveChat(" 10 秒后将离开当前地图。",MessageType.System)
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==148):
		PlayerSetV(Sender,BV_NQ_MAIN,149)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """（这是什么。。。）"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==153):
		PlayerSetV(Sender,BV_NQ_MAIN,154)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """（一本旧书，上面写满了奇怪的内容。。。）"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==164):
		MainQuestRewards(Sender)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """（这是灵魂明珠吗？...拿去给无名老人看看）"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==167):
		PlayerSetV(Sender,BV_NQ_MAIN,168)
		map.ClearAllMonsters()
		PlayerSetV(Sender,BV_NQ_KILLMON,1)
		PlayerSetV(Sender,BV_NQ_KILLNUM,0)
		map.CreateMon(17,19,8,100033,6)
		say = """呵呵呵…弟兄们啊！收拾了这个家伙吧！

[结束:0]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==168):
		PlayerSetV(Sender,BV_NQ_MAIN,169)
		say = """作为人还是做得不错。

[难道你是说你不是人吗？:1]"""
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==169):
		map.ClearAllMonsters()
		Sender.GiveItem('沃玛神铁锤',1)
		Sender.GiveItem('灵魂明珠',1)
		PlayerSetV(Sender,BV_NQ_MAIN,170)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """（呼~~呼~~~
		嗯，一个锤头？说不定会有用。。。。）"""
		SEnvir.DelayCall("Map.Teleport.DelayTeleport",20,(Sender,map))
		Sender.Connection.ReceiveChat(" 20 秒后将离开当前地图。",MessageType.System)
	elif(PlayerGetV(Sender,BV_NQ_MAIN)==172):
		PlayerSetV(Sender,BV_NQ_MAIN,173)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """（呼~~呼~~~呃~~~

		好强大的恶魔。。。）"""
	elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5003):
		PlayerSetV(Sender,BV_NQ_SJKILL,5004)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		SEnvir.DelayCall("Map.Teleport.DelayTeleport",10,(Sender,map))
		Sender.Connection.ReceiveChat(" 10 秒后将退出地图。",MessageType.System)
		say = """总算解决了，回去找霸王幽灵吧。"""
	elif(PlayerGetV(Sender,BV_NQ_SJKILL)==5008):
		PlayerSetV(Sender,BV_NQ_SJKILL,5009)
		Sender.GiveItem('遗骸',1)
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

NpcEvent.add_listener(277,"OnClick",OnClick)