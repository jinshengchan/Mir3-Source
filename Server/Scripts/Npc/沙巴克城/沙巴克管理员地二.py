# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import System
s1 = clr.Reference[System.Object]()
import Server
import PlayerEvent
clr.AddReference('System')
import Server.Envir.SEnvir as SEnvir
from Utils import ServerUtils
import MapEvent
from Utils.TimeUtil import *
import datetime
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}

	map = SEnvir.GetMap(551)               #开启地图
	tmap = SEnvir.GetMap(552)               #要去的地图
	randomLocation = tmap.GetRandomLocation()      #取随机数坐标值
	if map.GetAliveMonsterCount("宝盒") < 1:
		#先判断城池的名字
		guild = SEnvir.GetGuildFromCastleName("沙巴克")
		#如果 角色行会为空 或 行会不是沙巴克成员
		if (not Sender.Character.Account.GuildMember) or (Sender.Character.Account.GuildMember.Guild != guild):
			if (Sender.Gold < 200000):
				say = """你没有足够的金币，无法传送。
				
				[离开:0]"""
			else:
				SubGold(Sender,200000)
				Sender.TeleportByMapIndex(552,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
				return
		else:
			Sender.TeleportByMapIndex(552,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
			return
	else:
		say = """地图的宝盒还没清理干净，无法进入下一层。
		
		[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(347,"OnClick",OnClick)