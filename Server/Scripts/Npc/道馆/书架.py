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
import MapEvent
import NpcEvent
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from 主线任务奖励 import *
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
	map = SEnvir.GetMap(Sender.Character.CurrentMap)
	Dict={}

#主菜单
	if(PlayerGetV(Sender,BV_NQ_MAIN)==160):
		PlayerSetV(Sender,BV_NQ_MAIN,161)
		Sender.GiveItem('地狱神钟',1)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """这好像就是无名老人说的那个东西。。。 赶快拿去给商人，找回沃玛金牌。
			
			[结束:0]"""
	else:
		say = """你是抓不到我的！
			
			[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(285,"OnClick",OnClick)
