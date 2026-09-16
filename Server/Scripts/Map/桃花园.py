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

def OnEnter(args):            #进入地图
	Map = args[0]
	Sender = args[1]
	
	#赋值定义时间传送出去
	SEnvir.ScheduledCall("Map.桃花园.TeleportBackToTown", SEnvir.Now.AddSeconds(3600), Sender, Sender)

def OnLeave(args):            #离开地图
	Map = args[0]
	Sender = args[1]
	
	#移除定义时间传送脚本
	SEnvir.RemoveScript("Map.桃花园.TeleportBackToTown", Sender)

def TeleportBackToTown(Sender):  #传送玩家出去
	map = SEnvir.GetMap(7)  # 要传送的地图7
	Sender.TeleportByMapIndex(7, 408, 120) #传送玩家回道馆
	
#MapEvent.add_listener(475,"OnEnter",OnEnter)             #定义地图ID进入
#MapEvent.add_listener(475,"OnLeave",OnLeave)             #定义地图ID离开