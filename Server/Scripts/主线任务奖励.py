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
from 变量.默认变量 import *
import Server.Envir.SEnvir as SEnvir
######################################################
#本函数为程序调用的固定格式 函数名和参数数量不要修改
#OnClick(Self, Sender, Menu)
##参数 Self：NPC的类
##   Sender：玩家的类
##     Menu：菜单的类
#####################################################
def MainQuestRewards(Sender,QuestType = BV_NQ_MAIN ):
	nq = PlayerGetV(Sender,QuestType)
	if QuestType == BV_NQ_MAIN: 
		MainQuestList = GetMainTaskList(Sender,nq)
	elif QuestType == BV_NQ_SJKILL:
		MainQuestList = GetSJTaskList(Sender,nq-5000)
	exp = MainQuestList[4]
	money = MainQuestList[5]
	sw = MainQuestList[6]
	nq += 1
	PlayerSetV(Sender,QuestType,nq)
	converted_reward = []
	if exp:
		exp1 = exp * Local_ExpRewards_Rate
		GiveExperience(Sender,exp1)
	if money:
		money1 = money * Local_GoldRewards_Rate
		GiveGold(Sender,money1)
		Sender.Connection.ReceiveChat("得到 {} 金币。".format(money1), MessageType.System)
	if sw:
		sw1 = sw *Local_PresRewards_Rate
		GivePrestige(Sender,sw1)
		Sender.Connection.ReceiveChat("得到 {} 点 声望。".format(sw1), MessageType.System)
	if MainQuestList[7]:
		i = MainQuestList[7]
		n = MainQuestList[8]
		grids = ItemUseIvetoryCount(i,n)
		if (GetInventoryCount(Sender) >= grids): #格子大于等于N数量
			Sender.GiveItem(i,n)
		else:
			converted_reward.append((i, n, True))
	if MainQuestList[9]:
		i = MainQuestList[9]
		n = MainQuestList[10]
		if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
			Sender.GiveItem(i,n)
		else:
			converted_reward.append((i, n, True))
	if Sender.Gender == Sender.Gender.Male:
		if Sender.Class == Sender.Class.Assassin:
			if MainQuestList[23]:
				i = MainQuestList[23]
				n = MainQuestList[24]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
		elif Sender.Class == Sender.Class.Wizard:
			if MainQuestList[15]:
				i = MainQuestList[15]
				n = MainQuestList[16]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
		elif Sender.Class == Sender.Class.Warrior:
			if MainQuestList[11]:
				i = MainQuestList[11]
				n = MainQuestList[12]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
		else:
			if MainQuestList[19]:
				i = MainQuestList[19]
				n = MainQuestList[20]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
	if Sender.Gender == Sender.Gender.Female:
		if Sender.Class == Sender.Class.Assassin:
			if MainQuestList[25]:
				i = MainQuestList[25]
				n = MainQuestList[26]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
		elif Sender.Class == Sender.Class.Wizard:
			if MainQuestList[17]:
				i = MainQuestList[17]
				n = MainQuestList[18]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
		elif Sender.Class == Sender.Class.Warrior:
			if MainQuestList[13]:
				i = MainQuestList[13]
				n = MainQuestList[14]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
		else:
			if MainQuestList[21]:
				i = MainQuestList[21]
				n = MainQuestList[22]
				if (GetInventoryCount(Sender) >= n): #格子大于等于N数量
					Sender.GiveItem(i,n)
				else:
					converted_reward.append((i, n, True))
	# 发奖
	if len(converted_reward)>0:
		Sender.PYMailSend("任务系统", "系统", "包裹满，任务发送邮件", converted_reward)
		Sender.Connection.ReceiveChat("由于你包裹满，任务奖励邮件发送", MessageType.System)
