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
	
	select = random.randint(0, 4)
	
	hp_percent = monster.CurrentHP * 100.0 / monster.Stats[Stat.Health]
	
###################怪物狂暴######################################################
	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) == 0:
		MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")+1)
		
	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) > 0 and select == 0 and hp_percent < 99:
		if monster.HasMonsterBuff('怪物狂暴'):
			pass
		else:
			monster.AddBuff('怪物狂暴', {Stat.MaxSC: 1*monster.Stats[Stat.MaxSC],}, 6)
			MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")-1)
			
####################怪物AI 触发怪物狂暴攻击速度和移动速度全部减半###################################
	if monster.HasMonsterBuff('怪物狂暴'):
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			monster.MoveDelayOffset -= 300
	else:
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.MoveDelayOffset = 0


MonsterEvent.add_listener(10114,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(10115,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(10117,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100351,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100352,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100354,"OnProcessAI",OnProcessAI)

MonsterEvent.add_listener(100413,"OnProcessAI",OnProcessAI) #诺玛新怪物
MonsterEvent.add_listener(100414,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100416,"OnProcessAI",OnProcessAI)

