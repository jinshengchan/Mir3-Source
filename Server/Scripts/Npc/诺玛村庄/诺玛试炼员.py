# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
from Npc.商店列表 import *
from 变量.默认变量 import *
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

	if (Menu == 1):
		map = Sender.CurrentMap
		if map.MonsterCount > 0:
			say = """当前地图的怪物还没清理干净。
			
			[关闭:0]"""
		else:
			index = PlayerGetV(Sender,GV_PLAYER_NMDIEMAP)
			x = PlayerGetV(Sender,GV_PLAYER_NMDIEMAPX)
			y = PlayerGetV(Sender,GV_PLAYER_NMDIEMAPY)
			Sender.TeleportByMapIndex(index,x + 1,y + 1)
			return
#主菜单
	else:
		say = """见到你真好。这里四处都是怪物，我很担心。。。
		
		[离开:1]"""#.format(PlayerGetV(Sender,GV_PLAYER_NMDIEMAP),PlayerGetV(Sender,GV_PLAYER_NMDIEMAPX),PlayerGetV(Sender,GV_PLAYER_NMDIEMAPY))

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(375,"OnClick",OnClick)

