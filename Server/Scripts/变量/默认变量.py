# -*- coding: utf-8 -*-
import sys
import random

import collections
import clr
clr.AddReference("Library")
from Library import *

#全局任务奖励倍率（可设置非整数倍）
Local_ExpRewards_Rate = 0.1           #经验
Local_GoldRewards_Rate = 0.1          #金币
Local_PresRewards_Rate = 1          #声望

#强元素，弱元素种类，默认无体质
ElementResistanceList = [ Stat.FireResistance, Stat.IceResistance, Stat.LightningResistance, Stat.WindResistance, Stat.HolyResistance, Stat.DarkResistance, Stat.PhantomResistance, ]

def Teleport(args): #传送
	Sender= args[0]
	map = args[1]
	x= args[2]
	y= args[3]
	
	Sender.Teleport(map,x,y)
	
