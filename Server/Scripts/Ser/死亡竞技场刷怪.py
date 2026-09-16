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


def TestSpawn1(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("毒蜘蛛", 10),("掷斧骷髅", 10),]
		# 随机点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn2(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("雷电僵尸", 15),("暗黑战士", 15),]
		# 随机点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn3(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("骷髅弓箭手", 15),("黑色恶蛆", 15),]
		# 定点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn4(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("祖玛弓箭手", 30),]
		# 定点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn5(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("潘夜左护卫", 15),]
		# 定点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn6(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("潘夜右护卫", 15),]
		# 随机点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn7(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("武力神将", 15),]
		# 随机点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn8(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("火焰狮子", 15),]
		# 随机点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return

def TestSpawn9(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("死亡竞技场出现大量怪物，大家小心！", MessageType.System)

		monList = [("白野猪", 2),]
		# 随机点刷
		for mon in monList:
			ServerUtils.SpawnMonsters("死亡竞技场", mon[0], mon[1], 24, 25, 100)
			# ServerUtils.SpawnMonsters("高级死亡竞技场", mon[0], mon[1], 24, 25, 100)
		return


