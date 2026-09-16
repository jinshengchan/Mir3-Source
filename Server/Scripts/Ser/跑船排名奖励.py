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
		dicyihou = GlobalGetObV(GV_PLAYER_PAOCHUANSHAGUAICOUNT)
		
		if dicyihou is None:
			dicyihou1 = {}
			GlobalSetObV(GV_PLAYER_PAOCHUANLINGQU, dicyihou1)
			return
		else:
			a1 = sorted(dicyihou.items(),key = lambda x:x[1],reverse = True)
			dicyihou1 = {}
			for i in range(len(a1)):
				if i >= 10:
					break
				dicyihou1[a1[i][0]] = 1
			GlobalSetObV(GV_PLAYER_PAOCHUANLINGQU, dicyihou1)
		dicyihou = {}
		GlobalSetObV(GV_PLAYER_PAOCHUANSHAGUAICOUNT,dicyihou)
		
		#清理一层的玩家
		sbkmap1 = SEnvir.GetMap(554)     #获取地图信息
		to_be_teleported = []
		for player in sbkmap1.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:       #遍历地图玩家
			player.TeleportByMapIndex(1,449,390)   #把玩家传送回比奇
		#清理二层的玩家
		sbkmap2 = SEnvir.GetMap(555)     #获取地图信息
		to_be_teleported = []
		for player in sbkmap2.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:       #遍历地图玩家
			player.TeleportByMapIndex(1,449,390)   #把玩家传送回比奇
		#清理三层的玩家
		sbkmap3 = SEnvir.GetMap(556)     #获取地图信息
		to_be_teleported = []
		for player in sbkmap3.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:       #遍历地图玩家
			player.TeleportByMapIndex(1,449,390)   #把玩家传送回比奇
		#清理四层的玩家
		sbkmap4 = SEnvir.GetMap(557)     #获取地图信息
		to_be_teleported = []
		for player in sbkmap4.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:       #遍历地图玩家
			player.TeleportByMapIndex(1,449,390)   #把玩家传送回比奇
		return
