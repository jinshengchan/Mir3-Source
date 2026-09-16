# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import MapEvent
import random
from Defines import *
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
from Map.进门条件列表 import *
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, nqvalue)
##参数 Self：NPC的类
##   Sender：玩家的类
##     nqvalue：菜单的类
#####################################################
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	mapt = PlayerGetV(Sender,BV_MAP_TARGET)
	list = Limited_Map[mapt]
	v2 = list.get('value2')
	i = list.get('item')
	c = list.get('ItemCount')
	u = list.get('TakeItem')
	x = list.get('X')
	y = list.get('Y')
	r = list.get('Range')
	t = list.get('TimeLimit')
	p = list.get('PlayerLimit')
	x1 = list.get('EnterX')
	y1 = list.get('EnterY')

#主菜单
	if(Menu == 1):
		if(PlayerGetV(Sender,BV_NQ_SJKILL)< 5000):
			PlayerSetV(Sender,BV_NQ_SJKILL,5001)
			Sender.TeleportByMapIndex(27,435,79)
			return
		else:
			Sender.TeleportByMapIndex(27,435,79)
			return
	else:
		if(PlayerGetV(Sender,BV_MAP_TARGET)==27):
			say = """（这里什么时候有了这样一扇门？）
				
				[走入这扇门:1]
				[到神舰别处去看看:0]"""
		elif(PlayerGetV(Sender,BV_MAP_TARGET)==63):
			if(PlayerGetV(Sender,BV_NQ_MAIN)==88):
				PlayerSetV(Sender,BV_NQ_MAIN,89)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say =  """（这儿的入口是被特殊魔法封住的。
					我们得去告诉比奇城城主。。。）"""
			else:
				say = """（门被堵住了。）"""
		elif(PlayerGetV(Sender,BV_MAP_TARGET)==64):
			if(PlayerGetV(Sender,BV_NQ_MAIN) < 107):
				say = """（被一种不知名的力量堵住了。）"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN) == 107):
				say = """看来不借助  <font color=\"0xff00ff00\"> {} </font>  的力量无法进去......""".format(i)
			else:
				say = """（门被堵住了。）"""
		elif(PlayerGetV(Sender,BV_MAP_TARGET)==107):
			if(PlayerGetV(Sender,BV_NQ_MAIN)==138):
				PlayerSetV(Sender,BV_NQ_MAIN,139)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """（他妈的，这种困魔咒和以前在半兽勇士的洞穴里见过的一样。拥有不死牌的署箭道士一定在里面）"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN) == 144):
				say = """看来不借助  <font color=\"0xff00ff00\"> {} </font>  的力量无法进去......""".format(i)
			elif(PlayerGetV(Sender,BV_NQ_MAIN) == 145):
				say = """看来不借助  <font color=\"0xff00ff00\"> {} </font>  的力量无法进去......""".format(i)
			elif(PlayerGetV(Sender,BV_NQ_MAIN) > 145):
				say = """（这里被打上封条了）"""
			else:
				say = """（无从知晓的困魔咒。。。）"""
		elif(PlayerGetV(Sender,BV_MAP_TARGET)==471):
			if(165 < PlayerGetV(Sender,BV_NQ_MAIN) < 170):
				say = """看来不借助  <font color=\"0xff00ff00\"> {} </font>  的力量无法进去......""".format(i)
			else:
				say = """（门被堵住了。）"""
		else:
			say = """（门被堵住了。。。）"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(265,"OnClick",OnClick)