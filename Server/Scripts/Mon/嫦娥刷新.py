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
import random

def RefreshMonster(dont_care):
	map1 = Server.Envir.SEnvir.GetMap(1) #比奇
	map2 = Server.Envir.SEnvir.GetMap(5) #边境
	map3 = Server.Envir.SEnvir.GetMap(6) #银杏
	map4 = Server.Envir.SEnvir.GetMap(7) #道馆
	map5 = Server.Envir.SEnvir.GetMap(24) #毒蛇
	map6 = Server.Envir.SEnvir.GetMap(27) #绿洲
	map7 = Server.Envir.SEnvir.GetMap(50) #盟重
	map8 = Server.Envir.SEnvir.GetMap(55) #潘夜
	map9 = Server.Envir.SEnvir.GetMap(57) #失乐园
	
	if map1.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(1, "嫦娥", 2, 438, 376, 1000)

	if map2.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(5, "嫦娥", 2, 321, 260, 1000)

	if map3.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(6, "嫦娥", 2, 302, 266, 1000)

	if map4.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(7, "嫦娥", 2, 310, 260, 1000)

	if map5.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(24, "嫦娥", 2, 211, 178, 1000)

	if map6.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(27, "嫦娥", 2, 250, 392, 1000)

	if map7.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(50, "嫦娥", 2, 282, 270, 1000)

	if map8.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(55, "嫦娥", 2, 417, 363, 1000)

	if map9.GetAliveMonsterCount("嫦娥") < 1:
		ServerUtils.SpawnMonsters(57, "嫦娥", 2, 358, 365, 1000)

	return

