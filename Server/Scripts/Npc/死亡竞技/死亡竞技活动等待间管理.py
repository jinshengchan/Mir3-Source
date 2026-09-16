# -*- coding: utf-8 -*-
#载入模块SYS
import sys
import datetime
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import Server
import NpcEvent
import collections
import PlayerEvent
clr.AddReference('System')
import Server.Envir.SEnvir as SEnvir
from Utils import ServerUtils
import MapEvent

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
	
	if (Menu == 1):
		Sender.TeleportByMapIndex(1,461,364)          #飞地图ID X坐标 Y坐标
		return
		
#主菜单
	else:	
		say = """你好勇士，欢迎参加死亡竞技场活动。
		
		竞技场要求：<font color=\"0xff00ff00\">等级达到40以上才能参加</font>
		竞技场活动时间：<font color=\"0xff00ff00\">周日晚上20点准时开启</font>
		竞技场规则：<font color=\"0xff00ff00\">不能喝药，不能随机，不掉落装备，场内强制使用全体模式，禁止传送移行技能，看不到对方名字，无法查看对方装备</font>
		
		[我要离开:1]
		
		[等待活动开启:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(408,"OnClick",OnClick)
NpcEvent.add_listener(352,"OnClick",OnClick)
