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
import random

def TestSpawn1(begin):
	if begin:
		map = SEnvir.GetMap(567)
		if map.GetAliveMonsterCount(100427) < 1:
			ServerUtils.SpawnMonsters(567, 100427, 1, 49, 54, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
			ServerUtils.SpawnMonsters(567, 100426, 10, 49, 54, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
		return

def TestSpawn2(begin):
	if begin:
		map = SEnvir.GetMap(567)
		if map.GetAliveMonsterCount(100429) < 1:
			ServerUtils.SpawnMonsters(567, 100429, 1, 49, 54, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
			ServerUtils.SpawnMonsters(567, 100431, 10, 49, 54, 5)  #刷怪 地图名 怪物名 数量 X Y 范围
		return

def TestSpawn3(begin):
	if begin:
		map = SEnvir.GetMap(567)
		map.CreateNpc(63,237,372)
		return
	else:
		map = SEnvir.GetMap(567)
		cell = map.Cells[63,237]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		return

def TestSpawn4(begin):
	if begin:
		map = SEnvir.GetMap(567)
		map.CreateNpc(210,206,372)
		return
	else:
		map = SEnvir.GetMap(567)
		cell = map.Cells[210,206]
		if cell.Objects != None:
			for object in reversed(cell.Objects):
				if object != None and object.Race == ObjectType.NPC:
					object.Die()
					object.Despawn()
		return