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
				player.Connection.ReceiveChat("爆打校长爆棒棒糖活动将于21点比奇城开始，请玩家集合！", MessageType.System)
				player.Connection.ReceiveChat("爆打校长爆棒棒糖活动将于21点比奇城开始，请玩家集合！", MessageType.System)
				player.Connection.ReceiveChat("爆打校长爆棒棒糖活动将于21点比奇城开始，请玩家集合！", MessageType.System)

def TestSpawn2(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("比奇城出现大量老校长，请玩家速度集合击杀！", MessageType.System)
				player.Connection.ReceiveChat("比奇城出现大量老校长，请玩家速度集合击杀！", MessageType.System)
				player.Connection.ReceiveChat("比奇城出现大量老校长，请玩家速度集合击杀！", MessageType.System)
				
		ServerUtils.SpawnMonsters("比奇城", "老校长", 20, 209, 249, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长", 20, 370, 497, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长", 20, 554, 499, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长", 20, 649, 250, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长", 20, 414, 97, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长77", 80, 209, 249, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长77", 80, 370, 497, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长77", 80, 554, 499, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长77", 80, 649, 250, 500)
		ServerUtils.SpawnMonsters("比奇城", "老校长77", 80, 414, 97, 500)
		return