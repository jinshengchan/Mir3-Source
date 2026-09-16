# -*- coding: utf-8 -*-
#载入模块SYS
from datetime import datetime, timedelta
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
from Utils.TimeUtil import *
#Server.Envir.SEnvir.Log(__name__+"导入")
def OnEnter(args):            #进入
	map = args[0]
	sender = args[1]
	sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.feitian.CloseFuben",7200,(map,))   #地图总时间 秒为单位
	MonsterCount((map,sender,))
	
def CloseFuben(args):            #关闭副本
	map=args[0]
	Server.Envir.SEnvir.CloseMap(map.Info)
	
def MonsterCount(args):         #怪物总数
	map = args[0]
	sender = args[1]
	inmap = Server.Envir.SEnvir.GetMap(map.Info)  # 判断地图是否存在
	if(inmap is None):
		#Server.Envir.SEnvir.Log("地图退出")
		return		
	#sender.Connection.ReceiveChat('%d'%map.MonsterCount,MessageType.System)
	map.MapMsg("地图剩余怪物"+'%d'%map.MonsterCount,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.feitian.MonsterCount",30,(map,sender,))
	
#MapEvent.add_listener(613,"OnEnter",OnEnter)
#MapEvent.add_listener(1530,"OnEnter",OnEnter)		
	