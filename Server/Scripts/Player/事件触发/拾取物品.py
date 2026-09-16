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
import Server.Envir.SEnvir as SEnvir

def OnPickUpItem(args):
	Sender=args[0]
	MapInfo=args[1]
	UserItem=args[2]
	Amount=UserItem.Count
	ItemInfo=UserItem.Info
	# 注意 不要使用UserItem.IsTemporary判断是否是新爆的物品 因为人物死亡爆东西 IsTemprary也会是True

	if MapInfo.Index == 251:
		if UserItem.Info.ItemName == '霸王教主雕像':
			if(PlayerGetV(Sender,BV_NQ_SJKILL)==5013):
				PlayerSetV(Sender,BV_NQ_SJKILL,5014)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """（得到了雕像。。。去找霸王幽灵吧。。）"""

	#Sender.Connection.ReceiveChat("你在{}拾取了{}个{}".format(MapInfo.Description, Amount, ItemInfo.ItemName),MessageType.System)

PlayerEvent.add_listener("OnPickUpItem",OnPickUpItem)
