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

def TestSpawn1(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("迎新年贺新春，比奇城击杀任意怪物得红包活动将于十分钟后开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新年贺新春，比奇城击杀任意怪物得红包活动将于十分钟后开启！", MessageType.System)
				player.Connection.ReceiveChat("迎新年贺新春，比奇城击杀任意怪物得红包活动将于十分钟后开启！", MessageType.System)
		return

def TestSpawn2(begin):
	if begin:
		for player in SEnvir.Players:
			if player:
				player.Connection.ReceiveChat("迎新年贺新春，比奇城击杀任意怪物得红包活动火爆开启，大波宝盒出现在比奇！", MessageType.System)
				player.Connection.ReceiveChat("迎新年贺新春，比奇城击杀任意怪物得红包活动火爆开启，大波宝盒出现在比奇！", MessageType.System)
				player.Connection.ReceiveChat("迎新年贺新春，比奇城击杀任意怪物得红包活动火爆开启，大波宝盒出现在比奇！", MessageType.System)
		ServerUtils.SpawnMonsters("比奇城", "宝盒", 888, 464, 372, 10000)
		return





