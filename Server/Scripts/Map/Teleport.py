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
import time
import Utils.ServerUtils as ServerUtils
import Server.Envir.SEnvir as SEnvir
#Server.Envir.SEnvir.Log(__name__+"导入")
def DelayTeleport(args):            #进入
	Sender = args[0]
	map = args[1]
	map_num = map.Info.Index
	if Sender:
		current_map = SEnvir.GetMap(Sender.Character.CurrentMap)
		if map_num in Teleport_Location:
			teleport_target = Teleport_Location[map_num]
			m = teleport_target.get('MAP')
			x = teleport_target.get('X')
			y = teleport_target.get('Y')
			if map == current_map:
				Sender.TeleportByMapIndex(m,x,y)
				PlayerSetV(Sender,BV_NQ_KILLMON,0)
				PlayerSetV(Sender,BV_NQ_KILLNUM,0)
				Sender.Connection.ReceiveChat("退出任务房间。",MessageType.System)
				return
			else:
				return
		else:
			return
	else:
		return
Teleport_Location = {70:{'MAP':69,'X':63,'Y':73},
					 63:{'MAP':58,'X':297,'Y':74},
					 64:{'MAP':59,'X':246,'Y':273},
					 470:{'MAP':92,'X':51,'Y':131},
					 107:{'MAP':104,'X':175,'Y':183},
					 473:{'MAP':78,'X':239,'Y':193},
					 471:{'MAP':81,'X':51,'Y':57},
					 262:{'MAP':250,'X':50,'Y':54},
}
	
	