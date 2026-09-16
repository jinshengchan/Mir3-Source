# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import NpcEvent
import Server.Envir.SEnvir as SEnvir
from Library import *

import clr
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)
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
	say = "" 
	
	#if Self.IsNew and Self.Current == Sender and Self.NPCName == "中立旗帜(争夺中)":
	if (GlobalGetV(GV_PLAYER_SBKCMFW) == 0) and Self.Current == Sender and Self.NPCName == "中立旗帜(争夺中)":
		map = Sender.CurrentMap
		Server.Envir.SEnvir.DelayCall("Npc.自定义NPC.Change",12,(Self,map))
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def Change(args):
	NPC = args[0]
	map = args[1]
	#if NPC.IsNew == False:
	if GlobalGetV(GV_PLAYER_SBKCMFW) == 0:
		cell = map.Cells[234,191]
		flag = True
		if cell.Objects != None:
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530:
					flag = False
		if flag:
			GlobalSetV(GV_PLAYER_SBKCMFW,1)
			map.CreateMon(234,191,0,'沙巴克城门1',1)
			map.CreateMon(169,191,0,'沙巴克城门3',1)
			map.CreateMon(234,127,0,'沙巴克城门4',1)
			for object in cell.Objects:
				if object != None and object.Race == ObjectType.Monster and object.MonsterInfo.BodyShape == 530:
					object.Direction = object.CurrentDir
					objcetTurn = System.Activator.CreateInstance(Network.ServerPackets.ObjectTurn)
					objcetTurn.ObjectID = object.ObjectID
					objcetTurn.Direction = object.Direction
					objcetTurn.Location =  object.CurrentLocation
					object.Broadcast(objcetTurn)
					map.CreateNpc(234,190,344)
					map.CreateNpc(233,191,344)
					map.CreateNpc(235,190,344)
					map.CreateNpc(168,190,344)
					map.CreateNpc(170,191,344)
					map.CreateNpc(169,190,344)
					map.CreateNpc(232,127,344)
					map.CreateNpc(233,127,344)
					map.CreateNpc(234,128,344)
					break
		
#NpcEvent.add_listener(999999,"OnClick",OnClick)