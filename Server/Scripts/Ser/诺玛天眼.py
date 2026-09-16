# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
from datetime import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils


def TestSpawn1(begin):
	if begin:
		#刷新诺玛天眼
		map = SEnvir.GetMap(33)
		map.CreateNpc(83,343,355)  #地图刷新的NPC （NPC坐标X,Y，NPC名字或者ID）
		ServerUtils.SendMsgToAll("囚禁在诺玛天牢的诺玛村庄原住居民向勇士们发出了求救信号，并打开了诺玛天眼。（坐标：83,343）", MessageType.System)
		ServerUtils.SendMsgToAll("囚禁在诺玛天牢的诺玛村庄原住居民向勇士们发出了求救信号，并打开了诺玛天眼。（坐标：83,343）", MessageType.System)
		ServerUtils.SendMsgToAll("囚禁在诺玛天牢的诺玛村庄原住居民向勇士们发出了求救信号，并打开了诺玛天眼。（坐标：83,343）", MessageType.RollNotice)
		return
	else:
		#诺玛天眼清除
		map = SEnvir.GetMap(33)
		cell = map.Cells[83,343]          #（NPC坐标X,Y）
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		return