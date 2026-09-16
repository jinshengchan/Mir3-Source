# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import clr

clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
import Server.Envir.SEnvir as SEnvir
clr.AddReference("System.Core")
clr.AddReference('System')
import System
clr.ImportExtensions(System.Linq)

# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *

import unicodedata
######################################################
# 本函数为程序调用的固定格式 函数名和参数数量不要修改
# OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict = {}

	if (Menu == 1):
		say = "下面是已经提交的攻城战:\n\n"
		count = 1
		for conquest in SEnvir.UserConquestList.Binding:
			say += '{}. {} 对 {} 的攻城战, 开始时间: {}\n'.format(count, conquest.Guild.GuildName, 
				conquest.Castle.Name, conquest.WarDate + conquest.Castle.StartTime)
			count += 1
			
	elif (Menu == 2):
		say = """诺玛攻城暂未开放
			
		[关闭:0]"""
	elif (Menu == 3):
		# 这里建议用NPC的index
		# 也可以用NPC的名字 ServerUtils.GetNPCObject("行会指引")
		NPCObject = ServerUtils.GetNPCObject(220)
		if NPCObject:
			Sender.NPC = NPCObject
			newArgs = [Self, Sender, 0]
			return Npc.行会指引.OnClick(newArgs)
		else:
			say = "未找到指定的NPC"
	# 主菜单
	else:
		say = """公告板用于行会注册，宣传或接受新人加入行会。
		没有行会的玩家可以申请加入行会。
		另外，还可以查看有关攻城的信息。
	
		[查询:1] 沙巴克攻城
		
		[查询:3] 行会
		
		[关闭:0]"""

	Dict['Say'] = say  # 定义聊天框对话内容
	return Dict


NpcEvent.add_listener(228, "OnClick", OnClick)
NpcEvent.add_listener(229, "OnClick", OnClick)
NpcEvent.add_listener(230, "OnClick", OnClick)
NpcEvent.add_listener(231, "OnClick", OnClick)
NpcEvent.add_listener(232, "OnClick", OnClick)
