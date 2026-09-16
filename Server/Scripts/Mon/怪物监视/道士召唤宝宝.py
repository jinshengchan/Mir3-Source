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

def OnProcessAI(args):
	monster = args[0]
	
	if monster.HasBuff(BuffType.MonsterBuff): 
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			monster.AttackDelayOffset -= 900
			monster.MoveDelayOffset -= 200
	else:
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.AttackDelayOffset = 0
		monster.MoveDelayOffset = 0


MonsterEvent.add_listener(40017,"OnProcessAI",OnProcessAI)  #变异骷髅
MonsterEvent.add_listener(40018,"OnProcessAI",OnProcessAI)  #神兽
MonsterEvent.add_listener(40020,"OnProcessAI",OnProcessAI)  #超强骷髅

