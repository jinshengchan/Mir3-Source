# -*- coding: utf-8 -*-
#载入模块SYS
import sys
import datetime
#引用模块的地址
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
from Globals import *
from Utils import ServerUtils
from Defines import *
import Server
import MonsterEvent
import Server.Envir.SEnvir as SEnvir
import Server.Envir as Envir
import random

def OnProcessAI(args):
	monster = args[0]
	
	select = random.randint(0, 3)
	
	hp_percent = monster.CurrentHP * 100.0 / monster.Stats[Stat.Health]
	
	if (select == 0) and not monster.Target is None:
		monster.LineAoE(12, -2, 12, MagicType.ScortchedEarth, Element.Fire)

MonsterEvent.add_listener(100424,"OnProcessAI",OnProcessAI)
MonsterEvent.add_listener(100483,"OnProcessAI",OnProcessAI)

