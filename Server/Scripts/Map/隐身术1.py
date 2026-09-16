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
	Server.Envir.SEnvir.DelayCall("Map.隐身术1.CloseFuben",300,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	select = random.randint(0,100)
	if select < 20:
		map.CreateMon(40,66,50,'沃玛勇士11',10)
		map.CreateMon(66,40,50,'火焰沃玛11',5)
	elif select < 50:
		map.CreateMon(40,66,50,'沃玛勇士11',5)
		map.CreateMon(66,40,50,'火焰沃玛11',10)
	else:
		map.CreateMon(40,66,50,'雷电僵尸',10)
		map.CreateMon(66,40,50,'沃玛勇士11',5)
	MonsterCount((map,Sender,))
	
def CloseFuben(args):            #关闭副本
	map=args[0]
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
		if map.MonsterCount < 15:
			PlayerSetV(Sender,GV_Taoist_Invisibility,1)
			Sender.TeleportByMapIndex(9,12,13)
			return Sender.NPCCall(31, True)  #调用对应的NPC
		#map.MapMsg("地图剩余怪物"+'%d'%map.MonsterCount,MessageType.System)
		Server.Envir.SEnvir.DelayCall("Map.隐身术1.MonsterCount",3,(map,Sender,))
	except Exception as ex:
		SEnvir.Log("出现如下异常%s"%ex)
		return

MapEvent.add_listener(17,"OnEnter",OnEnter)
