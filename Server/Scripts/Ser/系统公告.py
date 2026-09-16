# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
import random
import Server.Envir.SEnvir as SEnvir

def SendMsg(counter):
	# 公告信息延迟秒
	dalay = 150
	# 公告信息的内容
	lines = [
"系统公告：欢迎您，本服为仿光通1.45时期的版本，由于是仿制，不能保证怪物、物品、任务及各功能做到完全一致，在游戏中也难免出现各种BUG，如果有BUG请第一时间通知我们修复",
"系统公告：现在开放的是1.45版本，后续会开放新地图，新装备，新技能，新副本，更多玩法，请关注游戏群",
"系统公告：服务器重要公告请入群查阅：群号:123456789；不入群视为放弃，本游戏完全免费，没有任何收费项目，凡是打着游戏名义要钱的都是骗子！！！",
"系统公告：重要提醒：泡点前请关闭允许回生及关闭允许天地合一",
"系统公告：重要提醒：新手玩家请跟着游戏攻略及任务提示进行，可以熟悉游戏设置",
"系统公告：在游戏里，如果使用变态外挂，会被封号的。请大家切记！不要向任何人泄露您的游戏ID，否则很有可能被盗号。游戏虽然好玩，但是也要注意休息哦！",
"系统公告：GM绝不会参与游戏！请各位玩家妥善保管好个人ID以及注册信息，合理安排游戏时间,享受健康生活",
"本服是养老服，节奏较慢，一切装备都可以在游戏中获得，没有GM，不刷装备，全靠脸",
]

	###################下面的不用改################
	text = ""
	line_index = int(counter)

	if line_index is None:
		line_index = 0

	if line_index < 0:
		# 随机选一个
		text = random.choice(lines)
		line_index -= 1
	else:
		# 发送指定信息
		text = lines[line_index % len(lines)]
		
	BroadChat(text,MessageType.Notice)
	###################上面的不用改################

	# 自动定时发送公告
	SEnvir.DelayCall("Ser.系统公告.SendMsg", dalay, line_index + 1)


