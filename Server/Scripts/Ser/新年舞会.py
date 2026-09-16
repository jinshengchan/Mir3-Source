# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import datetime
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
import random

def TestSpawn1(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("迎新春新年舞会活动将于十分钟后开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新春新年舞会活动将于十分钟后开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新春新年舞会活动将于十分钟后开启！", MessageType.System)
		return

def TestSpawn2(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("迎新春新年舞会活动开启，请玩家前往皇宫大厅参加活动！", MessageType.System)
				player.Connection.ReceiveChat("迎新春新年舞会活动开启，请玩家前往皇宫大厅参加活动！", MessageType.System)
				player.Connection.ReceiveChat("迎新春新年舞会活动开启，请玩家前往皇宫大厅参加活动！", MessageType.System)
		#刷新舞娘
		map = SEnvir.GetMap(2)
		map.CreateNpc(22,48,377)
		map.CreateNpc(23,47,377)
		map.CreateNpc(24,46,377)
		map.CreateNpc(25,45,377)
		map.CreateNpc(26,44,377)
		map.CreateNpc(27,43,377)
		map.CreateNpc(31,47,377)
		map.CreateNpc(30,48,377)
		map.CreateNpc(29,49,377)
		map.CreateNpc(28,50,377)
		map.CreateNpc(27,51,377)
		map.CreateNpc(26,52,377)
		map.CreateNpc(41,30,378)
		map.CreateNpc(40,31,378)
		map.CreateNpc(39,32,378)
		map.CreateNpc(38,33,378)
		map.CreateNpc(37,34,378)
		map.CreateNpc(36,35,378)
		map.CreateNpc(35,36,378)
		map.CreateNpc(34,37,378)
		map.CreateNpc(33,38,378)
		map.CreateNpc(43,32,378)
		map.CreateNpc(42,33,378)
		map.CreateNpc(41,34,378)
		map.CreateNpc(40,35,378)
		map.CreateNpc(39,36,378)
		map.CreateNpc(38,37,378)
		map.CreateNpc(37,38,378)
		map.CreateNpc(36,39,378)
		map.CreateNpc(35,40,378)
		return
	else:
		map = SEnvir.GetMap(2)
		cell = map.Cells[22,48]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[23,47]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[24,46]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[25,45]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[26,44]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[27,43]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[31,47]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[30,48]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[29,49]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[28,50]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[27,51]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[26,52]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[41,30]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[40,31]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[39,32]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[38,33]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[37,34]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[36,35]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[35,36]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[34,37]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[33,38]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[43,32]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[42,33]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[41,34]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[40,35]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[39,36]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[38,37]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[37,38]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[36,39]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[35,40]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		return

def TestSpawn3(begin):
	if begin:
		#触发获得经验，每1分钟一次
		map = SEnvir.GetMap(2)      #获取活动地图
		to_be_teleported = []
		for player in map.Players:    #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:
			GiveExperience(player,100000)    #给每个人10万经验
			player.Connection.ReceiveChat("获得经验100000",MessageType.System)

def TestSpawn4(begin):  #触发刷神水使者，每3分钟一次
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("大厅出现大量舞会帮工，大家小心！", MessageType.System)
		ServerUtils.SpawnMonsters(2, 100347, 50, 36, 36, 50) #刷怪 地图名 怪物名 数量 X Y 范围
		return

def TestSpawn5(begin):  #触发刷神水使者1 2
	if begin:
		ServerUtils.SpawnMonsters(2, 100360, 1, 36, 36, 50) #刷怪 地图名 怪物名 数量 X Y 范围
		ServerUtils.SpawnMonsters(2, 100484, 1, 36, 36, 50) #刷怪 地图名 怪物名 数量 X Y 范围
		return

