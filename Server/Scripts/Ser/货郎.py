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
		#刷新货郎
		map = SEnvir.GetMap(33)
		map.CreateNpc(168,131,351)
		ServerUtils.SendMsgToAll("神秘货郎出现在诺玛村庄！", MessageType.System)
		ServerUtils.SendMsgToAll("神秘货郎出现在诺玛村庄！", MessageType.System)
		ServerUtils.SendMsgToAll("神秘货郎出现在诺玛村庄！", MessageType.RollNotice)
		return
	else:
		#货郎清除
		map = SEnvir.GetMap(33)
		cell = map.Cells[168,131]          #货郎位置
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		return 