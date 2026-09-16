# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
#引用模块的地址
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
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from 变量.默认变量 import *
from Utils.PlayerUtils import *

def OnDie(args):
	Sender=args[0]
	Killer=args[1]
	KillerName=''
	
	if Killer is not None: #如果杀人的不为空
		if hasattr(Killer, 'MonsterInfo'):
			KillerName = Killer.MonsterInfo.MonsterName
		else:
			KillerName = Killer.Name
	Sender.Connection.ReceiveChat("你被【{}】击杀了".format(KillerName),MessageType.System)
	for player in SEnvir.Players:
		if(player is None):
			continue
		player.Connection.ReceiveChat('{} 在 {} 被 {} 击杀了'.format(Sender.Name, Sender.CurrentMap.Info.Description, KillerName),MessageType.System)
	
	if check_item_equipped(Sender, '武器', '祈祷之刃'):
		select = random.randint(0,100)
		if select < 20:
			deleteEquip(Sender,'武器')
			Sender.Connection.ReceiveChat("祈祷之刃 消失了...",MessageType.Combat)
	if check_item_equipped(Sender, '左戒指', '祈祷戒指'):
		select = random.randint(0,100)
		if select < 20:
			deleteEquip(Sender,'左戒指')
			Sender.Connection.ReceiveChat("祈祷戒指 消失了...",MessageType.Combat)
	if check_item_equipped(Sender, '右戒指', '祈祷戒指'):
		select = random.randint(0,100)
		if select < 20:
			deleteEquip(Sender,'右戒指')
			Sender.Connection.ReceiveChat("祈祷戒指 消失了...",MessageType.Combat)
	if check_item_equipped(Sender, '左手镯', '祈祷手镯'):
		select = random.randint(0,100)
		if select < 20:
			deleteEquip(Sender,'左手镯')
			Sender.Connection.ReceiveChat("祈祷手镯 消失了...",MessageType.Combat)
	if check_item_equipped(Sender, '右手镯', '祈祷手镯'):
		select = random.randint(0,100)
		if select < 20:
			deleteEquip(Sender,'右手镯')
			Sender.Connection.ReceiveChat("祈祷手镯 消失了...",MessageType.Combat)
	if check_item_equipped(Sender, '项链', '祈祷项链'):
		select = random.randint(0,100)
		if select < 20:
			deleteEquip(Sender,'项链')
			Sender.Connection.ReceiveChat("祈祷项链 消失了...",MessageType.Combat)
	if check_item_equipped(Sender, '头盔', '祈祷头盔'):
		select = random.randint(0,100)
		if select < 20:
			deleteEquip(Sender,'头盔')
			Sender.Connection.ReceiveChat("祈祷头盔 消失了...",MessageType.Combat)

PlayerEvent.add_listener("OnDie",OnDie)
