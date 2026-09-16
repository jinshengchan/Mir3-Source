# -*- coding: utf-8 -*-
# 载入模块SYS
import sys
# 引用模块的地址
from Globals import *
import collections
from Defines import *
import PlayerEvent
import Server
import clr
import random

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir

GUMU_QUESTS = [10898,10899,10900]  #需要完成任务的序号，指定的3个古墓任务


CHAR_MIN = 1
CHAR_MAX = 24


def GetQuestChar(Sender, QuestIndex):
	Quest = Sender.GetUserQuestByQuestIndex(QuestIndex)
	if Quest is None or not Quest.ExtraInfo:
		return None

	try:
		Char = int(Quest.ExtraInfo)
	except (TypeError, ValueError):
		return None

	if Char < CHAR_MIN or Char > CHAR_MAX:
		return None
	return Char


def GetRandomChar(Used):
	Available = [value for value in range(CHAR_MIN, CHAR_MAX + 1) if value not in Used]
	return str(random.choice(Available))


def OnCompleteQuest(args):
	Sender = args[0]
	UserQuest = args[1]
	QuestInfo = UserQuest.QuestInfo

	if QuestInfo.Index in GUMU_QUESTS:
		GumuQuest(Sender, UserQuest, QuestInfo)


def GumuQuest(Sender, UserQuest, QuestInfo):
	if UserQuest.ExtraInfo:
		return

	Used = []
	if QuestInfo.Index == 10899:
		firstChar = GetQuestChar(Sender, 10898)
		if firstChar is None:
			return
		Used.append(firstChar)
	elif QuestInfo.Index == 10900:
		firstChar = GetQuestChar(Sender, 10898)
		secondChar = GetQuestChar(Sender, 10899)
		if firstChar is None or secondChar is None or firstChar == secondChar:
			return
		Used.extend([firstChar, secondChar])

	UserQuest.ExtraInfo = GetRandomChar(Used)


PlayerEvent.add_listener("OnCompleteQuest", OnCompleteQuest)
