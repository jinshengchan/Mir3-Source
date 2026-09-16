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
		#兵器商清除
		map = SEnvir.GetMap(25)
		cell = map.Cells[72,161]          #左上定国位置
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[302,513]         #右下定国位置
		if cell.Objects != None:
			for object in reversed(cell.Objects): 
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		cell = map.Cells[169,158]         #沙城里兵器商位置
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()

		#攻城结束 沙巴克置为GM行会
		#SEnvir.ReassignCastleToGuild("GM", "沙巴克")

		return