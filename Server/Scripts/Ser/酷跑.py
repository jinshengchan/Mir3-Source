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
from Utils.PlayerUtils import *

def doublePKTZ(begin):
	if begin:
		ServerUtils.SendMsgToAll("十五分钟后酷跑活动开始，请玩家届时到比奇活动管理员直接传送到活动地图！", MessageType.System)
		ServerUtils.SendMsgToAll("十五分钟后酷跑活动开始，请玩家届时到比奇活动管理员直接传送到活动地图！", MessageType.System)
		ServerUtils.SendMsgToAll("十五分钟后酷跑活动开始，请玩家届时到比奇活动管理员直接传送到活动地图！", MessageType.RollNotice)
		return
	else:
		ServerUtils.SendMsgToAll("剩余一分钟酷跑活动开始，请玩家届时到比奇活动管理员直接传送到活动地图！", MessageType.System)
		ServerUtils.SendMsgToAll("剩余一分钟酷跑活动开始，请玩家届时到比奇活动管理员直接传送到活动地图！", MessageType.System)
		ServerUtils.SendMsgToAll("剩余一分钟酷跑活动开始，请玩家届时到比奇活动管理员直接传送到活动地图！", MessageType.RollNotice)
		return

def doublePK(begin):
	if begin:
		ServerUtils.SendMsgToAll("酷跑活动开始，比奇密道刷新大量宝箱！", MessageType.System)
		ServerUtils.SendMsgToAll("酷跑活动开始，比奇密道刷新大量宝箱！", MessageType.System)
		ServerUtils.SendMsgToAll("酷跑活动开始，比奇密道刷新大量宝箱！", MessageType.RollNotice)
		GlobalSetV(GV_PLAYER_LIUYIPAOKUCOUNT,0)  #奖励全局变量复位
		pkmap = SEnvir.GetMap(562)      #获取比赛等待地图
		to_be_teleported = []
		for player in pkmap.Players:    #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:
			if (player.GroupMembers):   
				player.GroupLeave()  #如果判断有组，那么直接退出队伍在进入
			if (player.Equipment[int(EquipmentSlot.Fashion)] and ((player.Equipment[EQUIPMENT_SLOTS['时装']].Info.ItemName == '滑板（男）') or (player.Equipment[EQUIPMENT_SLOTS['时装']].Info.ItemName == '滑板（女）'))):
				PlayerSetV(player,GV_PLAYER_LIUYIPAOKU,1)
				player.TeleportByMapIndex(563, 243, 254)   #把玩家传送到比赛地图内
		
		ServerUtils.SpawnMonsters("比奇密道", "宝箱", 300, 148, 148, 5000)
		return
	else:
		ServerUtils.SendMsgToAll("酷跑活动结束，谢谢所有玩家的参与！", MessageType.System)
		ServerUtils.SendMsgToAll("酷跑活动结束，谢谢所有玩家的参与！", MessageType.System)
		ServerUtils.SendMsgToAll("酷跑活动结束，谢谢所有玩家的参与！", MessageType.RollNotice)
		pkmap = SEnvir.GetMap(563)     #获取比赛地图信息
		to_be_teleported = []
		for player in pkmap.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:
			player.TeleportByMapIndex(1,469,378)   #把玩家传送回比奇
			
		pkmap.ClearAllMonsters()    #清理掉刷出来的怪物
		return


