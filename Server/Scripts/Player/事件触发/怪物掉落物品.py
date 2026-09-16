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

# 怪物爆出物品触发
# 注意 碎片不会触发此函数
# 注意 如性能损失较大需要关闭此触发 注释掉最后一行代码(PlayerEvent.add_listener)即可
def OnMonDropItem(args):
	Sender=args[0]
	MapInfo=args[1]
	MonsterInfo=args[2]
	UserItem=args[3]
	Amount=UserItem.Count
	ItemInfo=UserItem.Info
	# 注意 不要使用UserItem.IsTemporary判断是否是新爆的物品 因为人物死亡爆东西 IsTemprary也会是True
	Sender.Connection.ReceiveChat("{}的{}爆出了{}个{}".format(MapInfo.Description,MonsterInfo.MonsterName, Amount, ItemInfo.ItemName),MessageType.System)

	# 掉落加属性
	#AllowedItemTypes = [ItemType.Weapon, ItemType.Armour, ItemType.Helmet, ItemType.Necklace, ItemType.Bracelet, ItemType.Ring, ItemType.Shoes]

	#if ItemInfo.ItemType in AllowedItemTypes:
	#	UserItem.AddStat(Stat.MinDC, 10, StatSource.Added, "掉落触发加属性")
	#	UserItem.AddStat(Stat.MaxDC, 20, StatSource.Added, "掉落触发加属性")
	#	UserItem.StatsChanged()

#PlayerEvent.add_listener("OnMonDropItem",OnMonDropItem)
