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


#注意 被闪避的攻击不会触发此函数
def OnPlayerAttack(args):
	Sender=args[0]
	MagicName=args[1]
	Target=args[2]
	TargetName=""
	if hasattr(Target, 'MonsterInfo'):
		TargetName = Target.MonsterInfo.MonsterName
	else:
		TargetName = Target.Name

	Damage=args[3]
	Sender.Connection.ReceiveChat("你使用{}攻击了{}, 造成了{}点伤害".format(MagicName, TargetName, Damage),MessageType.System)

#PlayerEvent.add_listener("OnPlayerAttack",OnPlayerAttack)
