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
import Utils.ServerUtils as ServerUtils

def TestSpawn1(begin):
	if begin:
		#神舰门点清理
		#map = SEnvir.GetMap(247)
		# map1 = SEnvir.GetMap(248)
		# map2 = SEnvir.GetMap(249)
		# map3 = SEnvir.GetMap(250)
		#ClearRangeMonster(map, 27, 75, 15)
		# ClearRangeMonster(map1, 161, 103, 15)
		# ClearRangeMonster(map2, 35, 76, 15)
		# ClearRangeMonster(map3, 183, 153, 15)
		#诺玛城门点清理
		map4 = SEnvir.GetMap(371)
		map5 = SEnvir.GetMap(372)
		map6 = SEnvir.GetMap(373)
		map7 = SEnvir.GetMap(565)
		map8 = SEnvir.GetMap(566)
		map9 = SEnvir.GetMap(567)
		map10 = SEnvir.GetMap(579)
		ClearRangeMonster(map4, 69, 263, 15)
		ClearRangeMonster(map5, 33, 260, 15)
		ClearRangeMonster(map6, 318, 315, 15)
		ClearRangeMonster(map7, 318, 315, 15)
		ClearRangeMonster(map8, 318, 315, 15)
		ClearRangeMonster(map9, 318, 315, 15)
		ClearRangeMonster(map10, 30, 33, 15)
		return
