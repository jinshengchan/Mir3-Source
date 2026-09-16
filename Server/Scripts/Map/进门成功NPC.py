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
	
	if(PlayerGetV(Sender,BV_MAP_TARGET)==107):
		say = """呼呼呼，虽然我也不知道怎么通过困魔咒，但你还是来晚了。因为我已经把不怒法师（不老不死）的力量汇聚到我 
为了祝贺我即升级为世界霸主，我将把你作为第一份祭礼。而且，我所获得的那个永远不死的躯体已经成为我忠实的仆从，让你见识一下我的力量吧。
"""
	else:
		return

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(296,"OnClick",OnClick)