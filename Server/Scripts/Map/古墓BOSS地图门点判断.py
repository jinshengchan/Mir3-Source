# -*- coding: utf-8 -*-
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
from Globals import *
import Server
from Library import *
import Server.Envir.SEnvir as SEnvir
		
def GumuBoss(args):
	Movement=args[0]
	Sender = args[1]      #玩家
	
	if Movement and Movement.ExtraInfo:
		if Movement.ExtraInfo == "开启":
			return True
		else:
			Sender.Connection.ReceiveChat("感受到强大的力量阻止你进入",MessageType.System)

	return False     


# 3251为地图链接ID
MapEvent.add_listener(3251,"OnMovement",GumuBoss)
MapEvent.add_listener(3252,"OnMovement",GumuBoss)
MapEvent.add_listener(3253,"OnMovement",GumuBoss)
MapEvent.add_listener(3254,"OnMovement",GumuBoss)
MapEvent.add_listener(3255,"OnMovement",GumuBoss)
MapEvent.add_listener(3256,"OnMovement",GumuBoss)

