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

def doublePKTZ(begin):
	if begin:
		ServerUtils.SendMsgToAll("十分钟后死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.System)
		ServerUtils.SendMsgToAll("十分钟后死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.System)
		ServerUtils.SendMsgToAll("十分钟后死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.RollNotice)
		return
	else:
		ServerUtils.SendMsgToAll("剩余一分钟死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.System)
		ServerUtils.SendMsgToAll("剩余一分钟死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.System)
		ServerUtils.SendMsgToAll("剩余一分钟死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.RollNotice)
		return

def doublePKTZ1(begin):
	if begin:
		ServerUtils.SendMsgToAll("五分钟后死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.RollNotice)
		return
	else:
		ServerUtils.SendMsgToAll("三分钟后死亡竞技活动开始，请玩家点击死亡竞技场进入准备！", MessageType.RollNotice)
		return


def doublePK(begin):
	if begin:
		ServerUtils.SendMsgToAll("死亡竞技活动开始，让我们拭目以待看哪位英雄能夺取荣誉！", MessageType.System)
		ServerUtils.SendMsgToAll("死亡竞技活动开始，让我们拭目以待看哪位英雄能夺取荣誉！", MessageType.System)
		ServerUtils.SendMsgToAll("死亡竞技活动开始，让我们拭目以待看哪位英雄能夺取荣誉！", MessageType.RollNotice)
		pkmap = SEnvir.GetMap(466)      #获取比赛等待地图
		to_be_teleported = []
		for player in pkmap.Players:    #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:
			random_point = pkmap.GetRandomLocation()      #取随机数坐标值
			if (player.GroupMembers):   
				player.GroupLeave()  #如果判断有组，那么直接退出队伍在进入
			player.TeleportByMapIndex(467, random_point.X, random_point.Y)   #把玩家传送到比赛地图内
			PlayerSetV(player,GV_PLAYER_ARENAACCESS,5)  #给进来的玩家增加竞技点
			GiveExperience(player,100000)    #给每个人10万经验
			if(SEnvir.Random.Next(100) < 10):
				player.GiveItem("白金盲盒",1)
		Server.Envir.SEnvir.DelayCall("Ser.死亡竞技场.CheckPlayerCount",3,())
		return
	else:
		ServerUtils.SendMsgToAll("死亡竞技活动结束，谢谢所有玩家的参与！", MessageType.System)
		ServerUtils.SendMsgToAll("死亡竞技活动结束，谢谢所有玩家的参与！", MessageType.System)
		ServerUtils.SendMsgToAll("死亡竞技活动结束，谢谢所有玩家的参与！", MessageType.RollNotice)
		#指定时间内如果还没人能抢下第一，那么活动结束直接把玩家传送出地图
		pkmap = SEnvir.GetMap(467)     #获取比赛地图信息
		to_be_teleported = []
		for player in pkmap.Players:       #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:
			player.TeleportByMapIndex(1,461,364)   #把玩家传送回比奇
			
		pkmap.ClearAllMonsters()    #清理掉刷出来的怪物
		return

def doubleEXP(begin):
	if begin:
		pkmap = SEnvir.GetMap(467)      #获取比赛地图
		to_be_teleported = []
		for player in pkmap.Players:    #遍历地图玩家
			to_be_teleported.append(player)
		for player in to_be_teleported:
			GiveExperience(player,100000)
		return
		
def CheckPlayerCount(args):
	pkmap = SEnvir.GetMap(467)      #获取比赛地图
	if pkmap.Players.Count > 5:
		Server.Envir.SEnvir.DelayCall("Ser.死亡竞技场.CheckPlayerCount",1,())
	else:
		BroadChat('竞技场当前只剩下5名玩家，究竟谁能成为天下第一，让我们拭目以待。',MessageType.RollNotice)
		killCount = {}
		for player in pkmap.Players:    #遍历地图玩家
			killCount[player] = PlayerGetTempV(player, GV_PLAYER_ARENAACCESS)
		a1 = sorted(killCount.items(),key = lambda x:x[1], reverse = True)
		for i in range(len(a1)):
			player = a1[i][0]
			if i == 0: #第一名
				player.PYMailSend("死亡竞技场", "系统", "邮件发送竞技场排名奖励", [('万年雪霜',100,True), ('强效太阳水',100,True), ('祝福油',10,True)])
				player.CustomBuffAdd(138)
			elif i == 1: #第二名
				player.PYMailSend("死亡竞技场", "系统", "邮件发送竞技场排名奖励", [('万年雪霜',80,True), ('强效太阳水',80,True), ('祝福油',8,True)])
				player.CustomBuffAdd(139)
			elif i == 2: #第三名
				player.PYMailSend("死亡竞技场", "系统", "邮件发送竞技场排名奖励", [('万年雪霜',60,True), ('强效太阳水',60,True), ('祝福油',6,True)])
				player.CustomBuffAdd(140)
			elif i == 3: #第四名
				player.PYMailSend("死亡竞技场", "系统", "邮件发送竞技场排名奖励", [('万年雪霜',40,True), ('强效太阳水',40,True), ('祝福油',4,True)])
				player.CustomBuffAdd(141)
			elif i == 4: #第五名
				player.PYMailSend("死亡竞技场", "系统", "邮件发送竞技场排名奖励", [('万年雪霜',20,True), ('强效太阳水',20,True), ('祝福油',2,True)])
				player.CustomBuffAdd(142)
	
