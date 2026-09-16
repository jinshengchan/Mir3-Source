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

from Utils import PlayerUtils

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir


def OnPutOnItem(args):
	Sender=args[0]
	UserItem=args[1]
	ItemInfo=UserItem.Info
	Position=args[2] #对应EquipmentSlot
	#将int类型的EquipmentSlot转为汉字
	PositionName=PlayerUtils.EQUIPMENT_SLOTS.keys()[PlayerUtils.EQUIPMENT_SLOTS.values().index(Position)]

	#Sender.Connection.ReceiveChat("你装备上了{}: {}".format(PositionName,ItemInfo.ItemName),MessageType.System)


def OnTakeOffItem(args):
	Sender=args[0]
	UserItem=args[1]
	ItemInfo=UserItem.Info
	Position=args[2] #对应EquipmentSlot
	#将int类型的EquipmentSlot转为汉字
	PositionName=PlayerUtils.EQUIPMENT_SLOTS.keys()[PlayerUtils.EQUIPMENT_SLOTS.values().index(Position)]

	#Sender.Connection.ReceiveChat("你把{}: {}脱下了".format(PositionName,ItemInfo.ItemName),MessageType.System)


PlayerEvent.add_listener("OnPutOnItem",OnPutOnItem)
PlayerEvent.add_listener("OnTakeOffItem",OnTakeOffItem)
