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
import Utils

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir


# 开启后多少秒关闭
OPEN_TIME = 60

# 2层地图序号
GUMU2_MAPS = [1638,1639,1640,1641,1642]

# 2下3门点序号
GATES_1 = [6271,6272,6273,6274]
GATES_2 = [6275,6276,6277,6278]
GATES_3 = [6279,6280,6281,6282]
GATES_4 = [6283,6284,6285,6286]
GATES_5 = [6287,6288,6289,6290]

# 提示信息
PRE_MESSAGE = "前往古代坟墓3层的路很快就要关闭。(倒数{}秒)"
AFTER_MESSAGE = "前往古代坟墓3层的路已经关闭"
OPEN_MESSAGE = "前往古代坟墓3层的路: {} 已经开启"

def Gumu(interval):
	Utils.ServerUtils.SendMsgToMapOneArg([GUMU2_MAPS, PRE_MESSAGE.format(interval)])
	SEnvir.ScheduledCall("Map.古墓2定时开关门.ChangeGumuEntrance", SEnvir.Now.AddSeconds(interval), 'dont_care')


# 重置现在的门点
def CloseGumuGates(dont_care):
	for index1 in GATES_1:
		gate = SEnvir.GetMovementInfo(index1)
		if gate:
			gate.ExtraInfo = "关闭"
	Utils.ServerUtils.SendMsgToMapOneArg([1638, AFTER_MESSAGE]);

	for index2 in GATES_2:
		gate = SEnvir.GetMovementInfo(index2)
		if gate:
			gate.ExtraInfo = "关闭"
	Utils.ServerUtils.SendMsgToMapOneArg([1639, AFTER_MESSAGE]);

	for index3 in GATES_3:
		gate = SEnvir.GetMovementInfo(index3)
		if gate:
			gate.ExtraInfo = "关闭"
	Utils.ServerUtils.SendMsgToMapOneArg([1640, AFTER_MESSAGE]);

	for index4 in GATES_4:
		gate = SEnvir.GetMovementInfo(index4)
		if gate:
			gate.ExtraInfo = "关闭"
	Utils.ServerUtils.SendMsgToMapOneArg([1641, AFTER_MESSAGE]);

	for index5 in GATES_5:
		gate = SEnvir.GetMovementInfo(index5)
		if gate:
			gate.ExtraInfo = "关闭"
	Utils.ServerUtils.SendMsgToMapOneArg([1642, AFTER_MESSAGE]);

# 开门
def ChangeGumuEntrance(dont_care):
	# 换门点
	# 每个2层地图 随机开启1个门点
	gate1 = SEnvir.GetMovementInfo(random.choice(GATES_1))
	gate1.ExtraInfo = "开启"
	Utils.ServerUtils.SendMsgToMapOneArg([1638, OPEN_MESSAGE.format(gate1.SourceRegion.Description)])

	gate2 = SEnvir.GetMovementInfo(random.choice(GATES_2))
	gate2.ExtraInfo = "开启"
	Utils.ServerUtils.SendMsgToMapOneArg([1639, OPEN_MESSAGE.format(gate2.SourceRegion.Description)])

	gate3 = SEnvir.GetMovementInfo(random.choice(GATES_3))
	gate3.ExtraInfo = "开启"
	Utils.ServerUtils.SendMsgToMapOneArg([1640, OPEN_MESSAGE.format(gate3.SourceRegion.Description)])

	gate4 = SEnvir.GetMovementInfo(random.choice(GATES_4))
	gate4.ExtraInfo = "开启"
	Utils.ServerUtils.SendMsgToMapOneArg([1641, OPEN_MESSAGE.format(gate4.SourceRegion.Description)])

	gate5 = SEnvir.GetMovementInfo(random.choice(GATES_5))
	gate5.ExtraInfo = "开启"
	Utils.ServerUtils.SendMsgToMapOneArg([1642, OPEN_MESSAGE.format(gate5.SourceRegion.Description)])

	# 指定时间后关闭
	SEnvir.ScheduledCall("Map.古墓2定时开关门.CloseGumuGates", SEnvir.Now.AddSeconds(OPEN_TIME), 'dont_care')

	return

