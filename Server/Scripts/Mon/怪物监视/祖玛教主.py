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
	
	hp_percent = monster.CurrentHP * 100.0 / monster.Stats[Stat.Health]
	
###################怪物狂暴######################################################
	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) > 0 and hp_percent < 60:
		if monster.HasMonsterBuff('怪物狂暴'):
			pass
		else:
			monster.AddBuff('怪物狂暴', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MaxMC: 2*monster.Stats[Stat.MaxMC]}, 1)
			MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")-1)
			monster.MonSay("吃了雄心豹子胆，敢来打我")

	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) == 0 and hp_percent > 62:
		MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")+1)
####################怪物AI 触发怪物狂暴攻击速度和移动速度全部减半###################################
	if monster.HasMonsterBuff('怪物狂暴'):
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			monster.AttackDelayOffset -= 800 
			monster.MoveDelayOffset -= 500
			#monster.AttackAoE(5, MagicType.SamaGuardianFire, Element.Fire)
			#monster.AttackAoE(5, MagicType.SamaGuardianFire, Element.Fire)
			#monster.AttackAoE(5, MagicType.SamaGuardianFire, Element.Fire)
	else:
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.AttackDelayOffset = 0 
		monster.MoveDelayOffset = 0
###################二次狂暴######################################################
	if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) > 0 and hp_percent < 25:
		if monster.HasMonsterBuff('怪物狂暴1'):
			pass
		else:
			monster.AddBuff('怪物狂暴1', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MaxMC: 2*monster.Stats[Stat.MaxMC]}, 1)
			MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")-1)
			monster.MonSay("我要把你们做成烤串，去死吧！")

	if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) == 0 and hp_percent > 27:
		MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")+1)
####################怪物AI 触发怪物狂暴攻击速度和移动速度全部减半###################################
	if monster.HasMonsterBuff('怪物狂暴1'):
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			monster.AttackDelayOffset -= 400 
			monster.MoveDelayOffset -= 300
			#monster.AttackAoE(5, MagicType.SamaGuardianFire, Element.Fire)
			#monster.AttackAoE(5, MagicType.SamaGuardianFire, Element.Fire)
			#monster.AttackAoE(5, MagicType.SamaGuardianFire, Element.Fire)
	else:
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.AttackDelayOffset = 0 
		monster.MoveDelayOffset = 0
####################怪物AI 玩家靠近2格就释放抗拒####################################################
	# playerlists =  monster.GetTargets(monster.CurrentMap, monster.CurrentLocation, 2)
	# for i in range(playerlists.Count):
		# Sender = playerlists[i]

	# if playerlists.Count > 0:
		# if not monster.Target is None:
			# monster.DragonRepulse(monster.GetTargets(monster.CurrentMap, monster.CurrentLocation, Envir.Config.MaxViewRange))


MonsterEvent.add_listener(30007,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100070,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100476,"OnProcessAI",OnProcessAI)
