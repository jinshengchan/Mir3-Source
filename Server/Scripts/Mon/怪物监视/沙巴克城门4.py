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
	
	GlobalSetV(GV_MON_SBKCMHP4,monster.CurrentHP)      #沙巴克城门1血量记录
	GlobalSetV(GV_MON_SBKCMON4,int(monster.Direction))      #沙巴克城门1开关状态记录

MonsterEvent.add_listener(40008,"OnProcessAI",OnProcessAI)