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
import Server
import NpcEvent
import collections
import PlayerEvent
clr.AddReference('System')
import Server.Envir.SEnvir as SEnvir
from Utils import ServerUtils
import MapEvent
from Utils.TimeUtil import *
import datetime
import os
import Utils.ServerUtils as ServerUtils
from Utils.PlayerUtils import *
clr.ImportExtensions(System.Linq)
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
		today = datetime.datetime.now().weekday() + 1  #判断周几
		pkmap = SEnvir.GetMap(467)      #获取比赛地图
		if (Sender.Level < 48):
			say = """你还不够强大，需要等级48级才能参加活动。
			
			[离开:0]"""
		elif today == 6 and current_time_is_between("22:00:00", "23:59:59") and (PlayerGetV(Sender,GV_PLAYER_ARENAACCESS) == 0):
			say = """你的竞技点为0，无法再参加活动。
			
			[离开:0]"""
		elif today == 6 and current_time_is_between("22:00:00", "23:59:59") and (pkmap.Players.Count <= 5):
			say = """地图内只剩余前5名决一胜负，你无法参加活动。
			
			[离开:0]"""
		#身上有对应的BUFF 无法进入               凝血                                       铁布衫                                    破血                                                                          道盾                                           妙影
		elif(Sender.Buffs.Any(lambda x:x.Type == BuffType.Renounce)) or (Sender.Buffs.Any(lambda x:x.Type == BuffType.Defiance)) or (Sender.Buffs.Any(lambda x:x.Type == BuffType.Might)) or (Sender.Buffs.Any(lambda x:x.Type == BuffType.CelestialLight)) or (Sender.Buffs.Any(lambda x:x.Type == BuffType.Transparency)):
			say = """你身上存在诺玛技能BUFF，无法进入。
			
			[离开:0]"""
		else:
			pkmap = SEnvir.GetMap(467)      #获取比赛地图
			random_point = pkmap.GetRandomLocation()      #取随机数坐标值
			if today == 6 and current_time_is_between("21:50:00", "21:59:59"):   #如果是周六 并且是  晚上21点50分
				Sender.TeleportByMapIndex(466,20,22)          #飞地图ID X坐标 Y坐标
			#活动开始的时间 玩家的进入次数小于5次 活动地图存活的玩家大于5人
			elif today == 6 and current_time_is_between("22:00:00", "23:59:59") and (PlayerGetV(Sender,GV_PLAYER_ARENAACCESS) > 0) and (pkmap.Players.Count > 5):
				Sender.TeleportByMapIndex(467, random_point.X, random_point.Y)          #飞地图ID X坐标 Y坐标
			else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
#主菜单
	else:
		gregorianCalendar = System.Activator.CreateInstance(System.Globalization.GregorianCalendar)
		#获取指定日期是周数 CalendarWeekRule指定 第一周开始于该年的第一天，DayOfWeek指定每周第一天是星期几　
		weekOfYear= gregorianCalendar.GetWeekOfYear(SEnvir.Now, System.Globalization.CalendarWeekRule.FirstDay, System.DayOfWeek.Monday)
		
		if weekOfYear % 4 == 0:
			say = """你好勇士，欢迎参加死亡竞技场活动。
			
			要求：<font color=\"0xff00ff00\">等级达到48以上才能参加</font>
			活动时间：<font color=\"0xff00ff00\">周六晚上22点准时开启</font>
			活动规则：<font color=\"0xff00ff00\">晚上9点50可进入等待室（安全区），10点统一传送</font>
			<font color=\"0xff00ff00\">到竞技场。玩家起始拥有5点竞技点，每击杀1名玩家，增加1点</font>
			<font color=\"0xff00ff00\">竞技点；每被击杀一次，扣减1点竞技点，当竞技点为0，无法</font>
			<font color=\"0xff00ff00\">进入竞技场。场内允许使用药水，不允许使用诺玛技能和随机</font>
			<font color=\"0xff00ff00\">、移行、瞬移，人物统一模型、隐藏血条，不掉落装备，不计</font>
			<font color=\"0xff00ff00\">PK值。每次进入竞技场，有几率直接获得白金盲盒；每次击杀</font>
			<font color=\"0xff00ff00\">玩家，有几率获得白金盲盒。当场内剩下5名玩家，关闭竞技场</font>
			<font color=\"0xff00ff00\">，并按该5名玩家竞技点排名发放排名奖励。最后存活玩家，还</font>
			<font color=\"0xff00ff00\">可领取额外奖励。</font>
			
			[参与死亡竞技活动:1]
			
			[离开:0]"""
		else:
			say = """你好勇士，欢迎参加死亡竞技场活动。
			
			要求：<font color=\"0xff00ff00\">等级达到48以上才能参加</font>
			活动时间：<font color=\"0xff00ff00\">周六晚上22点准时开启</font>
			活动规则：<font color=\"0xff00ff00\">晚上9点50可进入等待室（安全区），10点统一传送</font>
			<font color=\"0xff00ff00\">到竞技场。玩家起始拥有5点竞技点，每击杀1名玩家，增加1点</font>
			<font color=\"0xff00ff00\">竞技点；每被击杀一次，扣减1点竞技点，当竞技点为0，无法</font>
			<font color=\"0xff00ff00\">进入竞技场。场内允许使用药水，不允许使用诺玛技能和随机</font>
			<font color=\"0xff00ff00\">、移行、瞬移，人物统一模型、隐藏血条，不掉落装备，不计</font>
			<font color=\"0xff00ff00\">PK值。每次进入竞技场，有几率直接获得白金盲盒；每次击杀</font>
			<font color=\"0xff00ff00\">玩家，有几率获得白金盲盒。当场内剩下5名玩家，关闭竞技场</font>
			<font color=\"0xff00ff00\">，并按该5名玩家竞技点排名发放排名奖励。最后存活玩家，还</font>
			<font color=\"0xff00ff00\">可领取额外奖励。</font>？
			
			[离开:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(407,"OnClick",OnClick)