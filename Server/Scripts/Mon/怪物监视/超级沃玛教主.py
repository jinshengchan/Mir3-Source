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
	
	#获取血量百分比
	hp_percent = monster.CurrentHP * 100.0 / monster.Stats[Stat.Health]
	
	#是否符合触发条件(剩余次数>0 并且 血量低于85%)
	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) > 0 and hp_percent < 60:
		# 判断怪物是否已经有buff了
		if monster.HasMonsterBuff('怪物狂暴'):
			#已经有怪物狂暴BUFF
			pass
		else:
			#给怪物加buff   攻击翻倍 魔法翻倍
			monster.AddBuff('怪物狂暴', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MinMC: 2*monster.Stats[Stat.MinMC]}, 1)
			#扣掉次数
			MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")-1)
			#给当前地图所有玩家发送信息
			#ServerUtils.SendMsgToMap(monster.CurrentMap.Info.Index, "进入怪物狂暴状态，持续10秒")
			monster.MonSay("恭喜你们，成功的激怒了我！！！")
	
	#判断怪物是否回血了，是的话，给自定义触发条件还原，可以再次触发该AI
	if MonsterGetTempVDefault(monster,"怪物狂暴", 1) == 0 and hp_percent > 62:
		MonsterSetTempV(monster,"怪物狂暴",MonsterGetTempV(monster,"怪物狂暴")+1)

####################怪物AI 触发怪物狂暴攻击速度和移动速度全部减50###################################
	#这里额外修改怪物的属性
	if monster.HasMonsterBuff('怪物狂暴'):
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			#怪物的攻击间隔缩小50
			monster.AttackDelayOffset -= 500 
			#怪物的移动间隔缩小50
			monster.MoveDelayOffset -= 400
	else:
		#还原
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.AttackDelayOffset = 0 
		monster.MoveDelayOffset = 0
#####################二次触发########################################################
	#是否符合触发条件(剩余次数>0 并且 血量低于45%)
	if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) > 0 and hp_percent < 25:
		# 判断怪物是否已经有buff了
		if monster.HasMonsterBuff('怪物狂暴1'):
			#已经有怪物狂暴BUFF
			pass
		else:
			#给怪物加buff   攻击翻倍 魔法翻倍
			monster.AddBuff('怪物狂暴1', {Stat.MaxDC: 2*monster.Stats[Stat.MaxDC], Stat.MinMC: 2*monster.Stats[Stat.MinMC]}, 5)
			#扣掉次数
			MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")-1)
			#给当前地图所有玩家发送信息
			#ServerUtils.SendMsgToMap(monster.CurrentMap.Info.Index, "进入怪物狂暴状态，持续10秒")
			monster.MonSay("颤抖吧，渺小的人类")
	
	#判断怪物是否回血了，是的话，给自定义触发条件还原，可以再次触发该AI
	if MonsterGetTempVDefault(monster,"怪物狂暴1", 1) == 0 and hp_percent > 27:
		MonsterSetTempV(monster,"怪物狂暴1",MonsterGetTempV(monster,"怪物狂暴1")+1)

####################怪物AI 触发怪物狂暴攻击速度和移动速度全部减半###################################
	#这里额外修改怪物的属性
	if monster.HasMonsterBuff('怪物狂暴1'):
		if MonsterGetTempVDefault(monster,TV_MONPET_AIBUFF,0) == 0:
			MonsterSetTempV(monster,TV_MONPET_AIBUFF,1)
			#怪物的攻击间隔缩小50
			monster.AttackDelayOffset -= 300 
			#怪物的移动间隔缩小50
			monster.MoveDelayOffset -= 300
	else:
		#还原
		MonsterSetTempV(monster,TV_MONPET_AIBUFF,0)
		monster.AttackDelayOffset = 0 
		monster.MoveDelayOffset = 0

##################怪物AI 血低飞瞬移随机地图坐标###########################################################
	#是否符合触发条件(剩余次数>0 并且 血量低于15%)
	if MonsterGetTempVDefault(monster,"怪物逃跑", 1) > 0 and hp_percent < 5:
		#判断怪物是否已经有buff了
		if monster.HasMonsterBuff('怪物逃跑'):
			#已经有怪物狂暴BUFF
			pass
		else:
			#血低飞瞬移随机坐标(怪物当前坐标范围100格)
			monster.Teleport(monster.CurrentMap, monster.CurrentMap.GetRandomLocation(monster.CurrentLocation, 100))
			#扣掉次数
			MonsterSetTempV(monster,"怪物逃跑",MonsterGetTempV(monster,"怪物逃跑")-1)
			#给当前地图所有玩家发送信息
			#ServerUtils.SendMsgToMap(monster.CurrentMap.Info.Index, "打不过了，溜吧")
			monster.MonSay("卧槽打不过了，溜吧")

MonsterEvent.add_listener(100008,"OnProcessAI",OnProcessAI)

