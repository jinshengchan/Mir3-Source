# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
from Defines import *
import PlayerEvent
import Server
import clr
import random
import Utils.Colors as Colors

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir

def generateOption(Text='Hi', LocationXOffset=30, LocationYOffset=30, NPCIndex=184, TextColor=Colors.白色):
    return {'Text':Text, 'LocationX': LocationXOffset, 'LocationY': LocationYOffset, 'NPCIndex': NPCIndex, 'TextColor': TextColor}

def OnDKey(args):
    Sender = args[0]

    return 211

PlayerEvent.add_listener("OnDKey",OnDKey)
