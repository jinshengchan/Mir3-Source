# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
from datetime import *
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
		#清理一层的怪物
		sbkmap1 = SEnvir.GetMap(554)     #获取地图信息
		sbkmap1.ClearAllMonsters()    #清理掉刷出来的怪物
		
		#清理二层的怪物
		sbkmap2 = SEnvir.GetMap(555)     #获取地图信息
		sbkmap2.ClearAllMonsters()    #清理掉刷出来的怪物
		
		#清理三层的怪物
		sbkmap3 = SEnvir.GetMap(556)     #获取地图信息
		sbkmap3.ClearAllMonsters()    #清理掉刷出来的怪物
		
		#清理四层的怪物
		sbkmap4 = SEnvir.GetMap(557)     #获取地图信息
		sbkmap4.ClearAllMonsters()    #清理掉刷出来的怪物
		return
		
def TestSpawn2(begin):
	if begin:
		ServerUtils.SendMsgToAll("每周跑船活动开启，请玩家到比奇找活动管理员参与活动！", MessageType.System)
		ServerUtils.SendMsgToAll("每周跑船活动开启，请玩家到比奇找活动管理员参与活动！", MessageType.System)
		ServerUtils.SendMsgToAll("每周跑船活动开启，请玩家到比奇找活动管理员参与活动！", MessageType.RollNotice)
		return