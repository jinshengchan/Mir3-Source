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
	
	select = random.randint(0, 6)
	
	if select == 0 and hp_percent < 30 and not monster.Target is None:
		#刷出新的怪物
		monster.CurrentMap.CreateMon(monster.CurrentLocation.X,monster.CurrentLocation.Y,0,100455,1)
		SEnvir.ScheduledCall("Mon.怪物监视.女性诺玛.DelayClearMonster", SEnvir.Now.AddMilliseconds(1), monster)

def DelayClearMonster(monster):
	#删掉当前怪物
	monster.EXPOwner = None
	monster.Die()
	monster.Despawn()


MonsterEvent.add_listener(100419,"OnProcessAI",OnProcessAI)

