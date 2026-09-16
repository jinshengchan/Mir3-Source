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
	
	ServerUtils.SpawnMonsters("赤月恶魔洞穴", "赤月恶魔", 1, 23, 18, 1)
	ServerUtils.SpawnMonsters("调控室", "霸王教主", 1, 32, 31, 10)

	return