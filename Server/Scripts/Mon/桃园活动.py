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

# BOSS列表
MONBOSSLIST = [
"沃玛教主",
"霸王教主",
"触龙神",
"骷髅教主",
"赤月恶魔",
"潘夜牛魔王",
"祖玛教主",
"震天魔神",
"诺玛教主",
"地天灭王",
]

def RefreshMonster(dont_care):
	map = Server.Envir.SEnvir.GetMap(475)
	selected = random.choice(MONBOSSLIST)
	if (map.MonsterCount == 0):#没有怪物就刷怪
		ServerUtils.SpawnMonsters("桃花源", selected, 1, 48, 40, 5)
	return

