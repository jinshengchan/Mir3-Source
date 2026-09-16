# -*- coding: utf-8 -*-
import clr
clr.AddReference("Library")
from Library import *
import MapEvent
from Globals import *
import Server
from Library import *
import Server.Envir.SEnvir as SEnvir
		
def Gumu2(args):
	Movement=args[0]
	Sender = args[1]      #玩家
	
	if Movement and Movement.ExtraInfo:
		if Movement.ExtraInfo == "开启":
			return True
		else:
			Sender.Connection.ReceiveChat("感受到强大的力量阻止你进入",MessageType.System)

	return False     


# 6271为地图链接ID
MapEvent.add_listener(6271,"OnMovement",Gumu2)
MapEvent.add_listener(6272,"OnMovement",Gumu2)
MapEvent.add_listener(6273,"OnMovement",Gumu2)
MapEvent.add_listener(6274,"OnMovement",Gumu2)

MapEvent.add_listener(6275,"OnMovement",Gumu2)
MapEvent.add_listener(6276,"OnMovement",Gumu2)
MapEvent.add_listener(6277,"OnMovement",Gumu2)
MapEvent.add_listener(6278,"OnMovement",Gumu2)

MapEvent.add_listener(6279,"OnMovement",Gumu2)
MapEvent.add_listener(6280,"OnMovement",Gumu2)
MapEvent.add_listener(6281,"OnMovement",Gumu2)
MapEvent.add_listener(6282,"OnMovement",Gumu2)

MapEvent.add_listener(6283,"OnMovement",Gumu2)
MapEvent.add_listener(6284,"OnMovement",Gumu2)
MapEvent.add_listener(6285,"OnMovement",Gumu2)
MapEvent.add_listener(6286,"OnMovement",Gumu2)

MapEvent.add_listener(6287,"OnMovement",Gumu2)
MapEvent.add_listener(6288,"OnMovement",Gumu2)
MapEvent.add_listener(6289,"OnMovement",Gumu2)
MapEvent.add_listener(6290,"OnMovement",Gumu2)
