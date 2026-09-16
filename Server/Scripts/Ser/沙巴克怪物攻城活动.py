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
import re

# 怪物列表
MON_LIST = {	1: [("僵尸王6", 9), ("尸王", 10), ("僵尸王", 1)],
				2: [("沃玛教主6", 9), ("沃玛卫士", 10), ("沃玛教主", 1)],
				3: [("黑猪王6", 9), ("白野猪", 10), ("黑猪王", 1)],
				4: [("触龙神6", 4), ("邪恶钳虫", 10), ("触龙神", 1)],
				5: [("骷髅教主6", 9), ("骨鬼将", 10), ("骷髅教主", 1)],
				6: [("赤月恶魔6", 4), ("神鬼王", 10), ("赤月恶魔", 1)],
				7: [("祖玛教主6", 9), ("护法天", 10), ("祖玛教主", 1)],
				8: [("潘夜牛魔王6", 9), ("潘夜鬼将", 10), ("潘夜牛魔王", 1)],
				9: [("震天魔神6", 9), ("震天首将", 10), ("震天魔神", 1)],
				10: [("霸王教主6", 9), ("霸王守卫", 10), ("霸王教主", 1)],
				11: [("诺玛教主6", 9), ("诺玛突击队长", 10), ("诺玛教主", 1)],
				12: [("霸王教主6", 3), ("诺玛教主6", 3), ("诺玛统领1", 1)],
				}

def TestSpawn1(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("迎新春怪物攻城活动将于十分钟后在沙巴克开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新春怪物攻城活动将于十分钟后在沙巴克开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新春怪物攻城活动将于十分钟后在沙巴克开启！", MessageType.System)
		return

def TestSpawn2(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("迎新春怪物攻城活动在沙巴克火爆开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新春怪物攻城活动在沙巴克火爆开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新春怪物攻城活动在沙巴克火爆开启！", MessageType.System)
		Server.Envir.SEnvir.DelayCall("Ser.沙巴克怪物攻城活动.CheckMon", 1, (0,))
		return

def CheckMon(args):
	wave = args[0]		# 第几波
	map = SEnvir.GetMap(25)
	
	index = wave
	if index == 0:
		index = 1
	monsterList = MON_LIST[index]
	flag = True
	for i in range(len(monsterList)):
		current_boss_name = monsterList[i][0]
		#SEnvir.Log(current_boss_name)
		current_boss_index = SEnvir.GetMonsterInfo(current_boss_name).Index
		if map.GetAliveMonsterCount(current_boss_index) > 0:
			flag = False
			break
	if flag: #True说明没有怪物 则 刷怪
		wave = wave + 1
		#如果不存在的层数则退出
		if not MON_LIST.has_key(wave):
			#SEnvir.Log("123")
			return
		monsterList = MON_LIST[wave]
		for i in range(len(monsterList)):
			#副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(206, 159, 50, monsterList[i][0], monsterList[i][1])
		#去除数字显示
		BroadChat("{}携带大量精英出现在沙巴克城！".format(re.split('\d+$',MON_LIST[wave][2][0])[0]), MessageType.System)
		BroadChat("{}携带大量精英出现在沙巴克城！".format(re.split('\d+$',MON_LIST[wave][2][0])[0]), MessageType.System)
		BroadChat("{}携带大量精英出现在沙巴克城！".format(re.split('\d+$',MON_LIST[wave][2][0])[0]), MessageType.System)

	Server.Envir.SEnvir.DelayCall("Ser.沙巴克怪物攻城活动.CheckMon", 5, (wave,))
		


