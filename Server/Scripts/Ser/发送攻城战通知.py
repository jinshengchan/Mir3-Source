# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import datetime
import collections
import clr
clr.AddReference("Library")
clr.AddReference("System")
from Library import *
from System import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils


def SendMsgBeforeConquestWar(dont_care):
	if not SEnvir.UserConquestList or SEnvir.UserConquestList.Count < 1:
		return

	for conquest in SEnvir.UserConquestList.Binding:
		warTime = conquest.WarDate + conquest.Castle.StartTime

		if warTime < SEnvir.Now:
			continue

		warTimeFromNow = warTime - SEnvir.Now

		if warTimeFromNow > System.TimeSpan.FromDays(3):
			continue

		# 提前30分钟
		SchedulePreWarNotice(["距离{}攻城战开始还有30分钟".format(conquest.Castle.Name), warTime - System.TimeSpan.FromMinutes(30)])
		# 提前1小时
		SchedulePreWarNotice(["距离{}攻城战开始还有60分钟".format(conquest.Castle.Name), warTime - System.TimeSpan.FromMinutes(60)])



def SchedulePreWarNotice(param):
	SEnvir.ScheduledCall("Utils.ServerUtils.SendMsgToAll", param[1], param[0]) 
