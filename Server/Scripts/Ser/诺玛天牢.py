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

# 此变量设为这个自定义buff的序号
PLAYER_BAOXIANGBUFF_INDEX = 112

def TestSpawn1(begin):
	if begin:
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛总魔将", 40, 196, 109, 500)  #刷怪 地图名 怪物名 数量 X Y 范围
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛装甲魔将", 40, 196, 109, 500)
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛少将", 40, 196, 109, 500)
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛法老召唤兵", 40, 196, 109, 500)
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛司令大法师", 40, 196, 109, 500)
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛装甲魔将55", 3, 196, 109, 500)
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛少将55", 3, 196, 109, 500)
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛法老召唤兵55", 3, 196, 109, 500)
		ServerUtils.SpawnMonsters("诺玛天牢", "诺玛司令大法师55", 3, 196, 109, 500)
		GlobalSetV(GV_KILLMON_NUOMATIANLAO,1)
		return
	else:
		GlobalSetTempV(GV_NUOMATIANLAO_GUILD_ID,None)  #清空参与奖励变量
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("诺玛天牢关闭，谢谢玩家参与活动！", MessageType.System)
				player.Connection.ReceiveChat("诺玛天牢关闭，谢谢玩家参与活动！", MessageType.System)
				player.Connection.ReceiveChat("诺玛天牢关闭，谢谢玩家参与活动！", MessageType.System)
		sbkmap = SEnvir.GetMap(561)     #获取地图信息
		sbkmap.ClearAllMonsters()    #清理掉刷出来的怪物
		to_be_teleported = []
		for player in sbkmap.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:       #遍历地图玩家
			if (player.HasCustomBuff(PLAYER_BAOXIANGBUFF_INDEX)):
				continue
			player.TeleportByMapIndex(33,181,135)   #把玩家传送回诺玛
