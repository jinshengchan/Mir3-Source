# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import System
s1 = clr.Reference[System.Object]()
import Server
import PlayerEvent
clr.AddReference('System')
import Server.Envir.SEnvir as SEnvir
from Utils import ServerUtils
import MapEvent
from Utils.TimeUtil import *
import datetime
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	map = SEnvir.GetMap(550)               #开启地图
	tmap = SEnvir.GetMap(551)               #要去的地图
	randomLocation = tmap.GetRandomLocation()      #取随机数坐标值
	if map.GetAliveMonsterCount("宝盒") < 1:
		Sender.TeleportByMapIndex(551,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
		return
	else:
		say = """地图的宝盒还没清理干净，无法进入下一层。
		
		[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict


NpcEvent.add_listener(346,"OnClick",OnClick)