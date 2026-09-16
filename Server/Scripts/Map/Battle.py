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
#Server.Envir.SEnvir.Log(__name__+"导入")

_COUNT_TIME = 1;			#计算怪物剩余数量的时间间隔;
_INFORM_TIME = 5;			#通知怪物剩余数量的时间间隔;

_V_STATUS = 1;			#开启下一刷怪状态(清理当前房间的所有怪物)(0--重置数量,1--刷怪完成,2--正在刷怪);
_V_TIME = 2;			#倒计时时间记录状态(用于异常掉线下重连);
_V_OPEN = 4;			#副本开启状态();
_V_NUM =5;				#第几波;

_MonList=[	{'mon':[[21,7],[13,7],[20,7],],'sec':1800},#第一波怪物id 和数量   时间限制秒
			{'mon':[[13,21],],'sec':1800},#第二波怪物id 和数量   时间限制秒
			{'mon':[[20,21],],'sec':1800},{'mon':[[22,21],],'sec':1800},{'mon':[[43,21],],'sec':1800},
			{'mon':[[44,21],],'sec':1800},{'mon':[[15,21],],'sec':1800},{'mon':[[18,21],],'sec':1800},
			{'mon':[[14,21],],'sec':1800},{'mon':[[19,21],],'sec':1800},{'mon':[[27,21],],'sec':1800},
			{'mon':[[29,21],],'sec':1800},{'mon':[[26,21],],'sec':1800},{'mon':[[28,21],],'sec':1800},
			{'mon':[[35,21],],'sec':1800},{'mon':[[34,21],],'sec':1800},{'mon':[[33,21],],'sec':1800},
			{'mon':[[46,21],],'sec':1800},{'mon':[[32,21],],'sec':1800},{'mon':[[47,21],],'sec':1800},
			{'mon':[[38,21],],'sec':1800},{'mon':[[41,21],],'sec':1800},{'mon':[[40,21],],'sec':1800},
			{'mon':[[62,21],],'sec':1800},{'mon':[[61,21],],'sec':1800},{'mon':[[63,21],],'sec':1800},
			{'mon':[[58,21],],'sec':1800},{'mon':[[57,21],],'sec':1800},{'mon':[[125,21],],'sec':1800},
			{'mon':[[127,21],],'sec':1800},{'mon':[[124,21],],'sec':1800},{'mon':[[126,21],],'sec':1800},
			{'mon':[[50,21],],'sec':1800},{'mon':[[53,21],],'sec':1800},{'mon':[[52,21],],'sec':1800},
			{'mon':[[54,21],],'sec':1800},{'mon':[[117,21],],'sec':1800},{'mon':[[119,21],],'sec':1800},
			{'mon':[[118,21],],'sec':1800},{'mon':[[116,21],],'sec':1800},{'mon':[[66,21],],'sec':1800},
			{'mon':[[72,21],],'sec':1800},{'mon':[[71,21],],'sec':1800},{'mon':[[69,21],],'sec':1800},
			{'mon':[[70,21],],'sec':1800},{'mon':[[89,21],],'sec':1800},{'mon':[[91,21],],'sec':1800},
			{'mon':[[90,21],],'sec':1800},{'mon':[[82,21],],'sec':1800},{'mon':[[86,21],],'sec':1800},
			{'mon':[[107,21],],'sec':1800},{'mon':[[108,21],],'sec':1800},{'mon':[[110,21],],'sec':1800},
			{'mon':[[112,21],],'sec':1800},{'mon':[[113,21],],'sec':1800},{'mon':[[77,21],],'sec':1800},
			{'mon':[[78,21],],'sec':1800},{'mon':[[76,21],],'sec':1800},{'mon':[[109,21],],'sec':1800},
			{'mon':[[111,21],],'sec':1800},{'mon':[[130,21],],'sec':1800},{'mon':[[131,21],],'sec':1800},
			{'mon':[[137,21],],'sec':1800},{'mon':[[134,21],],'sec':1800},{'mon':[[136,21],],'sec':1800},
			{'mon':[[138,21],],'sec':1800},{'mon':[[132,21],],'sec':1800},{'mon':[[151,21],],'sec':1800},
			{'mon':[[156,21],],'sec':1800},{'mon':[[152,21],],'sec':1800},{'mon':[[157,21],],'sec':1800},
			{'mon':[[155,21],],'sec':1800},{'mon':[[153,21],],'sec':1800},{'mon':[[158,21],],'sec':1800},
			{'mon':[[154,21],],'sec':1800},{'mon':[[165,21],],'sec':1800},{'mon':[[161,21],],'sec':1800},
			{'mon':[[164,21],],'sec':1800},{'mon':[[163,21],],'sec':1800},{'mon':[[162,21],],'sec':1800},
			{'mon':[[99,21],],'sec':1800},{'mon':[[106,21],],'sec':1800},{'mon':[[97,21],],'sec':1800},
			{'mon':[[100,21],],'sec':1800},{'mon':[[103,21],],'sec':1800},{'mon':[[101,21],],'sec':1800},
			{'mon':[[102,21],],'sec':1800},{'mon':[[174,21],],'sec':1800},{'mon':[[176,21],],'sec':1800},
			{'mon':[[168,21],],'sec':1800},{'mon':[[171,21],],'sec':1800},{'mon':[[173,21],],'sec':1800},
			{'mon':[[225,21],],'sec':1800},{'mon':[[226,21],],'sec':1800},{'mon':[[221,21],],'sec':1800},
			{'mon':[[227,21],],'sec':1800},{'mon':[[223,21],],'sec':1800},{'mon':[[224,21],],'sec':1800},
			{'mon':[[228,21],],'sec':1800},{'mon':[[222,21],],'sec':1800},
		]
		
#_monlists = collections.OrderedDict(_MonList)
	
def OnCreate(args):    #创建副本
	map = args[0]
	sender=args[1]
	Server.Envir.SEnvir.DelayCall("Map.Battle.CloseFuben",3600,(map,))   #地图总时间 秒为单位
	MapSetTempV(map,_V_NUM,0)               #设定值     
	Server.Envir.SEnvir.DelayCall("Map.Battle.ManualCloseFuben",5,(map,0))   #5秒判断一次地图是否有人如果没有则关闭掉这个副本节约资源
	
def OnEnter(args):            #进入副本
	map = args[0]
	sender = args[1]
	sender.Connection.ReceiveChat(map.Info.Description,MessageType.System)  #进入副本提示
	MonsterCount((map,sender,MapGetTempV(map,_V_NUM)))
	
def ManualCloseFuben(args):   #判断关闭副本
	map=args[0]
	count = args[1]
	if(map is None):
		return
	if(map.PlayerCount == 0):
		count+=1
	else:
		count = 0
	if(count >= 6):
		CloseFuben((map,))
		return
	Server.Envir.SEnvir.DelayCall("Map.Battle.ManualCloseFuben",5,(map,count))   #重复判断
	
def CloseFuben(args):            #关闭副本
	map=args[0]
	if(map is None):
		return
	Server.Envir.SEnvir.CloseMap(map.Info)
	
def MonsterCount(args):         #怪物总数
	map = args[0]
	sender = args[1]
	index = args[2]
	if(sender is None or map is None):         #如果玩家不在线, 副本地图为空
		return
	inmap = Server.Envir.SEnvir.GetMap(map.Info)  # 判断地图是否存在
	if(inmap is None):
		#Server.Envir.SEnvir.Log("地图退出")
		return
	if (sender.CurrentMap!= map):    #判断玩家已经不在副本地图(单人地图需要)
		return
	if (map.MonsterCount == 0 ):#没有怪物就刷怪
		if (index >= len(_MonList)):#成功到底
			sender.Connection.ReceiveChat("成功到底",MessageType.System)
			return
		Server.Envir.SEnvir.DelayCall("Map.Battle.CreateMon",3,(map,sender,index))
		return
	if(map.Expiry < Server.Envir.SEnvir.Now):#判断小关卡时间是否到期
		Server.Envir.SEnvir.Log("地图退出")
		CloseFuben((map,))
		return
	#sender.Connection.ReceiveChat('%d'%map.MonsterCount,MessageType.System)
	map.MapMsg("地图剩余怪物"+'%d'%map.MonsterCount,MessageType.System)
	Server.Envir.SEnvir.DelayCall("Map.Battle.MonsterCount",1,(map,sender,index))

def CreateMon(args):
	map = args[0]
	sender = args[1]
	index = args[2]
	if(map is None):         #判断副本地图为空
		return
	inmap = Server.Envir.SEnvir.GetMap(map.Info)  # 判断地图是否存在
	if(inmap is None):
		#Server.Envir.SEnvir.Log("地图退出")
		return
	if (index >= len(_MonList)):  #判断关卡是否完成
		return
	moli = _MonList[index]
	modi=moli['mon']
	sec = moli['sec']
	for li in modi:
		map.CreateMon(53,33,10,li[0],li[1]) #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
	map.Expiry = datetime.datetime.now()+datetime.timedelta(seconds=sec);#设置分关卡时间	           
	MapSetTempV(map,_V_NUM,index+1)
	Server.Envir.SEnvir.DelayCall("Map.Battle.MonsterCount",1,(map,sender,index+1))
	
MapEvent.add_listener(462,"OnEnter",OnEnter)                           #定义NPC 613的地图ID引用创建副本
MapEvent.add_listener(462,"OnCreate",OnCreate)                         #定义NPC 613的地图ID开启副本