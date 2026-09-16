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
			Sender.GiveItem("经验爆率补药",1)  #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			Sender.TeleportByMapIndex(7,400,125)	
		else:
			str = """还有怪物的嚎叫，我害怕
			
			[离开:0]"""	
	
#主菜单
	else:
		str = """虚空恢复了平静，我想静静……
		
		[送我回去:1] 
		
		[离开:0]"""
	Dict['Say']=str                         #定义聊天框对话内容
	return Dict


NpcEvent.add_listener(395,"OnClick",OnClick)
NpcEvent.add_listener(396,"OnClick",OnClick)
NpcEvent.add_listener(397,"OnClick",OnClick)