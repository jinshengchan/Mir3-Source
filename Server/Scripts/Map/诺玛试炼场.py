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

def OnEnter(args):            #进入
	map = args[0]
	Sender = args[1]
	Sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.诺玛试炼场.CloseFuben",60,(map,Sender))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=1);  #副本地图关卡时间设置
	#map.CreateMon(12,12,5,100413,1)
	#map.CreateMon(12,12,5,100414,1)
	#map.CreateMon(12,12,5,100415,1)
	#map.CreateMon(12,12,5,100416,1)
	map.CreateMon(12,12,5,100417,1)
	MonsterCount((map,Sender,))

def CloseFuben(args):            #关闭副本
	map = args[0]
	Sender = args[1]
	
	#传送玩家到进入地图的随机坐标
	index = PlayerGetV(Sender,GV_PLAYER_NMDIEMAP)
	map1 = SEnvir.GetMap(index)  # 要传送的地图
	randomLocation = map1.GetRandomLocation()      #取随机数坐标值
	if(index != 0 and Sender.CurrentMap == map):
		#X = PlayerGetV(Sender,GV_PLAYER_DIEMAPX)
		#Y = PlayerGetV(Sender,GV_PLAYER_DIEMAPY)
		Sender.TeleportByMapIndex(index,randomLocation.X, randomLocation.Y)
	#Sender.TeleportByMapIndex(33, 181, 136) #传送玩家到诺玛村庄
	
	if Server.Envir.SEnvir.FubenMaps.Contains(map):
		Server.Envir.SEnvir.CloseMap(map)
		Server.Envir.SEnvir.FubenMaps.Remove(map)
	
def MonsterCount(args):         #怪物总数
	map = args[0]
	Sender = args[1]
	inmap = Server.Envir.SEnvir.GetMap(map.Info)  # 判断地图是否存在
	
	try:
		if Sender.CurrentMap != map:
			return
		map.MapMsg("地图剩余怪物"+'%d'%map.MonsterCount,MessageType.System)
		Server.Envir.SEnvir.DelayCall("Map.诺玛试炼场.MonsterCount",3,(map,Sender,))
	except Exception as ex:
		SEnvir.Log("出现如下异常%s"%ex)
		return
	
MapEvent.add_listener(569,"OnEnter",OnEnter)