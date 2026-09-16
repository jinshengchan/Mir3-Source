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

# 此变量设为这个自定义buff的序号
PLAYER_BAOXIANGBUFF_INDEX = 112

def OnDropItem(args):
	Sender=args[0]
	MapInfo=args[1]
	UserItem=args[2]
	Amount=UserItem.Count
	ItemInfo=UserItem.Info

	# 注意 不要使用UserItem.IsTemporary判断是否是新爆的物品 因为人物死亡爆东西 IsTemprary也会是True

	if MapInfo.Index == 561 and UserItem.Info.ItemName == '诺玛宝箱':
		Sender.CustomBuffRemove(PLAYER_BAOXIANGBUFF_INDEX)  #删除夺宝BUFF
		for player in SEnvir.Players:
			if(player is None):
				continue
			player.Connection.ReceiveChat("玩家【{}】丢掉诺玛宝箱。".format(Sender.Name),MessageType.RollNotice)

	#Sender.Connection.ReceiveChat("你在{}丢弃了{}个{}".format(MapInfo.Description, Amount, ItemInfo.ItemName),MessageType.System)

PlayerEvent.add_listener("OnDropItem",OnDropItem)