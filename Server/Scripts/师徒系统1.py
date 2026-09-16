# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
from Defines import *
import collections
import NpcEvent
import Server
import xlwt
import xlrd
import datetime
from xlutils.copy import copy
from 变量.默认变量 import *
from Utils.PlayerUtils import *
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import Server.Envir.SEnvir as SEnvir
import os
import PlayerEvent
clr.AddReference('System')
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
	bg = {}
	font={}
	Dict={}
	say = ''

	if (Menu == 1):
		if (GetInventoryCount(Sender) >= 1): #格子大于等于2格
			shifu = str(SEnvir.GetCharacter(PlayerGetV(Sender,BV_ON_ADMISSION)))
			if SEnvir.GetPlayerByCharacter(shifu):
				if CheckReferral(Sender) != "IP检查通过":
					player = SEnvir.GetPlayerByCharacter(shifu)
					PlayerSetV(Sender,BV_ON_ADMISSION,0)
					PlayerSetV(player,BV_ON_ADMISSION,0)
					PlayerSetV(Sender,BV_MASTER_INDEX,player.Character.Index)
					PlayerSetV(player,BV_CURRENT_STUDENT1,Sender.Character.Index)
					PlayerSetV(Sender,BV_TU_BONUSCOUNT,0) #清除临时授业值
					Sender.GiveItem('师徒令',1)
					#不同等级赋值不同的变量
					if Sender.Level < 22:
						PlayerSetV(Sender,BV_LEVEL_REWARD,1)
					elif Sender.Level < 33:
						PlayerSetV(Sender,BV_LEVEL_REWARD,2)
					elif Sender.Level < 38:
						PlayerSetV(Sender,BV_LEVEL_REWARD,3)
					elif Sender.Level < 42:
						PlayerSetV(Sender,BV_LEVEL_REWARD,4)
					else:
						PlayerSetV(Sender,BV_LEVEL_REWARD,5)
					player.Connection.ReceiveChat("成功将 {} 收入师门。".format(Sender.Name),MessageType.System)
					Sender.Connection.ReceiveChat("你拜师成功，成为 {} 的徒弟。".format(player.Name),MessageType.System)
					return
				else:
					say = """相同IP或者相同网段无法执行拜师。
					
					[关闭:0]"""
			else:
				say = """无法拜入 {} 师门，请重试。
				
				[关闭:0]""".format(shifu)
		else:
			say ="""包裹需要保留一个格子，才可以拜师获得师徒令。
			请整理好包裹，在联系师父收你为徒。
			
			[关闭:0]"""
	elif (Menu == 2):
		shifu = str(SEnvir.GetCharacter(PlayerGetV(Sender,BV_ON_ADMISSION)))
		if SEnvir.GetPlayerByCharacter(shifu):
			player = SEnvir.GetPlayerByCharacter(shifu)
			player.Connection.ReceiveChat("{} 拒绝拜入你的门下。".format(Sender.Name),MessageType.System)
			Sender.Connection.ReceiveChat("你拒绝成为 {} 的徒弟。".format(player.Name),MessageType.System)
			return
	else:
		for player in SEnvir.Players:
			if PlayerGetV(player,BV_ON_ADMISSION) == Sender.Character.Index and PlayerGetV(Sender,BV_ON_ADMISSION) == player.Character.Index:
				say = """玩家 {} 向你发出收徒申请。
				
				<font color=\"0xff00ff00\">注意：拜师前包裹记得保留一个格子位置。</font>
				
				请点击：  [同意:1]      [拒绝:2]
				""".format(player.Name)

	Dict['Say'] = say                         #定义聊天框对话内容
	return Dict
	
def CheckReferral(myself):
	if not myself:
		return ""
	# 本人
	myself_level = myself.Level
	myself_creation_IP = myself.Character.Account.CreationIP
	myself_last_IP = myself.Character.Account.LastIP
	myself_current_IP = myself.Character.Account.Connection.IPAddress

	# 我的师傅
	shifu = SEnvir.GetCharacter(PlayerGetV(myself,BV_ON_ADMISSION))
	if not shifu:
		return "找不到师傅"

	shifu_creation_IP = shifu.Account.CreationIP
	shifu_last_IP = shifu.Account.LastIP

	if myself_creation_IP == shifu_creation_IP or myself_last_IP == shifu_last_IP or myself_current_IP == shifu_last_IP:
		return "师徒IP相同！"

	return "IP检查通过"

NpcEvent.add_listener(363,"OnClick",OnClick)
