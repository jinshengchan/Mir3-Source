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
				player.Connection.ReceiveChat("庄园将于20点开启，请玩家点击比奇城心愿树进入！", MessageType.System)
				player.Connection.ReceiveChat("庄园将于20点开启，请玩家点击比奇城心愿树进入！", MessageType.System)
				player.Connection.ReceiveChat("庄园将于20点开启，请玩家点击比奇城心愿树进入！", MessageType.System)

def TestSpawn2(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("各大教主携带大量小怪出现在庄园，请玩家点击比奇城心愿树进入！", MessageType.System)
				player.Connection.ReceiveChat("各大教主携带大量小怪出现在庄园，请玩家点击比奇城心愿树进入！", MessageType.System)
				player.Connection.ReceiveChat("各大教主携带大量小怪出现在庄园，请玩家点击比奇城心愿树进入！", MessageType.System)
				
		ServerUtils.SpawnMonsters("庄园", "祖玛弓箭手", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "祖玛雕像", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "祖玛卫士", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "大老鼠", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜战士", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜冰魔", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜右护卫", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜云魔", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜左护卫", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜风魔", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜火魔", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "东魔神怪", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "猿猴战士", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "猿猴战将", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "巨象兽", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "西魔神怪", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神1", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神2", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "武力神将", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神3", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神4", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "石像狮子", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "武力魔神将", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "火焰狮子", 50, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "祖玛弓箭手8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "祖玛雕像8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "祖玛卫士8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "大老鼠8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜战士8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜冰魔8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜右护卫8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜云魔8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜左护卫8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜风魔8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜火魔8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "东魔神怪8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "猿猴战士8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "猿猴战将8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "巨象兽8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "西魔神怪8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神18", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神28", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "武力神将8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神38", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "地牢女神48", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "石像狮子8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "武力魔神将8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "火焰狮子8", 5, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "尸王5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "蚂蚁将军5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "红甲虫5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "沃玛卫士5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "邪恶钳虫5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "白野猪5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "骨鬼将5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "八角首领5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "大法老5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "神鬼王5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "护法天5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜鬼将5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "疯狂魔神盗5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "震天首将5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "半兽勇士55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "巨型多角虫55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "骷髅精灵55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "尸王55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "蚂蚁将军55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "红甲虫55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "沃玛卫士55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "邪恶钳虫55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "白野猪55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "骨鬼将55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "八角首领55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "大法老55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "神鬼王55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "护法天55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜鬼将55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "疯狂魔神盗55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "震天首将55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "沃玛教主5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "骷髅教主5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "触龙神5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "黑猪王5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "赤月恶魔5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜牛魔王5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "祖玛教主5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "震天魔神5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "僵尸王5", 3, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "沃玛教主55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "骷髅教主55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "触龙神55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "黑猪王55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "赤月恶魔55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "潘夜牛魔王55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "祖玛教主55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "震天魔神55", 1, 188, 183, 500)
		ServerUtils.SpawnMonsters("庄园", "僵尸王55", 1, 188, 183, 500)
		return
	else:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("庄园已经关闭，谢谢玩家参与活动！", MessageType.System)
				player.Connection.ReceiveChat("庄园已经关闭，谢谢玩家参与活动！", MessageType.System)
				player.Connection.ReceiveChat("庄园已经关闭，谢谢玩家参与活动！", MessageType.System)

		#清理人和怪物
		sbkmap = SEnvir.GetMap(553)     #获取地图信息
		to_be_teleported = []
		for player in sbkmap.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:
			player.TeleportByMapIndex(1,451,390)   #把玩家传送回比奇
			
		sbkmap.ClearAllMonsters()    #清理掉刷出来的怪物
		