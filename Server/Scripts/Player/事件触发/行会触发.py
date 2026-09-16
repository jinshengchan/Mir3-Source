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

# 此变量设为这个自定义buff的序号
PLAYER_HANGHUIBUFF_INDEX = 113

def OnAcceptGuild(args):
	GuileLeaderSender=args[0]#行会老大
	playerInfo = args[1]#申请者
	# if playerInfo.Account.Connection is not None and playerInfo.Account.Connection.Player is not None:
		# Sender=playerInfo.Account.Connection.Player
		# if Sender is not None:#玩家在线
			# Sender.Connection.ReceiveChat("你入会申请已通过", MessageType.System)
		
def OnKickGuild(args):
	GuileLeaderSender=args[0]#行会老大
	playerInfo = args[1]#申请者
	
	if playerInfo.Account.Connection is not None and playerInfo.Account.Connection.Player is not None:
		Sender = playerInfo.Account.Connection.Player
		if Sender is not None:#玩家在线
			if (Sender.HasCustomBuff(PLAYER_HANGHUIBUFF_INDEX)):
				Sender.CustomBuffRemove(PLAYER_HANGHUIBUFF_INDEX)  #移除行会BUFF状态
				#Sender.Connection.ReceiveChat("你被踢出行会", MessageType.System)

def OnJoinGuild(args):
	Sender = args[0]#玩家接受了行会邀请
	
	#Sender.Connection.ReceiveChat("你已经成功加入了{}行会".format(Sender.Character.Account.GuildMember.Guild.GuildName), MessageType.System)
	
def OnLeaveGuild(args):
	Sender = args[0]#玩家接受了行会邀请
	
	if (Sender.HasCustomBuff(PLAYER_HANGHUIBUFF_INDEX)):
		Sender.CustomBuffRemove(PLAYER_HANGHUIBUFF_INDEX)  #移除行会BUFF状态
	#Sender.Connection.ReceiveChat("你已经成功离开了{}行会".format(Sender.Character.Account.GuildMember.Guild.GuildName), MessageType.System)


PlayerEvent.add_listener("OnAcceptGuild",OnAcceptGuild)###监听老大接受新会员入会邀请
PlayerEvent.add_listener("OnJoinGuild",OnJoinGuild)###监听玩家接受行会老大邀请 触发时玩家已经成功加入行会 可以在玩家里找到行会信息

PlayerEvent.add_listener("OnKickGuild",OnKickGuild)###监听老大踢掉会员
PlayerEvent.add_listener("OnLeaveGuild",OnLeaveGuild)###监听玩家离开行会 触发时玩家还未成功离开行会 可以在玩家里找到行会信息
