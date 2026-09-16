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
import random

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
from Server.DBModels import *
from Server.Models import *
from MirDB import *
import Server.Envir.SEnvir as SEnvir


def SpawnMonsters(mapName, monName, amount, x=0, y=0, spawnRange=10):
    mapInfo = SEnvir.GetMapInfo(mapName)
    monInfo = SEnvir.GetMonsterInfo(monName)
    if not mapInfo or not monInfo:
        return
    targetMap = SEnvir.GetMap(mapInfo)
    if not targetMap:
        return

    spawnX = x
    spawnY = y

    if x == 0 and y == 0:
        # 寻找一个地图内的随机位置
        spawnX = random.randint(1, targetMap.Width)
        spawnY = random.randint(1, targetMap.Height)

    minX = max(0, spawnX - spawnRange)
    maxX = min(targetMap.Width, spawnX + spawnRange)
    minY = max(0, spawnY - spawnRange)
    maxY = min(targetMap.Height, spawnY + spawnRange)

    for i in range(amount):
        mob = Server.Models.MonsterObject.GetMonster(monInfo)
        mob.Spawn(mapInfo, targetMap.GetRandomLocation(minX, maxX, minY, maxY, 200))


def SendMsgToAll(msg, msg_type = MessageType.System):
    for player in SEnvir.Players:
        if player:
            player.Connection.ReceiveChat(msg, msg_type)


def SendMsgToMap(map_index, msg, msg_type = MessageType.System):
    for player in SEnvir.Players:
        if player and player.CurrentMap:
            if isinstance(map_index, list) and player.CurrentMap.Info.Index in map_index:
                player.Connection.ReceiveChat(msg, msg_type)
            elif player.CurrentMap.Info.Index == map_index:
                player.Connection.ReceiveChat(msg, msg_type)
            

def SendMsgToMapOneArg(args):
    if not args or len(args) < 2:
        return
    
    map_index = args[0]
    msg = args[1]
    msg_type = MessageType.System
    if len(args) == 3:
        msg_type = args[2]

    for player in SEnvir.Players:
        if player and player.CurrentMap:
            if isinstance(map_index, list) and player.CurrentMap.Info.Index in map_index:
                player.Connection.ReceiveChat(msg, msg_type)
            elif player.CurrentMap.Info.Index == map_index:
                player.Connection.ReceiveChat(msg, msg_type)

def GetNPCObject(indexOrName):
    NPCInfo = SEnvir.GetNpcInfo(indexOrName)
    if not NPCInfo:
        return None

    NPCMap = SEnvir.GetMap(NPCInfo.Region.Map)
    if not NPCMap:
        return None

    result = []
    if isinstance(indexOrName, int):
        result = [x for x in NPCMap.NPCs if x.NPCInfo.Index == indexOrName]
    else:
        result = [x for x in NPCMap.NPCs if x.NPCInfo.NPCName == indexOrName]

    if not result:
        return None

    return result[0]
