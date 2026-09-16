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
			Sender.GiveItem("绿玫瑰",1)  #给与奖励
			map = Server.Envir.SEnvir.CreateMap(535)                         #开启副本地图（地图ID）
			map.MapTime = datetime.now()+ timedelta(minutes=30);  #副本地图关卡时间设置
			Sender.Teleport(map,23,48)	#飞地图ID X坐标 Y坐标
			map.CreateMon(50,48,100,'副本-猿猴',15)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(50,48,50,'副本-魔神怪',15)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(50,48,50,'副本-暗黑战士',10)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(50,48,50,'副本-沃玛战将',20)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(50,48,50,'难民弓箭手',10)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(50,48,50,'精英弓箭手',2)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(40,30,50,'经验小兔兔',8)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			map.CreateMon(50,48,1,'花怪1',1)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）

		else:
			str = """地图里还有怪物没打完，你当我瞎子么
			
			[离开:0]"""	
	
#主菜单
	else:
		str = """限时通关可以获得绝世宝藏
		
		[下层:1] 杀光了所有怪物，挑战下一层
		
		[离开:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict


NpcEvent.add_listener(356,"OnClick",OnClick)
