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
	
	#赋值定义时间传送出去  调用指定传送玩家出去的函数
	SEnvir.ScheduledCall("Map.诺玛城.TeleportBackToTown", SEnvir.Now.AddSeconds(7200), Sender, Sender)

def OnLeave(args):            #离开地图
	Map = args[0]
	Sender = args[1]
	
	#移除定义时间传送脚本  移除指定传送玩家出去的函数
	SEnvir.RemoveScript("Map.诺玛城.TeleportBackToTown", Sender)

def TeleportBackToTown(Sender):  #指定传送玩家出去的函数
	Sender.TeleportByMapIndex(33, 181, 136) #传送玩家到诺玛村庄
	
MapEvent.add_listener(374,"OnEnter",OnEnter)             #定义教主房地图ID进入
MapEvent.add_listener(374,"OnLeave",OnLeave)             #定义教主房地图ID离开
