# -*- coding: utf-8 -*-
#载入模块SYS
import sys
from datetime import datetime, timedelta
#引用模块的地址
from Globals import *
import clr
import System
import collections
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import Server
import NpcEvent
from Utils.TimeUtil import *
import MapEvent

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	str = ""
	
	current_map = SEnvir.GetMap(Sender.Character.CurrentMap)        #先获取当前角色所在的地图
	
	if (Menu == 1):
		if (current_map.MonsterCount == 0 ):    #判断当前角色所在地图是否还有怪物
			Sender.GiveItem("BOSS宝箱",1)  #给与奖励
			map = Server.Envir.SEnvir.CreateMap(1506)                         #开启副本地图（地图ID）
			map.MapTime = datetime.now()+ timedelta(minutes=30);  #副本地图关卡时间设置
			Sender.Teleport(map,31,107)	#飞地图ID X坐标 Y坐标
			map.CreateMon(104,27,1,'超级骷髅教主',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）

		else:
			str = """地图里还有怪物没打完，你当我瞎子么
			
			[离开:0]"""	
	
#主菜单
	else:
		str = """限时通关可以获得绝世宝藏
		
		[我挑战完成了:1] 杀光了所有怪物，挑战下一层
		
		[离开:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict


NpcEvent.add_listener(339,"OnClick",OnClick)
