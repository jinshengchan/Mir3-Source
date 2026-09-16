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
	
	ServerUtils.SpawnMonsters("生死关", "触龙神", 1, 84, 169, 1)
	ServerUtils.SpawnMonsters("真天宫", "震天魔神", 1, 19, 37, 5)

	return