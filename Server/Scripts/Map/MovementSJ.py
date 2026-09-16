# -*- coding: utf-8 -*-
#载入模块SYS
from datetime import datetime, timedelta
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import MapEvent
import NpcEvent
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from Map.进门条件列表 import *
from 主线任务奖励 import *
#此脚本为目标地图为任务地图，即默认不刷怪的地图（因为进入地图后会清除目标地图的所有怪物）
def OnMovement(args):
	Movement = args[0]
	Sender = args[1]      #玩家
	destMap = Movement.DestinationRegion.Map     #目标地图，要去的地图
	currentMap = Movement.SourceRegion.Map  #当前地图
	mapt = destMap.Index       #目标地图Index
	PlayerSetV(Sender,BV_MAP_TARGET,mapt)
	map = SEnvir.GetMap(destMap)
	mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
	mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(265)
	mynpc.NPCCall(Sender)
	return False

MapEvent.add_listener(560,"OnMovement",OnMovement)           #神舰出门560