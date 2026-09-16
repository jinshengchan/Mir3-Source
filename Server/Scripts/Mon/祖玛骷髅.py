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
	
	ServerUtils.SpawnMonsters("祖玛教主宫廷", "祖玛教主", 1, 21, 19, 1)
	ServerUtils.SpawnMonsters("潘夜石窟5层", "骷髅教主", 1, 200, 200, 1)

	return