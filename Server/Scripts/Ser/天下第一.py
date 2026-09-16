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


def doublePKTZ(begin):
    if begin:
        ServerUtils.SendMsgToAll("十分钟后天下第一活动开始，请玩家点击天下第一雕像进入准备！", MessageType.System)
        ServerUtils.SendMsgToAll("十分钟后天下第一活动开始，请玩家点击天下第一雕像进入准备！", MessageType.System)
        ServerUtils.SendMsgToAll("十分钟后天下第一活动开始，请玩家点击天下第一雕像进入准备！", MessageType.System)
        return

    else:
        ServerUtils.SendMsgToAll("剩余一分钟天下第一活动开始，请玩家点击天下第一雕像进入准备！", MessageType.System)
        ServerUtils.SendMsgToAll("剩余一分钟天下第一活动开始，请玩家点击天下第一雕像进入准备！", MessageType.System)
        ServerUtils.SendMsgToAll("剩余一分钟天下第一活动开始，请玩家点击天下第一雕像进入准备！", MessageType.System)
        return
		
		
def doublePK(begin):
    if begin:
        ServerUtils.SendMsgToAll("天下第一活动开始，让我们拭目以待看哪位英雄能夺取荣誉！", MessageType.System)
        ServerUtils.SendMsgToAll("天下第一活动开始，让我们拭目以待看哪位英雄能夺取荣誉！", MessageType.System)
        ServerUtils.SendMsgToAll("天下第一活动开始，让我们拭目以待看哪位英雄能夺取荣誉！", MessageType.System)
        pkmap = SEnvir.GetMap(726)      #获取比赛等待地图
        to_be_teleported = []
        for player in pkmap.Players:     #遍历地图玩家
            to_be_teleported.append(player)
        for player in to_be_teleported:
            random_point = pkmap.GetRandomLocation()     #取随机数坐标值
            player.TeleportByMapIndex(727, random_point.X, random_point.Y)   #把玩家传送到比赛地图内
        return

    else:
        ServerUtils.SendMsgToAll("天下第一活动结束，谢谢所有玩家的参与！", MessageType.System)
        ServerUtils.SendMsgToAll("天下第一活动结束，谢谢所有玩家的参与！", MessageType.System)
        ServerUtils.SendMsgToAll("天下第一活动结束，谢谢所有玩家的参与！", MessageType.System)
        #指定时间内如果还没人能抢下第一，那么活动结束直接把玩家传送出地图
        pkmap = SEnvir.GetMap(727)      #获取比赛地图信息
        to_be_teleported = []
        for player in pkmap.Players:     #遍历地图玩家
            to_be_teleported.append(player)
        for player in to_be_teleported:
            player.TeleportByMapIndex(5,443,368)   #把玩家传送回道馆
        return
