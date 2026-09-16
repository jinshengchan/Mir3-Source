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
	map1 = Server.Envir.SEnvir.GetMap(61) #刷僵尸王地图
	map2 = Server.Envir.SEnvir.GetMap(84) #刷沃玛教主地图
	map3 = Server.Envir.SEnvir.GetMap(157) #刷触龙神地图
	map4 = Server.Envir.SEnvir.GetMap(176) #刷黑猪王地图
	map5 = Server.Envir.SEnvir.GetMap(303) #刷骷髅教主地图
	map6 = Server.Envir.SEnvir.GetMap(277) #刷赤月恶魔地图
	map7 = Server.Envir.SEnvir.GetMap(298) #刷潘夜牛魔王地图
	map8 = Server.Envir.SEnvir.GetMap(142) #刷祖玛教主地图
	map9 = Server.Envir.SEnvir.GetMap(355) #刷震天魔神地图
	
	if map1.GetAliveMonsterCount("僵尸王") < 1 and map1.GetAliveMonsterCount("超级僵尸王") < 1:
		ServerUtils.SpawnMonsters(61, "僵尸王", 1, 18, 16, 1)

	if map2.GetAliveMonsterCount("沃玛教主") < 1 and map2.GetAliveMonsterCount("超级沃玛教主") < 1:
		ServerUtils.SpawnMonsters(84, "沃玛教主", 1, 50, 49, 1)

	if map3.GetAliveMonsterCount("触龙神") < 1 and map3.GetAliveMonsterCount("超级触龙神") < 1:
		ServerUtils.SpawnMonsters(157, "触龙神", 1, 84, 169, 1)

	if map4.GetAliveMonsterCount("黑猪王") < 1 and map4.GetAliveMonsterCount("超级黑猪王") < 1:
		ServerUtils.SpawnMonsters(176, "黑猪王", 1, 73, 33, 1)

	if map5.GetAliveMonsterCount("骷髅教主") < 1 and map5.GetAliveMonsterCount("超级骷髅教主") < 1:
		ServerUtils.SpawnMonsters(303, "骷髅教主", 1, 196, 179, 1)

	if map6.GetAliveMonsterCount("赤月恶魔") < 1 and map6.GetAliveMonsterCount("超级赤月恶魔") < 1:
		ServerUtils.SpawnMonsters(277, "赤月恶魔", 1, 23, 18, 1)

	if map7.GetAliveMonsterCount("潘夜牛魔王") < 1 and map7.GetAliveMonsterCount("超级潘夜牛魔王") < 1:
		ServerUtils.SpawnMonsters(298, "潘夜牛魔王", 1, 51, 51, 1)

	if map8.GetAliveMonsterCount("祖玛教主") < 1 and map8.GetAliveMonsterCount("超级祖玛教主") < 1:
		ServerUtils.SpawnMonsters(142, "祖玛教主", 1, 21, 19, 1)

	if map9.GetAliveMonsterCount("震天魔神") < 1 and map9.GetAliveMonsterCount("超级震天魔神") < 1:
		ServerUtils.SpawnMonsters(355, "震天魔神", 1, 23, 39, 1)

	return

