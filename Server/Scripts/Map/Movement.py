# -*- coding: utf-8 -*-
#载入模块SYS
from datetime import datetime, timedelta
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import MapEvent
import NpcEvent
import datetime
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from Map.进门条件列表 import *
from Map.进门成功NPC import *
from Map.进门失败NPC import *
from 主线任务奖励 import *
#此脚本为目标地图为任务地图，即默认不刷怪的地图（因为进入地图后会清除目标地图的所有怪物）
def OnMovement(args):
	Movement = args[0]
	Sender = args[1]      #玩家
	destMap = Movement.DestinationRegion.Map     #目标地图，要去的地图 拿到的类型是MapInfo
	currentMap = Movement.SourceRegion.Map  #当前地图 拿到的类型是MapInfo

	mapt = destMap.Index       #目标地图Index
	map = SEnvir.GetMap(destMap)
	
	if mapt in Limited_Map:                                                                                          #判断目标地图在限制列表内
		PlayerSetV(Sender,BV_MAP_TARGET,mapt)
		list = Limited_Map[mapt]
		i = list.get('item')
		c = list.get('ItemCount')
		playerlimit = list.get('PlayerLimit')
		if (list['value1']):
			for v1 in list['value1']:
				if v1 == '':                                                                                #不需要任务条件，可以直接进入
					SpawnMonsters(Sender,mapt)
					mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
					mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(296)
					mynpc.NPCCall(Sender)
					return True
				elif (PlayerGetV(Sender,BV_NQ_MAIN) == v1):                                                 #判断任务变量等于可进入变量
					if playerlimit > 0:                                                                     #判断不限制进入人数
						if map.PlayerCount < playerlimit:                                                   #判断目标地图玩家没有达到限制数量
							if i !='':                                                                      #列表内有条件道具限制
								if(Sender.GetItemCount(i) < c):                                             #检测包裹没有条件道具则不允许进入
									mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
									mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(265)
									mynpc.NPCCall(Sender)
									return False
								else:
									SpawnMonsters(Sender,mapt)
									mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
									mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(296)
									mynpc.NPCCall(Sender)
									return True
							else:                                                                           #检测不需要道具，允许进入
								SpawnMonsters(Sender,mapt)
								mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
								mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(296)
								mynpc.NPCCall(Sender)
								return True
						else:                                                                               #检测目标地图有玩家，禁止进入
							Sender.Connection.ReceiveChat("请稍等再进入。。。",MessageType.System)
							return False
					else:                                                                                   #检测无玩家人数限制，直接进入
						SpawnMonsters(Sender,mapt)
						mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
						mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(296)
						mynpc.NPCCall(Sender)
						return True
			else:                                                                                           #检测不符合
				mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
				mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(265)
				mynpc.NPCCall(Sender)
				return False


def SpawnMonsters(Sender,mapt):
	map = SEnvir.GetMap(mapt)
	list = Limited_Map[mapt]
	v2 = list.get('value2')
	i = list.get('item')
	c = list.get('ItemCount')
	u = list.get('TakeItem')
	x = list.get('X')
	y = list.get('Y')
	r = list.get('Range')
	if map.MonsterCount > 0:
		map.ClearAllMonsters()
	for v1 in list['value1']:
		if ( PlayerGetV(Sender,BV_NQ_MAIN) == v1 ):
			if u == 1:                                              #判断是否扣除道具，如果变量值为1，则扣除
				Sender.TakeItem(i,c)
			if v2 != '':                                        #如果列表内value2不为空，进入后更改变量
				PlayerSetV(Sender,BV_NQ_MAIN,v2)
			if (list['Monster']):                               #如果列表内有添加怪物，则自动刷怪
				for (m,n) in list['Monster'].items():
					if m != '':
						PlayerSetV(Sender,BV_NQ_KILLMON,1)
						PlayerSetV(Sender,BV_NQ_KILLNUM,0)
						map.CreateMon(x,y,r,m,n)
			return
			
MapEvent.add_listener(770,"OnMovement",OnMovement)          #半兽勇士洞63
MapEvent.add_listener(778,"OnMovement",OnMovement)          #骷髅精灵洞64
MapEvent.add_listener(776,"OnMovement",OnMovement)          #至善屋474
MapEvent.add_listener(780,"OnMovement",OnMovement)           #连接通路署箭70
MapEvent.add_listener(784,"OnMovement",OnMovement)          #进秘密洞穴477
MapEvent.add_listener(782,"OnMovement",OnMovement)          #进矿山洞穴107
MapEvent.add_listener(789,"OnMovement",OnMovement)          #进师徒关479
MapEvent.add_listener(792,"OnMovement",OnMovement)           #进半兽天然洞穴云发475
MapEvent.add_listener(774,"OnMovement",OnMovement)           #进天然洞穴云发67
MapEvent.add_listener(510,"OnMovement",OnMovement)           #诺玛村庄左入口
MapEvent.add_listener(512,"OnMovement",OnMovement)           #诺玛村庄右入口
MapEvent.add_listener(514,"OnMovement",OnMovement)           #诺玛村庄左下入口
MapEvent.add_listener(516,"OnMovement",OnMovement)           #诺玛村庄右下入口
MapEvent.add_listener(600,"OnMovement",OnMovement)           #西沙漠入口
MapEvent.add_listener(850,"OnMovement",OnMovement)           #雪原村落-龙血入口
MapEvent.add_listener(842,"OnMovement",OnMovement)           #雪原神宫1层
MapEvent.add_listener(806,"OnMovement",OnMovement)           #火影地牢入口
MapEvent.add_listener(804,"OnMovement",OnMovement)           #本国领土-雪原村落入口