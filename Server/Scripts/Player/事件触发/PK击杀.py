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


def OnKillPlayer(args):
	Sender = args[0]
	Victim = args[1]

	#Sender.Connection.ReceiveChat("你击杀了玩家{}".format(Victim.Name), MessageType.System)

    


PlayerEvent.add_listener("OnKillPlayer",OnKillPlayer)
