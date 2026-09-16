# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import datetime
import collections
import clr
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
import random

def TestSpawn1(begin):
    for player in SEnvir.Players:
        if player:
            player.Connection.ReceiveChat("每日副本活动将于5分钟后开启，从道馆活动管理员进入", MessageType.System)
            player.Connection.ReceiveChat("每日副本活动将于5分钟后开启，从道馆活动管理员进入", MessageType.System)
            player.Connection.ReceiveChat("每日副本活动将于5分钟后开启，从道馆活动管理员进入", MessageType.System)
            player.Connection.ReceiveChat("每日副本活动将于5分钟后开启，从道馆活动管理员进入", MessageType.System)
    return


def TestSpawn2(begin):
    for player in SEnvir.Players:
        if player:
            player.Connection.ReceiveChat("每日副本活动火爆开启，大波怪物出现在雪原荒村！", MessageType.System)
            player.Connection.ReceiveChat("每日副本活动火爆开启，大波怪物出现在雪原荒村！", MessageType.System)
            player.Connection.ReceiveChat("每日副本活动火爆开启，大波怪物出现在雪原荒村！", MessageType.System)
    return


def TestSpawn3(begin):
    for player in SEnvir.Players:
        if player:
            player.Connection.ReceiveChat("每日副本活动结束，谢谢玩家的参与和支持！", MessageType.System)
            player.Connection.ReceiveChat("每日副本活动结束，谢谢玩家的参与和支持！", MessageType.System)
            player.Connection.ReceiveChat("每日副本活动结束，谢谢玩家的参与和支持！", MessageType.System)

    return



