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
	
	ServerUtils.SpawnMonsters("地下魔宫", "地天灭王", 1, 31, 19, 5)
	ServerUtils.SpawnMonsters("诺玛勇士坟墓", "诺玛教主", 1, 27, 39, 10)

	return