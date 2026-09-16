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
	Server.Envir.SEnvir.DelayCall("Map.大火球.CloseFuben",300,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	map.CreateMon(25,22,5,'火焰沃玛',3)
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
		if map.MonsterCount < 1 :
			PlayerSetV(Sender,GV_Wizard_AdamantineFireBall,3)
			return Sender.NPCCall(125, True)  #调用对应的NPC
		map.MapMsg("地图剩余怪物"+'%d'%map.MonsterCount,MessageType.System)
		Server.Envir.SEnvir.DelayCall("Map.大火球.MonsterCount",3,(map,Sender,))
	except Exception as ex:
		SEnvir.Log("出现如下异常%s"%ex)
		return
	
MapEvent.add_listener(521,"OnEnter",OnEnter)		
