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


def OnAcceptQuest(args):
	Sender=args[0]
	QuestInfo=args[1]


	#Sender.Connection.ReceiveChat("你接受了任务: {}".format(QuestInfo.QuestName),MessageType.System)

PlayerEvent.add_listener("OnAcceptQuest",OnAcceptQuest)
