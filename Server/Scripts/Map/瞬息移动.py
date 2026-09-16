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

def OnEnter1(args):            #进入
	map = args[0]
	Sender = args[1]
	Sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.瞬息移动.CloseFuben",600,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	map.CreateMon(55,91,1,'沙漠树魔61',1)
	map.CreateMon(94,44,1,'沙漠树魔62',1)
	map.CreateMon(17,51,5,'骷髅精灵61',4)
	map.CreateMon(58,8,5,'掷斧骷髅61',2)
	map.CreateMon(36,29,5,'骷髅战士61',2)
	PlayerSetV(Sender,TV_Wizard_TeleporMon1,0)
	PlayerSetV(Sender,TV_Wizard_TeleporMon2,0)
	PlayerSetV(Sender,TV_Wizard_TeleporMon3,0)
	PlayerSetV(Sender,TV_Wizard_TeleporMon4,0)
	PlayerSetV(Sender,TV_Wizard_TeleporMon5,0)

def OnEnter2(args):            #进入
	map = args[0]
	Sender = args[1]
	Sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.瞬息移动.CloseFuben",600,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	map.CreateMon(55,91,1,'沙漠树魔61',1)
	map.CreateMon(94,44,1,'沙漠树魔62',1)
	map.CreateMon(17,51,5,'沃玛勇士61',4)
	map.CreateMon(58,8,5,'沃玛勇士61',4)
	map.CreateMon(36,29,5,'火焰沃玛61',2)

def OnEnter3(args):            #进入
	map = args[0]
	Sender = args[1]
	Sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.瞬息移动.CloseFuben",600,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	map.CreateMon(55,91,1,'沙漠树魔61',1)
	map.CreateMon(94,44,1,'沙漠树魔62',1)
	map.CreateMon(17,51,5,'掷斧骷髅61',4)
	map.CreateMon(58,8,5,'骷髅精灵61',4)
	map.CreateMon(36,29,5,'骷髅战士61',3)

def OnEnter4(args):            #进入
	map = args[0]
	Sender = args[1]
	Sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.瞬息移动.CloseFuben",600,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	map.CreateMon(55,91,1,'沙漠树魔61',1)
	map.CreateMon(94,44,1,'沙漠树魔62',1)
	map.CreateMon(17,51,5,'沃玛勇士61',4)
	map.CreateMon(58,8,5,'沃玛勇士61',4)
	map.CreateMon(36,29,5,'火焰沃玛61',3)

def OnEnter5(args):            #进入
	map = args[0]
	Sender = args[1]
	Sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.瞬息移动.CloseFuben",600,(map,))   #地图总时间 秒为单位
	map.MapTime = datetime.now()+ timedelta(minutes=5);  #副本地图关卡时间设置
	map.CreateMon(55,91,1,'沙漠树魔61',2)
	map.CreateMon(94,44,1,'沙漠树魔62',2)
	map.CreateMon(17,51,5,'骷髅精灵61',4)
	map.CreateMon(58,8,5,'掷斧骷髅61',3)
	map.CreateMon(36,29,5,'骷髅战士61',3)

def CloseFuben(args):            #关闭副本
	map=args[0]
	if Server.Envir.SEnvir.FubenMaps.Contains(map):
		Server.Envir.SEnvir.CloseMap(map)
		Server.Envir.SEnvir.FubenMaps.Remove(map)

MapEvent.add_listener(533,"OnEnter",OnEnter1)
MapEvent.add_listener(534,"OnEnter",OnEnter2)
MapEvent.add_listener(535,"OnEnter",OnEnter3)
MapEvent.add_listener(536,"OnEnter",OnEnter4)
MapEvent.add_listener(537,"OnEnter",OnEnter5)

