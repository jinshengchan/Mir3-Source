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
rewardshanghui = [
				('半兽勇士召唤卷', 1, True, 3000),
				('骷髅精灵召唤卷', 1, True, 3000),
				('尸王召唤卷', 1, True, 3000),
				('红甲虫召唤卷', 1, True, 3000),
				('巨型多角虫召唤卷', 1, True, 3000),
				('蚂蚁将军召唤卷', 1, True, 2000),
				('白野猪召唤卷', 1, True, 2000),
				('沃玛卫士召唤卷', 1, True, 2000),
				('邪恶钳虫召唤卷', 1, True, 2000),
				('八角首领召唤卷', 1, True, 2000),
				('骨鬼将召唤卷', 1, True, 1000),
				('大法老召唤卷', 1, True, 1000),
				('疯狂魔神盗召唤卷', 1, True, 1000),
				('护法天召唤卷', 1, True, 1000),
				('神鬼王召唤卷', 1, True, 1000),
				('潘夜鬼将召唤卷', 1, True, 500),
				('震天首将召唤卷', 1, True, 500),
				]

def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if (Menu == 1):
		Sender.TeleportByMapIndex(1,469,378)          #飞地图ID X坐标 Y坐标
		return
#主菜单
	else:
		say = """你好勇士，欢迎参加酷跑活动。
		
		酷跑活动时间：<font color=\"0xff00ff00\">酷跑活动周六晚上22点准时开启</font>
		酷跑规则：<font color=\"0xff00ff00\">22点15分准时传送等待室内玩家到酷跑活动地图。场内安全区，禁用随机、移行、瞬移。</font>
		
		跑到终点的前50名将获得额外奖励。
		路上发现的宝箱击杀获得泡泡糖。
		泡泡糖只允许在终点相聚教室里使用，按泡泡的大小获得对应的奖励，离开相聚教室泡泡糖将被系统收回。
		<font color=\"0xffff0000\">注意：必须穿戴滑板时装，才可以参与活动，切记别脱掉时装。</font>
		
		[我要离开:1]
		
		[等待活动开启:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick1(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	Sender.TeleportByMapIndex(564,23,50)          #飞地图ID X坐标 Y坐标
	return

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def OnClick2(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if (Menu == 1):
		if PlayerGetV(Sender,GV_PLAYER_LIUYIPAOKU) == 9999:
			say = """你已经领取过奖励，无法重复领取。
			
			[离开:0]"""
		elif GlobalGetV(GV_PLAYER_LIUYIPAOKUCOUNT) < 50:  #第一名奖励
			GlobalSetV(GV_PLAYER_LIUYIPAOKUCOUNT,GlobalGetV(GV_PLAYER_LIUYIPAOKUCOUNT)+1)
			PlayerSetV(Sender,GV_PLAYER_LIUYIPAOKU,9999)
			# 最终奖励
			converted_reward = []
			for item in rewardshanghui:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("酷跑活动", "运营团队", "你获得随机奖励", my_reward)
			Sender.PYMailSend("酷跑活动", "运营团队", "邮件发送活动额外奖励", [('金质盲盒',1,True),('万年雪霜（绑定）',100,True),('祝福油（绑定）',5,True)])
			BroadChat('恭喜玩家 {} 完成酷跑活动，获得 {} ，金质盲盒，各一个。前五十名额外奖励万年雪霜100个，祝福油5瓶。'.format(Sender.Name, my_reward[0][0]))
			say = """恭喜你完成酷跑活动，前五十名，请查收你的奖励。
			
			[离开:0]"""
		else: 
			PlayerSetV(Sender,GV_PLAYER_LIUYIPAOKU,9999)
			# 最终奖励
			converted_reward = []
			for item in rewardshanghui:
				converted_item = (item[0], item[1], item[2])
				for i in range(item[3]):
					converted_reward.append(converted_item)
			# 抽取1个
			my_reward = random.sample(converted_reward, 1)
			# 发奖
			Sender.PYMailSend("酷跑活动", "运营团队", "你获得随机奖励", my_reward)
			Sender.PYMailSend("酷跑活动", "运营团队", "邮件发送活动额外奖励", [('金质盲盒',1,True)])
			BroadChat('恭喜玩家 {} 完成酷跑活动，获得 {} ，金质盲盒，各一个。'.format(Sender.Name, my_reward[0][0]))
			say = """恭喜你完成酷跑活动，请查收你的奖励。
			
			[离开:0]"""
	elif (Menu == 2):
		Sender.TeleportByMapIndex(1,469,378)   #把玩家传送回比奇
		return
	else:
		say = """[领取酷跑活动奖励:1]
		
		[离开活动地图:2]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(364,"OnClick",OnClick)
NpcEvent.add_listener(366,"OnClick",OnClick1)
NpcEvent.add_listener(365,"OnClick",OnClick2)

