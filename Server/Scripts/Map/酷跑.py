# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
import Server
from Defines import *
import random
import NpcEvent
from datetime import datetime, timedelta
import System
s1 = clr.Reference[System.Object]()
from Utils.TimeUtil import *
import Utils.ServerUtils as ServerUtils
from Utils import ServerUtils
from Npc import *

def OnEnter(args):            #进入
	map = args[0]
	Sender = args[1]
	
	for i in range(len(Sender.Pets)-1,-1,-1):
		Sender.Pets[i].SetHP(0)

	

MapEvent.add_listener(562,"OnEnter",OnEnter)
MapEvent.add_listener(563,"OnEnter",OnEnter)

