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
	
#####################触发狂暴############################################
	#if MonsterGetTempVDefault(monster,"怪物狂暴", 1) > 0 and hp_percent < 60:
		#if monster.HasMonsterBuff('怪物狂暴'):
			#pass
		#else:
			#monster.AddBuff('怪物狂暴', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MaxMC: 2*monster.Stats[Stat.MaxMC]}, 60)
			#MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")-1)
			#monster.MonSay("哥狂暴了，就问你怕不怕")

	#if MonsterGetTempVDefault(monster,"怪物狂暴", 1) == 0 and hp_percent > 62:
		#MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")+1)
####################怪物AI 触发怪物狂暴攻击速度减半###################################
	#if monster.HasMonsterBuff('怪物狂暴'):
		#monster.AttackDelayOffset -= 500 
	#else:
		#monster.AttackDelayOffset = 0 
#####################二次狂暴############################################
	#if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) > 0 and hp_percent < 25:
		#if monster.HasMonsterBuff('怪物狂暴1'):
			#pass
		#else:
			#monster.AddBuff('怪物狂暴1', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MaxMC: 2*monster.Stats[Stat.MaxMC]}, 60)
			#MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")-1)
			#monster.MonSay("欺龙太甚，喷死你们！")

	#if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) == 0 and hp_percent > 27:
		#MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")+1)
####################怪物AI 触发怪物狂暴攻击速度减半###################################
	#if monster.HasMonsterBuff('怪物狂暴1'):
		#monster.AttackDelayOffset -= 450 
	#else:
		#monster.AttackDelayOffset = 0 



MonsterEvent.add_listener(100078,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100066,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100010,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100339,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100480,"OnProcessAI",OnProcessAI)
