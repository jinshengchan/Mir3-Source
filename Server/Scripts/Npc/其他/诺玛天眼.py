# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
import System
s1 = clr.Reference[System.Object]()
from Defines import *
import Server
import PlayerEvent
clr.AddReference('System')
import Server.Envir.SEnvir as SEnvir
from Utils import ServerUtils
import MapEvent
from Utils.TimeUtil import *
import datetime
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
	say = ""
	
	if (Menu == 1):
		say = """<font color=\"0xffffff00\">进入条件：</font>
		新手行会<font color=\"0xff00ff00\">等级45级成员</font>或者<font color=\"0xff00ff00\">3级行会等级45级成员</font>。
		
		<font color=\"0xffffff00\">活动规则：</font>
		新手行会成员只能参与<font color=\"0xff00ff00\">第一阶段清理小怪活动</font>，小怪清理结束将自动被传送出地图，无法在进入。
		第二阶段BOSS击杀和第三阶段宝箱争夺<font color=\"0xff00ff00\">3级行会成员</font>才能参与。
		
		<font color=\"0xffffff00\">活动消耗：</font>
		每次进入地图，新手行会成员消耗<font color=\"0xff00ff00\">2万金币</font>，3级行会成员消耗
		<font color=\"0xff00ff00\">行会资金2万金币</font>，死亡可以复活，小退就退出活动地图，需重新消耗金币才能进入。
		
		[参与活动:11]
		
		[离开:0]"""
	elif (Menu == 11):
		map = SEnvir.GetMap(561)  # 要传送的地图
		if map is None:
			say = """活动地图尚未加载，请稍后再试。
			
			[离开:0]"""
			Dict['Say']=say
			return Dict
		randomLocation = map.GetRandomLocation()      #取随机数坐标值
		if Sender.Character.Account.GuildMember is None:
			say = """你没有行会，无法参与活动。
			
			[离开:0]"""
			
			Dict['Say']=say                         #定义聊天框对话内容
			return Dict
		today = datetime.datetime.now().weekday() + 1  #判断周几
		if (Sender.Level < 45):
			say = """你还不够强大，需要等级45级才能参与活动。
			
			[离开:0]"""
		# elif (Sender.Character.Account.GuildMember.Guild.GuildLevel != 0) and (Sender.Character.Account.GuildMember.Guild.GuildLevel < 5):
			# say = """你不是新手行会成员或者不是5级行会成员，无法参与活动。
			
			# [离开:0]"""
		elif (PlayerGetV(Sender,GV_PLAYER_NUOMATIANLAOYI)> 0):  #(Sender.Character.Account.GuildMember.Guild.GuildLevel == 0) and 
			say = """第一阶段活动已经结束，无法参与活动。
			
			[离开:0]"""
		else:
			if today == 6 and current_time_is_between("22:00:00", "22:59:59"):   #如果是周六 并且是  晚上10点开始
				#判断 新手行会 无行会 的 花自己金币进
				if (Sender.Character.Account.GuildMember.Guild.GuildLevel == 0):
					if (Sender.Gold < 20000):
						say = """你没有足够的金币，无法参与活动。
							
							[离开:0]"""
					else:
						SubGold(Sender,20000)
						Sender.TeleportByMapIndex(561,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
				else:
					#行会资金不足的就没办法进入
					if (Sender.Character.Account.GuildMember.Guild.GuildFunds < 20000):
						say = """你的行会没有足够的行会资金，无法参与活动。
							
							[离开:0]"""
					else:
						#有行会的直接扣行会资金进
						Sender.Character.Account.GuildMember.Guild.GuildFunds -= 20000
						update = Sender.Character.Account.GuildMember.Guild.GetUpdatePacket()
						for member in Sender.Character.Account.GuildMember.Guild.Members:
							if member.Account.Connection is not None and member.Account.Connection.Player is not None:
								member.Account.Connection.Player.Enqueue(update)
						Sender.TeleportByMapIndex(561,randomLocation.X,randomLocation.Y)          #飞地图ID X坐标 Y坐标
			else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
	else:
		say = """[诺玛天牢:1]
		
		[离开:0]"""


	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(355,"OnClick",OnClick)
