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
import Server.Envir.SEnvir as SEnvir
import collections
clr.AddReference("System.Core")
clr.AddReference('System')
clr.ImportExtensions(System.Linq)
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
import unicodedata
import PlayerEvent
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
	say =''
	
	if (Menu == 1):
		say = """活动时间：<font color=\"0xff00ff00\">12月30日 - 1月1日，每天早上8点 - 晚上12点</font>
		等级要求：<font color=\"0xff00ff00\">33级以上</font>
		材料要求：<font color=\"0xff00ff00\">1个小雪球</font>
		制作加成：<font color=\"0xff00ff00\">提交材料随机获得1-10点进度，每天提交一次</font>
		奖励：<font color=\"0xff00ff00\">每次参与雪人制作，获得20万经验、3瓶职业神水、3瓶祝福油，并有机会获取赞助币。</font>
		
		雪人制作进度: <font color=\"0xff00ff00\">{} / 1500</font>
		
		你确定要制作雪人吗？
		
		[提交材料:11]
		[购买材料:12] （需要花费20万金币）
		
		[离开:0]""".format(GlobalGetV(GV_BOSS_QINGDIANDANGAO))
	elif (Menu == 11):
		Points=[(449, 391),(465,372),(422,368),(462,402),(438,392)]
		today = datetime.date.today()  #判断日期
		if ((today.month == 12 and today.day > 29) or (today.month == 1 and today.day < 2)):
			if current_time_is_between("8:00:00", "23:59:59"):
				if (Sender.Level < 33):
					say = """你的等级不够，无法参与活动。
					
					[离开]"""
				elif (GlobalGetV(GV_BOSS_DANGAOSHUAXIN) == 3):
					say = """今天的雪人已经集满，等明天再来吧。
					
					[离开]"""
				elif(PlayerGetV(Sender,GV_PLAYER_DANGAOCOUNT) > 0):
					say = """今天已经提交过一次材料了，等明天再来吧。
					
					[离开]"""
				elif(Sender.GetItemCount("小雪球") < 1):
					say ="""你的材料不足，请准备好足够的材料在来。
					
					[离开:0]"""
				else:
					if GlobalGetV(GV_BOSS_QINGDIANDANGAO) >= 500 and GlobalGetV(GV_BOSS_DANGAOSHUAXIN) == 0:
						GlobalSetV(GV_BOSS_DANGAOSHUAXIN, 1)
						point = random.sample(Points,1)
						ServerUtils.SpawnMonsters(1, 100469, 1, point[0][0], point[0][1], 1)  #刷怪 地图名 怪物名 数量 X Y 范围
						#系统发出公告提示
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						SEnvir.Log("脚本记录：雪人小已经刷新")
						SEnvir.Log("脚本记录：雪人小已经刷新")
						SEnvir.Log("脚本记录：雪人小已经刷新")
						return
					elif GlobalGetV(GV_BOSS_QINGDIANDANGAO) >= 1000 and GlobalGetV(GV_BOSS_DANGAOSHUAXIN) == 1:
						GlobalSetV(GV_BOSS_DANGAOSHUAXIN, 2)
						point = random.sample(Points,1)
						ServerUtils.SpawnMonsters(1, 100470, 1, point[0][0], point[0][1], 1)  #刷怪 地图名 怪物名 数量 X Y 范围
						#系统发出公告提示
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						SEnvir.Log("脚本记录：雪人中已经刷新")
						SEnvir.Log("脚本记录：雪人中已经刷新")
						SEnvir.Log("脚本记录：雪人中已经刷新")
						return
					elif GlobalGetV(GV_BOSS_QINGDIANDANGAO) >= 1500 and GlobalGetV(GV_BOSS_DANGAOSHUAXIN) == 2:
						GlobalSetV(GV_BOSS_DANGAOSHUAXIN, 3)
						GlobalSetV(GV_BOSS_QINGDIANDANGAO, 0)
						point = random.sample(Points,1)
						ServerUtils.SpawnMonsters(1, 100471, 1, point[0][0], point[0][1], 1)  #刷怪 地图名 怪物名 数量 X Y 范围
						#系统发出公告提示
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("雪人出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						SEnvir.Log("脚本记录：雪人大已经刷新")
						SEnvir.Log("脚本记录：雪人大已经刷新")
						SEnvir.Log("脚本记录：雪人大已经刷新")
						return
					else:
						if (GetInventoryCount(Sender) > 3):
							Sender.TakeItem("小雪球",1)
							GiveExperience(Sender,200000)
							Sender.GiveItem("祝福油（绑定）",3)
							if Sender.Class == Sender.Class.Warrior: #战士
								Sender.GiveItemsByStat([{'name':'攻击神水（大）','bound':True,'count':3,},])
							elif Sender.Class == Sender.Class.Taoist: #道士
								Sender.GiveItemsByStat([{'name':'灵魂神水（大）','bound':True,'count':3,},])
							else:
								Sender.GiveItemsByStat([{'name':'自然神水（大）','bound':True,'count':3,},])
							select = random.randint(0,100)
							if select < 20:
								Sender.GiveItem("5赞助币",1)
								BroadChat('{} 加入了雪人制作队伍，获得额外奖励。'.format(Sender.Name))
							select2 = random.randint(1,10)
							PlayerSetV(Sender,GV_PLAYER_DANGAOCOUNT,1)
							GlobalSetV(GV_BOSS_QINGDIANDANGAO,GlobalGetV(GV_BOSS_QINGDIANDANGAO)+select2)
							say ="""材料提交成功，随机增加雪人进度 {} 点。
							
							[离开:0]""".format(select2)
						else:
							say = """背包空间不足，请整理下再来。
							
							[离开:0]"""
			else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
		else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
	elif (Menu == 12):
		if (Sender.Level < 33):
			say = """你的等级不够，无法参与活动。
			
			[离开]"""
		elif (Sender.Gold < 200000):
			say = """你金币不足，无法购买材料。

			[离开:0]"""
		elif (GetInventoryCount(Sender) < 1):
			say = """你的背包没有空间，整理下再来购买。
			
			[离开:0]"""
		else:
			SubGold(Sender,200000)
			Sender.GiveItem("小雪球",1)
			say = """购买成功，快去提交材料制作雪人吧。
			
			[离开:0]"""
	elif (Menu == 2):
		say = """活动时间：<font color=\"0xff00ff00\">12月30日 - 1月1日，每晚7点起</font>
		活动地点：<font color=\"0xff00ff00\">比奇皇宫</font>
		活动内容：<font color=\"0xff00ff00\">每天晚上7点，比奇城主将在比奇皇宫举办一场新年</font>
		<font color=\"0xff00ff00\">舞会，时间二十分钟。玩家在观看过程中，有几率得到城主送</font>
		<font color=\"0xff00ff00\">出的限时1个月的新年时装。</font>
		
		[参与活动:21]
		
		[离开:0]"""
	elif (Menu == 21):
		today = datetime.date.today()  #判断日期
		if ((today.month == 12 and today.day > 29) or (today.month == 1 and today.day < 2)):
			if current_time_is_between("18:50:00", "19:29:59"):
				Sender.TeleportByMapIndex(2,26,48)
				return
			else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
		else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
	elif (Menu == 3):
		say = """活动时间：<font color=\"0xff00ff00\">12月30日 - 1月1日，每晚10点起</font>
		活动地点：<font color=\"0xff00ff00\">沙巴克城</font>
		活动内容：<font color=\"0xff00ff00\">晚上10点，玛法大陆最强BOSS诺玛统领，将召唤所</font>
		<font color=\"0xff00ff00\">有大小BOSS出现在沙巴克，企图争夺人类圣地。</font>
		
		[参与活动:31]
		
		[离开:0]"""
	elif (Menu == 31):
		today = datetime.date.today()  #判断日期
		if ((today.month == 12 and today.day > 29) or (today.month == 1 and today.day < 2)):
			if current_time_is_between("22:00:00", "23:59:59"):
				Sender.TeleportByMapIndex(25,222,157)
				return
			else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
		else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
#主菜单
	else:
		say = """[堆雪人:1]
		
		[新年舞会:2]
		
		[BOSS大巡游:3]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(349,"OnClick",OnClick)