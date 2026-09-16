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
	Server.Envir.SEnvir.DelayCall("Map.施毒术.CloseFuben",300,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	map.CreateMon(5,14,10,'毒蜘蛛61',5)
	map.CreateMon(5,14,10,'食人花61',5)
	map.CreateMon(5,14,10,'蝎子61',5)
	map.CreateMon(5,14,10,'洞蛆61',5)
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
		if (Sender.GetItemCount("蛆卵") > 0) and (Sender.GetItemCount("蝎子的尾巴") > 0) and (Sender.GetItemCount("食人花树叶") > 0) and (Sender.GetItemCount("食人花果实") > 0) and (Sender.GetItemCount("毒蜘蛛牙齿") > 0):
			PlayerSetV(Sender,GV_Taoist_PoisonDust,2)
			Sender.TeleportByMapIndex(9,9,13)
			return Server.Envir.SEnvir.DelayCall("Map.施毒术.DelayCall",1,(Sender,))
		map.MapMsg("地图剩余怪物"+'%d'%map.MonsterCount,MessageType.System)
		Server.Envir.SEnvir.DelayCall("Map.施毒术.MonsterCount",3,(map,Sender,))
	except Exception as ex:
		SEnvir.Log("出现如下异常%s"%ex)
		return

def DelayCall(args):
	Sender = args[0]
	Sender.NPCCall(31, True)  #调用对应的NPC

MapEvent.add_listener(15,"OnEnter",OnEnter)