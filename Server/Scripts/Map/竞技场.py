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
	Server.Envir.SEnvir.DelayCall("Map.竞技场.RandomPlayer",180,(map,Sender,))   #地图总时间 秒为单位
	
def RandomPlayer(args):
	map = args[0]
	Sender = args[1]
	inmap = Server.Envir.SEnvir.GetMap(map.Info)  # 判断地图是否存在
	
	try:
		if Sender.CurrentMap != map:
			return
		random_point = inmap.GetRandomLocation()
		Sender.TeleportByMapIndex(467, random_point.X, random_point.Y)   #把玩家传送到比赛地图内
		Server.Envir.SEnvir.DelayCall("Map.竞技场.RandomPlayer",180,(map,Sender,))
	except Exception as ex:
		SEnvir.Log("出现如下异常%s"%ex)
		return
	
MapEvent.add_listener(467,"OnEnter",OnEnter)

