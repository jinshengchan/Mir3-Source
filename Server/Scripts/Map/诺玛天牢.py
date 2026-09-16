# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
from Defines import *
import random
import NpcEvent
from datetime import datetime, timedelta
import System
s1 = clr.Reference[System.Object]()
from Utils.TimeUtil import *
import Utils.ServerUtils as ServerUtils
from Utils import ServerUtils
from Npc import *

# 此变量设为这个自定义buff的序号
PLAYER_BAOXIANGBUFF_INDEX = 112

def OnEnter(args):            #进入
	map = args[0]
	Sender = args[1]
	Server.Envir.SEnvir.DelayCall("Map.诺玛天牢.RandomPlayer",2,(map,Sender,))   #地图总时间 秒为单位
	
	
def RandomPlayer(args):
	map = args[0]
	Sender = args[1]
	randomLocation = map.GetRandomLocation()      #取随机数坐标值
	try:
		if Sender.CurrentMap != map:
			return
		if Sender.Character.Account.GuildMember is None:
			Sender.TeleportByMapIndex(33,181,135)
			return
		if (map.MonsterCount == 0) and (GlobalGetV(GV_KILLMON_NUOMATIANLAO) == 1):#没有怪物 并且是活动开始了 就开始刷BOSS
			#先把新手行会的直接T出去，赋值已经完成的变量  无行会  行会低于5级得
			if not Sender.Character.Account.TempAdmin and (Sender.Character.Account.GuildMember.Guild.GuildLevel == 0 or Sender.Character.Account.GuildMember is None or Sender.Character.Account.GuildMember.Guild.GuildLevel < 3):
				PlayerSetV(Sender,GV_PLAYER_NUOMATIANLAOYI,1)
				Sender.TeleportByMapIndex(33,181,135)
			#开始刷BOSS
			# flag = False
			# for player in map.Players:
				# if not Sender.Character.Account.TempAdmin and (Sender.Character.Account.GuildMember.Guild != player.Character.Account.GuildMember.Guild):
					# flag = True
					# break
			if map.GetAliveMonsterCount("诺玛巡逻队长") < 1: # and map.PlayerCount >= 50 and flag:
				GlobalSetV(GV_KILLMON_NUOMATIANLAO,2)
				ServerUtils.SpawnMonsters("诺玛天牢", "诺玛巡逻队长", 1, 196, 109, 100)  #刷怪 地图名 怪物名 数量 X Y 范围
				ServerUtils.SpawnMonsters("诺玛天牢", "诺玛巡逻队长77", 1, 196, 109, 100)  #刷怪 地图名 怪物名 数量 X Y 范围
				for player in SEnvir.Players:
					if player:
						player.Connection.ReceiveChat("诺玛巡逻队长出现在诺玛天牢！", MessageType.System)
						player.Connection.ReceiveChat("诺玛巡逻队长出现在诺玛天牢！", MessageType.System)
						player.Connection.ReceiveChat("诺玛巡逻队长出现在诺玛天牢！", MessageType.System)
		
		if (GlobalGetV(GV_KILLMON_NUOMATIANLAO) == 2): #重复判断是否还有新手行会成员
			#再次判断是否还存有新手行会的直接T出去，赋值已经完成的变量   无行会  行会低于5级得
			if not Sender.Character.Account.TempAdmin and (Sender.Character.Account.GuildMember.Guild.GuildLevel == 0 or Sender.Character.Account.GuildMember is None or Sender.Character.Account.GuildMember.Guild.GuildLevel < 3):
				PlayerSetV(Sender,GV_PLAYER_NUOMATIANLAOYI,1)
				Sender.TeleportByMapIndex(33,181,135)
		
		Server.Envir.SEnvir.DelayCall("Map.诺玛天牢.RandomPlayer",2,(map,Sender,))
	except Exception as ex:
		SEnvir.Log("出现如下异常%s"%ex)
		return

def OnLeave(args):            #离开地图
	Map = args[0]
	Sender = args[1]
	
	if (Sender.HasCustomBuff(PLAYER_BAOXIANGBUFF_INDEX)):
		if(Sender.GetItemCount("诺玛宝箱") > 0):
			Sender.TakeItem("诺玛宝箱",1)
			userItem = SEnvir.CreateFreshItem("诺玛宝箱")
			itemOb = System.Activator.CreateInstance(Server.Models.ItemObject)
			itemOb.Item = userItem
			itemOb.Spawn(Map.Info, Sender.CurrentLocation)
			Sender.CustomBuffRemove(PLAYER_BAOXIANGBUFF_INDEX)  #删除夺宝BUFF
			for player in SEnvir.Players:
				if(player is None):
					continue
				player.Connection.ReceiveChat("玩家【{}】离开诺玛天牢，诺玛宝箱掉落。".format(Sender.Name),MessageType.RollNotice)

MapEvent.add_listener(561,"OnEnter",OnEnter)
MapEvent.add_listener(561,"OnLeave",OnLeave)
