# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import collections
from Defines import *
import PlayerEvent
import Server
import clr
import Server.Models.MonsterObject as Monster
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
from Utils.PlayerUtils import *
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
import random
from 变量.默认变量 import *
from 变量.任务杀怪 import *
from 主线任务奖励 import *
from string import digits

# 击杀怪物的index
# KILL_MON = [] 为任意怪物
KILL_MON = [10114,10115,10116,10117,10118]  #诺玛的怪物
KILL_MONDZ = [20022]  #诺玛的怪物



		
def OnKillMon(args):
	Sender = args[0]
	MonsterInfo = args[1]
	kill_map = SEnvir.GetMap(Sender.Character.CurrentMap)
	
	if MonsterInfo.Index in KILL_MON:  #判断击杀诺玛怪物的信息 
		 PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) + 1)   #新书兑换任务变量增加
		 PlayerSetV(Sender,GV_KILLMON_NMGWJSCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWJSCOUNT) + 1)  #杀死诺玛怪物变量增加
	 #Sender.Connection.ReceiveChat("你成功击杀了怪物{}".format(MonsterInfo.MonsterName), MessageType.System)

	if MonsterInfo.Index in KILL_MONDZ:  #判断击杀诺玛队长的信息
		 PlayerSetV(Sender,GV_KILLMON_NMDZJSCOUNT,PlayerGetV(Sender,GV_KILLMON_NMDZJSCOUNT) + 1)   #杀死诺玛队长变量增加

	if(PlayerGetV(Sender,GV_KILLMON_NMGWJSCOUNT)== 200):  #如果杀死诺玛怪物的数量达到200只
		 PlayerSetV(Sender,GV_KILLMON_NMGWJSCOUNT,0)   #先把杀死诺玛怪物的计数清零
		 #在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 2格范围内 刷怪的名字  刷怪的数量)
		 Sender.CurrentMap.CreateMon(Sender.CurrentLocation.X,Sender.CurrentLocation.Y,2,'诺玛突击队长',1)
		 #系统发出公告提示
		 Sender.Connection.ReceiveChat("由于玩家 {} 杀死了诺玛怪物200个，触发了队长的复仇，诺玛突击队长出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)

	if(PlayerGetV(Sender,GV_KILLMON_NMDZJSCOUNT)== 100):  #如果杀死诺玛队长的数量达到100只
		 PlayerSetV(Sender,GV_KILLMON_NMDZJSCOUNT,0)   #先把杀死诺玛队长的计数清零
		 #在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 5格范围内 刷怪的名字  刷怪的数量)
		 Sender.CurrentMap.CreateMon(Sender.CurrentLocation.X,Sender.CurrentLocation.Y,5,'诺玛教主',1)
		 #系统发出公告提示
		 Sender.Connection.ReceiveChat("由于玩家 {} 杀死了诺玛突击队长100个，触发了教主的复仇，诺玛教主出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)

	#古墓3小BOSS 古墓土偶护卫武士
	#if MonsterInfo.Index == 389:
		#击杀古墓3小BOSS.OnKillGumuBoss1()
	


	if(Sender.GroupMembers):                                        #检测是否组队
		for player in Sender.GroupMembers:                          #遍历队员
			pc_map = SEnvir.GetMap(player.Character.CurrentMap)     #定位队员的地图信息
			if pc_map == kill_map:                                  #检测同组队员处于同一地图
				X = Sender.Character.CurrentLocation.X
				Y = Sender.Character.CurrentLocation.Y
				X1 = player.Character.CurrentLocation.X
				Y1 = player.Character.CurrentLocation.Y
				if X - 16 < X1 < X + 16 and Y - 16 < Y1 < Y + 16:
					if PlayerGetV(player,BV_QT_KILLMON) == 1:
						TaskNumber = PlayerGetV(player,BV_QT_TODAY)
						if TaskNumber > 0:
							DailyTaskList = GetDailyTaskList(player,TaskNumber)
							if DailyTaskList:
								DailyKillMon(player,MonsterInfo,DailyTaskList)
					if PlayerGetV(player,BV_NQ_KILLMON) == 1:
						if PlayerGetV(player,BV_NQ_MAIN) in MainTaskMonsters:
							MainQuestList = MainTaskMonsters[PlayerGetV(player,BV_NQ_MAIN)]
							if MainQuestList:
								zdq = MainQuestList.get('组队')
								if zdq == 1:
									NQKillMon(player,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_MAIN))
					if PlayerGetV(player,BV_NQ_SKILLMON) == 1:
						if PlayerGetV(player,BV_NQ_SKILL) in SkillTaskMonsters:
							MainQuestList = SkillTaskMonsters[PlayerGetV(player,BV_NQ_SKILL)]
							if MainQuestList:
								zdq = MainQuestList.get('组队')
								if zdq == 1:
									NQSKillMon(player,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SKILL))
					if PlayerGetV(player,BV_NQ_SJKILLMON) == 1:
						if PlayerGetV(player,BV_NQ_SJKILL) in ShipTaskMonsters:
							MainQuestList = ShipTaskMonsters[PlayerGetV(player,BV_NQ_SJKILL)]
							if MainQuestList:
								zdq = MainQuestList.get('组队')
								if zdq == 1:
									NQShipKillMon(player,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SJKILL))
					
	else:
		if PlayerGetV(Sender,BV_QT_KILLMON) == 1:
			TaskNumber = PlayerGetV(Sender,BV_QT_TODAY)
			if TaskNumber > 0 :
				DailyTaskList = GetDailyTaskList(Sender,TaskNumber)
				if DailyTaskList:
					DailyKillMon(Sender,MonsterInfo,DailyTaskList)
		if PlayerGetV(Sender,BV_NQ_KILLMON) == 1:
			if PlayerGetV(Sender,BV_NQ_MAIN) in MainTaskMonsters:
				MainQuestList = MainTaskMonsters[PlayerGetV(Sender,BV_NQ_MAIN)]
				if MainQuestList:
					NQKillMon(Sender,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_MAIN))
		if PlayerGetV(Sender,BV_NQ_SKILLMON) == 1:
			if PlayerGetV(Sender,BV_NQ_SKILL) in SkillTaskMonsters:
				MainQuestList = SkillTaskMonsters[PlayerGetV(Sender,BV_NQ_SKILL)]
				if MainQuestList:
					NQSKillMon(Sender,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SKILL))
		if PlayerGetV(Sender,BV_NQ_SJKILLMON) == 1:
			if PlayerGetV(Sender,BV_NQ_SJKILL) in ShipTaskMonsters:
				MainQuestList = ShipTaskMonsters[PlayerGetV(Sender,BV_NQ_SJKILL)]
				if MainQuestList:
					NQShipKillMon(Sender,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SJKILL))


####万事通任务杀怪
def DailyKillMon(Sender,MonsterInfo,DailyTaskList):
	kn = PlayerGetV(Sender,BV_QT_KILLNUM)               #kn = 万事通任务杀怪数量
	mk = MonsterInfo.MonsterName                        #获取怪物名称
	mks = MonsterInfo.MonsterName
	mks = mks.translate(None,digits)  #怪物名去除数字后缀
	nt = DailyTaskList.get('杀怪数量')
	if DailyTaskList.get('任务怪物'):
		if mk in DailyTaskList.get('任务怪物'):
			kn += 1
			PlayerSetV(Sender,BV_QT_KILLNUM,kn)
			
			if kn < nt:
				
				Sender.Connection.ReceiveChat("万事通任务：您打败了 1 只 {} ，累计 {} 只怪物！".format(mks,kn), MessageType.Combat)
				return
			else:
				PlayerSetV(Sender,BV_QT_KILLMON,0)
				Sender.Connection.ReceiveChat("万事通任务：您已经打败足够的 {} ，可以回去交差了。".format(mks), MessageType.Combat)

####江湖任务杀怪
def NQKillMon(Sender,MonsterInfo,MainQuestList,index):
	knq = PlayerGetV(Sender,BV_NQ_KILLNUM)              #knq = 江湖任务杀怪数量
	mk = MonsterInfo.MonsterName                        #获取怪物名称
	igq = PlayerGetV(Sender,BV_NQ_ITEMGOT)              #ig = 江湖任务杀怪获得道具变量
	tiq = MainQuestList.get('任务道具')
	ig = MainQuestList.get('道具数量')
	ntq = MainQuestList.get('目标参数')
	if mk in MainQuestList.get('任务怪物'):
		if ig == '':
			knq += 1
			PlayerSetV(Sender,BV_NQ_KILLNUM,knq)
			if knq < ntq:
				return
			else:
				PlayerSetV(Sender,BV_NQ_KILLMON,0)
				mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
				mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
				mynpc.NPCCall(Sender)
				Sender.Connection.ReceiveChat("江湖任务：完成杀怪！", MessageType.Combat)
		elif igq < ig:
			select = random.randint(0,1000)
			if select < ntq:
				igq += 1
				Sender.GiveItem(tiq,1)
				PlayerSetV(Sender,BV_NQ_ITEMGOT,igq)
				if igq == ig:
					PlayerSetV(Sender,BV_NQ_KILLMON,0)
					PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
					mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
					mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
					mynpc.NPCCall(Sender)
					Sender.Connection.ReceiveChat("江湖任务：完成！", MessageType.Combat)
			else:
				Sender.Connection.ReceiveChat("任务：没有找到 {} ，继续寻找吧...".format(tiq), MessageType.Combat)


####神舰任务杀怪
def NQShipKillMon(Sender,MonsterInfo,MainQuestList,index):
	knq = PlayerGetV(Sender,BV_NQ_SJKILLNUM)              #knq = 神舰任务杀怪数量
	mk = MonsterInfo.MonsterName                        #获取怪物名称
	igq = PlayerGetV(Sender,BV_NQ_SJKILLITEMGOT)              #ig = 神舰任务杀怪获得道具变量
	tiq = MainQuestList.get('任务道具')
	ig = MainQuestList.get('道具数量')
	ntq = MainQuestList.get('目标参数')
	if mk in MainQuestList.get('任务怪物'):
		if ig == '':
			knq += 1
			PlayerSetV(Sender,BV_NQ_SJKILLNUM,knq)
			if knq < ntq:
				return
			else:
				PlayerSetV(Sender,BV_NQ_SJKILLMON,0)
				mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
				mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
				mynpc.NPCCall(Sender)
				Sender.Connection.ReceiveChat("神舰任务：完成杀怪！", MessageType.Combat)
		elif igq < ig:
			select = random.randint(0,1000)
			if select < ntq:
				igq += 1
				Sender.GiveItem(tiq,1)
				PlayerSetV(Sender,BV_NQ_SJKILLITEMGOT,igq)
				if igq == ig:
					PlayerSetV(Sender,BV_NQ_SJKILLMON,0)
					PlayerSetV(Sender,BV_NQ_SJKILLITEMGOT,0)
					mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
					mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
					mynpc.NPCCall(Sender)
					Sender.Connection.ReceiveChat("神舰任务：完成！", MessageType.Combat)
			else:
				Sender.Connection.ReceiveChat("任务：没有找到 {} ，继续寻找吧...".format(tiq), MessageType.Combat)

PlayerEvent.add_listener("OnKillMon",OnKillMon)

