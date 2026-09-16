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

# 奖励信息, 格式如下
# 注意! 数量只对可以堆叠的道具有效 例如金币 元宝 药水
# 注意! 最多7种不同的物品

Rewards = {
#			1: [('双倍经验卷（绑定）', 1, True,)],
#			2: [('双倍经验卷（绑定）', 1, True,)],
#			3: [('双倍经验卷（绑定）', 1, True,)],
#			4: [('双倍经验卷（绑定）', 1, True,)],
#			5: [('双倍经验卷（绑定）', 1, True,)],
}
Rewards48 = {
#			1: [('双倍经验卷（绑定）', 1, True,)],
#			2: [('双倍经验卷（绑定）', 1, True,)],
#			3: [('双倍经验卷（绑定）', 1, True,)],
#			4: [('双倍经验卷（绑定）', 1, True,)],
#			5: [('双倍经验卷（绑定）', 1, True,)],
}

def OnTaskComplete(Sender,num_dt):
	if Sender.Level < 48:
		if num_dt in Rewards:
			TaskRewards = Rewards.get(num_dt)
			Sender.PYMailSend("万事通任务额外奖励", "万事通","恭喜您完成第 {} 次万事通任务~ 请确认你的礼物。".format(num_dt),TaskRewards)
	else:
		if num_dt in Rewards48:
			TaskRewards = Rewards48.get(num_dt)
			Sender.PYMailSend("万事通任务额外奖励", "万事通","恭喜您完成第 {} 次万事通任务~ 请确认你的礼物。".format(num_dt),TaskRewards)
PlayerEvent.add_listener("OnTaskComplete",OnTaskComplete)


