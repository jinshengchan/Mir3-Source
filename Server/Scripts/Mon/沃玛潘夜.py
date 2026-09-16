# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import datetime
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils

def RefreshMonster(dont_care):
	
	ServerUtils.SpawnMonsters("沃玛神殿", "沃玛教主", 1, 51, 50, 1)
	ServerUtils.SpawnMonsters("潘夜神殿", "潘夜牛魔王", 1, 51, 51, 1)

	return
