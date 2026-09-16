# -*- coding: utf-8 -*-
#载入模块SYS
import sys
import datetime
#引用模块的地址
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
from Globals import *
from Utils import ServerUtils
from Defines import *
import Server
import MonsterEvent
import Server.Envir.SEnvir as SEnvir
import Server.Envir as Envir
import random

def OnProcessAI(args):
	monster = args[0]
	
	hp_percent = monster.CurrentHP * 100.0 / monster.Stats[Stat.Health]
	hp_current = monster.CurrentHP
	select = random.randint(0, 1)
	
##################怪物AI 血低飞瞬移随机地图坐标###########################################################
	if MonsterGetTempVDefault(monster,"怪物逃跑", 1) > 0 and hp_percent < 10:
		if monster.HasMonsterBuff('怪物逃跑'):
			pass
		else:
			if select == 0 and hp_current > 50:
				monster.Teleport(monster.CurrentMap, monster.CurrentMap.GetRandomLocation(monster.CurrentLocation, 100))
				monster.MonSay("打不过了，溜吧")


MonsterEvent.add_listener(100366,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100395,"OnProcessAI",OnProcessAI)

