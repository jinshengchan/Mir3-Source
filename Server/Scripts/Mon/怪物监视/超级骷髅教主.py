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
	
	playerlists =  monster.GetTargets(monster.CurrentMap, monster.CurrentLocation, 8)
	for i in range(playerlists.Count):
		sender = playerlists[i]
	
	select = random.randint(0, 3)
	
	if select == 0:
		if not monster.Target is None:
			monster.LineAoE(10, 0, 16, MagicType.FireBall, Element.Lightning)
########################触发狂暴####################################################################
	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) > 0 and hp_percent < 60:
		if monster.HasMonsterBuff('怪物狂暴'):
			pass
		else:
			monster.AddBuff('怪物狂暴', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MaxMC: 2*monster.Stats[Stat.MaxMC]}, 5)
			MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")-1)
			monster.MonSay("辛苦你们跑这么远来送死了")
	
	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) == 0 and hp_percent > 62:
		MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")+1)

####################怪物AI 触发怪物狂暴攻击速度和移动速度全部减半###################################
	if monster.HasMonsterBuff('怪物狂暴'):
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			monster.AttackDelayOffset -= 500 
			monster.MoveDelayOffset -= 300
	else:
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.AttackDelayOffset = 0 
		monster.MoveDelayOffset = 0
		
########################二次触发狂暴####################################################################
	if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) > 0 and hp_percent < 25:
		if monster.HasMonsterBuff('怪物狂暴1'):
			pass
		else:
			monster.AddBuff('怪物狂暴1', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MaxMC: 2*monster.Stats[Stat.MaxMC]}, 5)
			MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")-1)
			monster.MonSay("颤抖吧，自不量力的人类！")
			
	if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) == 0 and hp_percent > 27:
		MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")+1)
####################怪物AI 触发怪物狂暴攻击速度和移动速度全部减半###################################
	if monster.HasMonsterBuff('怪物狂暴1'):
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			monster.AttackDelayOffset -= 900 
			monster.MoveDelayOffset -= 400
	else:
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.AttackDelayOffset = 0 
		monster.MoveDelayOffset = 0

MonsterEvent.add_listener(100009,"OnProcessAI",OnProcessAI)

