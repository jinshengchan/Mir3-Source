# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import clr

clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import Server.Envir.SEnvir as SEnvir
clr.AddReference("System.Core")
clr.AddReference('System')
import System
clr.ImportExtensions(System.Linq)

# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *

import unicodedata


# BOSS数量过多 建议分页
# 这里是按等级分的 0-45， 75-100这样
LEVEL_RANGE_1 = 70
LEVEL_RANGE_2 = 80
LEVEL_RANGE_3 = 90
LEVEL_RANGE_4 = 100
LEVEL_RANGE_5 = 120
LEVEL_RANGE_6 = 150
LEVEL_RANGE_7 = 200
LEVEL_RANGE_8 = 300

# 过滤名字结尾是数字的怪
allInfo = [x for x in SEnvir.BossTrackerList if not (x.BossName)[-1].isdigit()]
# 按等级升序
sortByLevel = sorted(allInfo, cmp=None, key=lambda x: x.BossInfo.Level, reverse=False)

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if Menu == 1:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(0, LEVEL_RANGE_1)
	elif Menu == 2:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(LEVEL_RANGE_1, LEVEL_RANGE_2)
	elif Menu == 3:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(LEVEL_RANGE_2, LEVEL_RANGE_3)
	elif Menu == 4:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(LEVEL_RANGE_3, LEVEL_RANGE_4)
	elif Menu == 5:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(LEVEL_RANGE_4, LEVEL_RANGE_5)
	elif Menu == 6:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(LEVEL_RANGE_5, LEVEL_RANGE_6)
	elif Menu == 7:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(LEVEL_RANGE_6, LEVEL_RANGE_7)
	elif Menu == 8:
#判断元宝
		if (Sender.Gold < 200000):
			say= """你没有足够的金币。

			[离开:0]"""
		else:
#上面条件达成，扣除金币开始查询
			SubGold(Sender,200000)
			say = GenereateSay(LEVEL_RANGE_7, LEVEL_RANGE_8)


	elif Menu >= 100:
		# 详情查询
		info = next(x for x in sortByLevel if x.BossInfo.Index == Menu-100)
		say = GenerateDetail(info.SpawnInfo) if info else "出错了"


	else:
		say = """这里可以查询所有BOSS的状态

		每次查询收费20W金币

		[查询0-{}级boss:1]

		[查询{}-{}级boss:2]

		[查询{}-{}级boss:3]

		[查询{}级以上boss:4]

		[查询{}级以上boss:5]

		[查询{}级以上boss:6]

		[查询{}级以上boss:7]

		[查询{}级以上boss:8]
		
		[关闭:0]""".format(LEVEL_RANGE_1, LEVEL_RANGE_1+1, LEVEL_RANGE_2, LEVEL_RANGE_2+1, LEVEL_RANGE_3, LEVEL_RANGE_3+1, LEVEL_RANGE_4+1, LEVEL_RANGE_5+1, LEVEL_RANGE_6, LEVEL_RANGE_7, LEVEL_RANGE_8)
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict


# 生成列表
def GenereateSay(minLevel, maxLevel):
	# 表头
	say = '{0: <15} {1: <15} {2: <15} \n'.format('BOSS', '击杀者', '击杀时间') 
	# 内容
	filtered = [x for x in sortByLevel if x.BossInfo.Level >= minLevel and x.BossInfo.Level <= maxLevel and not (x.BossName)[-1].isdigit()]
	say += '\n'.join("[{}:{}]     {}    {}".format(
			boss.BossName, 
			boss.BossInfo.Index + 100,
			boss.LastKiller.CharacterName if boss.LastKiller else '无',
			boss.LastKillTime if boss.LastKiller else '无') for boss in filtered)
	return say


def GenerateDetail(spawns):
	# 表头
	say = '{0: <10} {1: <6} {2: <6} {3: <6}\n'.format('名称', '当前地图', '存活数量', '下次刷新') 
	# 内容
	say += '\n'.join("{}    {}   {}   {}".format(
			spawn.Info.Monster.MonsterName, 
			spawn.CurrentMap.Info.Description,
			spawn.AliveCount,
			spawn.NextSpawn) for spawn in spawns)
	return say


NpcEvent.add_listener(336,"OnClick",OnClick)