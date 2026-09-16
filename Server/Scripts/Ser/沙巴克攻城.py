# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
from datetime import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils


def TestSpawn1(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("一个小时后沙巴克攻城战就会开始。", MessageType.System)
				player.Connection.ReceiveChat("一个小时后沙巴克攻城战就会开始。", MessageType.System)
				player.Connection.ReceiveChat("一个小时后沙巴克攻城战就会开始。", MessageType.System)
				player.Connection.ReceiveChat("兵器商出现在沙巴克，勇士们可以提前备战。", MessageType.System)
		#刷新兵器商
		map = SEnvir.GetMap(25)
		map.CreateNpc(72,161,106)
		map.CreateNpc(302,513,103)
		map.CreateNpc(169,158,93)
		#重置门的血量和方向
		GlobalSetV(GV_MON_SBKCMHP1, 0)      #沙巴克城门1血量记录
		GlobalSetV(GV_MON_SBKCMON1, 0)      #沙巴克城门1开关状态记录
		GlobalSetV(GV_MON_SBKCMHP3, 0)      #沙巴克城门3血量记录
		GlobalSetV(GV_MON_SBKCMON3, 0)      #沙巴克城门4血量记录
		GlobalSetV(GV_MON_SBKCMON4, 0)      #沙巴克城门4开关状态记录
		return

def TestSpawn2(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("半小时后沙巴克攻城战就会开始。", MessageType.System)
				player.Connection.ReceiveChat("半小时后沙巴克攻城战就会开始。", MessageType.System)
				player.Connection.ReceiveChat("半小时后沙巴克攻城战就会开始。", MessageType.System)
		return

def TestSpawn3(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("十分钟后沙巴克攻城战就会开始。", MessageType.System)
				player.Connection.ReceiveChat("十分钟后沙巴克攻城战就会开始。", MessageType.System)
				player.Connection.ReceiveChat("十分钟后沙巴克攻城战就会开始。", MessageType.System)
		return

def TestSpawn4(begin):
	if begin:
		flag = True
		for castle in SEnvir.CastleInfoList.Binding:
			if castle is not None and castle.Name == '沙巴克':
				flag = False
				break
		if flag:
			SEnvir.Log("没有找到攻城设置城堡")
			return
		if SEnvir.ConquestWars.Count > 0: #在攻城中
			SEnvir.Log("已经开启攻城")
			return
		Server.Models.ConquestWar.StartConquestWar(castle, True)

		#开始攻城 把门刷出来
		map = SEnvir.GetMap(25)
		cell = map.Cells[234,191]
		map.CreateMon(234,191,0,'沙巴克城门1',1)
		map.CreateMon(169,191,0,'沙巴克城门3',1)
		map.CreateMon(234,127,0,'沙巴克城门4',1)
		for object in cell.Objects:
			if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530:
				object.Direction = object.CurrentDir
				objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
				objcetTurn.ObjectID = object.ObjectID
				objcetTurn.Direction = object.Direction
				objcetTurn.Location =  object.CurrentLocation
				object.Broadcast(objcetTurn)
				map.CreateNpc(234,190,344)
				map.CreateNpc(233,191,344)
				map.CreateNpc(235,190,344)
				map.CreateNpc(168,190,344)
				map.CreateNpc(170,191,344)
				map.CreateNpc(169,190,344)
				map.CreateNpc(232,127,344)
				map.CreateNpc(233,127,344)
				map.CreateNpc(234,128,344)

		return
	else:
		#结束判断
		if SEnvir.ConquestWars.Count > 0: #在攻城中
			flag = True
			for castle in SEnvir.CastleInfoList.Binding:
				if castle is not None and castle.Name == '沙巴克':
					flag = False
					break
			if flag:
				SEnvir.Log("没有找到攻城设置城堡")
				return
			if SEnvir.ConquestWars.Count == 0: #在攻城中
				SEnvir.Log("没有攻城")
				return
			for war in SEnvir.ConquestWars:
				if war.info == castle:
					war.EndTime = datetime.min
			Server.Models.ConquestWar.EndConquestWar(castle, True)

		#兵器商清除
		map = SEnvir.GetMap(25)
		cell = map.Cells[72,161]          #左上定国位置
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[302,513]         #右下定国位置
		if cell.Objects != None:
			for object in reversed(cell.Objects): 
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[169,158]         #沙城里兵器商位置
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()

		#攻城结束 沙巴克置为GM行会
		#SEnvir.ReassignCastleToGuild("GM", "沙巴克")

		return