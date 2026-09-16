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

	if (Menu == 1):
		dicyihou = GlobalGetObV(GV_PLAYER_PAOCHUANSHAGUAICOUNT)
		
		if dicyihou is None:
			say = """<font color=\"0xff00ff00\">周跑船活动：周日晚上21点开启 - 21点30分关闭进入</font>
			玩家跑到船一的霸王幽灵处，可获得大量经验，万年雪霜，祝福油等奖励，累计次数以后，获得的奖励更丰厚。
			杀怪排名积分前十的玩家，将获得额外奖励。
			
			你当前累计跑船次数{}次。
			
			[跑船奖励:12]
			[参与活动:11]
			
			活动积分排名：（只显示积分排名前十玩家）
			
			暂无积分排名
			
			[关闭:0]""".format(PlayerGetV(Sender,GV_PLAYER_PAOCHUANGXUNHUAN))
		else:
			a1 = sorted(dicyihou.items(),key = lambda x:x[1],reverse = True)
			str1 = ""
			for i in range(len(a1)):
				if i >= 10: 
					break
				str1 = str1 + a1[i][0] +" " +str(a1[i][1]) + "\n"
			
			say = """<font color=\"0xff00ff00\">周跑船活动：周日晚上21点开启 - 21点30分关闭进入</font>
			玩家跑到船一的霸王幽灵处，可获得大量经验，万年雪霜，祝福油等奖励，累计次数以后，获得的奖励更丰厚。
			杀怪排名积分前十的玩家，将获得额外奖励。
			
			你当前累计跑船次数{}次。
			
			[跑船奖励:12]
			[参与活动:11]
			
			活动积分排名：（只显示积分排名前十玩家）
			
			{}
			
			[跑船积分排名奖励领取:13]
			
			[关闭:0]""".format(PlayerGetV(Sender,GV_PLAYER_PAOCHUANGXUNHUAN), str1)
	elif (Menu == 11):
		map = SEnvir.GetMap(554)  # 要传送的地图
		#today = datetime.date.today()  #判断日期
		#if (today.month == 7 and today.day > 9):
		today = datetime.datetime.now().weekday() + 1  #判断周几
		if (today == 7):
			if current_time_is_between("21:00:00", "21:30:00"):
				if(PlayerGetV(Sender,GV_PLAYER_PAOCHUANG) == 99):
					say = """你本周已经参与过一次活动，无法再次进入。
					
					[离开:0]"""
				elif(PlayerGetV(Sender,GV_PLAYER_PAOCHUANG) > 0):
					Sender.TeleportByMapIndex(554,23,81)          #飞地图ID X坐标 Y坐标
					return
				elif(PlayerGetV(Sender,GV_PLAYER_PAOCHUANG)==0):
					PlayerSetV(Sender,GV_PLAYER_YIJIESHENJIAN,1)
					Sender.TeleportByMapIndex(554,23,81)          #飞地图ID X坐标 Y坐标
					return
			else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
		else:
			say = """活动还没开启，请留意活动公告。
			
			[离开:0]"""
	elif (Menu == 12):
		say = """单次奖励：
		每层获得不同经验奖励，首次跑船有几率获得 霹雷（限时）、龙纹剑（限时）、嗜魂法杖（限时）。
		
		累积奖励：
		累积达到4次获得额外经验奖励
		第1次获得：装备刻名卷
		第3次获得：千里传音
		第5次获得：万年雪霜（绑定）100个
		第10次获得：祝福油5个
		第12次获得：钢玉石
		第20次获得：亡灵之药水
		第25次获得：白色口哨
		第30次获得：连环明珠
		第40次获得：诅咒之药水
		第70次获得：魔晶石
		第120次按职业获得：裁决之杖、无极棍、骨玉权杖
		
		[返回:1]"""
	elif (Menu == 13):
		dicyihou = GlobalGetObV(GV_PLAYER_PAOCHUANLINGQU)
		if dicyihou is None:
			say = """活动积分排名：（只显示积分排名前十玩家）
			
			暂无积分排名
			
			[关闭:0]"""
		else:
			#a1 = sorted(dicyihou.items(),key = lambda x:x[1],reverse = True)
			str1 = ""
			i = 0
			for key,value in dicyihou.items():
				i = i + 1
				str1 = str1 + str(i) +"    "+ key 
				if key==Sender.Name:
					if value == 1:
						str1 = str1 + "      [领取:14]\n"
					else:
						str1 = str1 + "      已领取\n"
				else:
					str1 = str1 + "\n"
				
			say = """活动积分排名：（只显示积分排名前十玩家）
			
			{} 
			
			[关闭:0]""".format(str1)
	elif (Menu == 14):
		dicyihou = GlobalGetObV(GV_PLAYER_PAOCHUANLINGQU)
		if dicyihou is None or dicyihou.get(Sender.Name, 0) == 0:
			return
		if (GetInventoryCount(Sender) >= 1):
			dicyihou[Sender.Name] = 0
			GlobalSetObV(GV_PLAYER_PAOCHUANLINGQU,dicyihou)
			Sender.GiveItemsByStat([{'name':'亡灵之药水','bound':True,'count':1,},])
			say = """恭喜你获得跑船杀怪排名奖励。
			
			[离开:0]"""
		else:
			say ="""你的包裹没有空格。
			
			[离开:0]"""
	elif (Menu == 2):
		say = """死亡竞技场于<font color=\"0xff00ff00\">周六晚上22点</font>开放，
		40—48级玩家可进初级竞技场，
		48级以上玩家可进高级竞技场，
		玩家有几率直接获得经验（最大不超过50万），
		击杀玩家可获得盲盒奖励，最后胜利玩家奖励多多。
		
		[关闭:0]"""
	elif (Menu == 3):
		say = """沙巴克地下城于<font color=\"0xff00ff00\">周六晚上22点</font>开放，
		地图内有大量宝盒、大爆怪，
		其中，第一、二层五倍经验，无需门票，
		第三层刷新大量boss，非沙巴克行会玩家需花费20万金币。
		
		[关闭:0]"""
	elif (Menu == 4):
		say = """行会副本<font color=\"0xff00ff00\">周六晚上22点</font>开启，
		从<font color=\"0xff00ff00\">诺玛村庄左下角坐标（83,343）进入</font>，
		所有行会的45级以上玩家都可以参与活动第一阶段，
		第二和第三阶段要求行会等级3级的成员参与，
		各阶段产出较为丰厚，
		最后赢得副本的行会，
		可获得一周限时BUFF（3%经验、3%金币加成）
		
		[关闭:0]"""
	elif (Menu == 5):
		say = """活动时间：<font color=\"0xff00ff00\">7月10日 - 16日，每天早上8点 - 晚上12点</font>
		材料要求：<font color=\"0xff00ff00\">1个面粉、1个鸡蛋</font>
		制作加成：<font color=\"0xff00ff00\">每次提交材料随机获得1-10点进度，每天只能提交一次</font>
		奖励：<font color=\"0xff00ff00\">每次参与蛋糕制作，获得20万经验、3瓶职业神水、3瓶祝福油，并有机会获取红包。</font>
		
		蛋糕制作进度: <font color=\"0xff00ff00\">{} / 1500</font>
		
		你确定要制作庆典蛋糕吗？
		
		[提交材料:51]
		[购买材料:52] （面粉加鸡蛋，需要花费20万金币）
		
		[离开:0]""".format(GlobalGetV(GV_BOSS_QINGDIANDANGAO))
	elif (Menu == 51):
		Points=[(449, 391),(465,372),(422,368),(462,402),(438,392)]
		today = datetime.date.today()  #判断日期
		if (today.month == 7 and today.day > 9 and today.day < 16):
			if current_time_is_between("8:00:00", "23:59:59"):
				if (GlobalGetV(GV_BOSS_DANGAOSHUAXIN) != 0):
					say = """今天的庆典蛋糕已经集满，等明天再来吧。
					
					[离开]"""
				elif(PlayerGetV(Sender,GV_PLAYER_DANGAOCOUNT) > 0):
					say = """今天已经提交过一次材料了，等明天再来吧。
					
					[离开]"""
				elif(Sender.GetItemCount("面粉") < 1):
					say ="""你的材料不足，请准备好足够的材料在来。
					
					[离开:0]"""
				elif(Sender.GetItemCount("鸡蛋") < 1):
					say ="""你的材料不足，请准备好足够的材料在来。
					
					[离开:0]"""
				else:
					if GlobalGetV(GV_BOSS_QINGDIANDANGAO) >= 1500 and GlobalGetV(GV_BOSS_DANGAOSHUAXIN) == 0:
						GlobalSetV(GV_BOSS_DANGAOSHUAXIN, 1)
						GlobalSetV(GV_BOSS_QINGDIANDANGAO, 0)
						point = random.sample(Points,1)
						ServerUtils.SpawnMonsters(1, "庆典蛋糕", 1, point[0][0], point[0][1], 1)  #刷怪 地图名 怪物名 数量 X Y 范围
						#系统发出公告提示
						BroadChat("庆典蛋糕出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("庆典蛋糕出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("庆典蛋糕出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("庆典蛋糕出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						BroadChat("庆典蛋糕出现在玛法大陆 比奇城安全区随机范围内，请玛法大陆的勇士们一同前往狂欢。", MessageType.System)
						SEnvir.Log("脚本记录：庆典蛋糕已经刷新")
						SEnvir.Log("脚本记录：庆典蛋糕已经刷新")
						SEnvir.Log("脚本记录：庆典蛋糕已经刷新")
						return
					else:
						if (GetInventoryCount(Sender) > 3):
							Sender.TakeItem("面粉",1)
							Sender.TakeItem("鸡蛋",1)
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
								Sender.GiveItem("8元红包",1)
							BroadChat(' {} 加入了庆典蛋糕制作队伍，获得额外奖励。'.format(Sender.Name))
							select2 = random.randint(1,10)
							PlayerSetV(Sender,GV_PLAYER_DANGAOCOUNT,1)
							GlobalSetV(GV_BOSS_QINGDIANDANGAO,GlobalGetV(GV_BOSS_QINGDIANDANGAO)+select2)
							say ="""材料提交成功，随机增加庆典蛋糕进度 {} 点。
							
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
	elif (Menu == 52):
		if (Sender.Gold < 200000):
			say = """你金币不足，无法购买材料。

			[离开:0]"""
		elif (GetInventoryCount(Sender) < 2):
			say = """你的背包没有空间，整理下再来购买。
			
			[离开:0]"""
		else:
			SubGold(Sender,200000)
			Sender.GiveItem("面粉",1)
			Sender.GiveItem("鸡蛋",1)
			say = """购买成功，快去提交材料制作蛋糕吧。
			
			[离开:0]"""
	elif (Menu == 6):
		say = """活动时间：<font color=\"0xff00ff00\">7月10号0点-7月16号0点</font>
		活动内容：<font color=\"0xff00ff00\">全区服忠诚度获得收益翻倍。</font>
		
		[离开:0]"""
	elif (Menu == 7):
		dicyihou = GlobalGetObV(GV_PLAYER_YIHOU)
		
		if dicyihou is None:
			say = """活动时间：<font color=\"0xff00ff00\">7月10号0点-7月16号0点</font>
			活动内容：<font color=\"0xff00ff00\">蚁后与驽马王累计击杀数量排名奖励</font>
			活动规则：<font color=\"0xff00ff00\">只有新号参与活动，同IP或同网段有超48级角色无法参与</font>
			奖励：<font color=\"0xff00ff00\">截至7月16号0点击杀数量前三玩家，分别获得奖励888元、688元、588元</font>
			
			活动排名：（只显示前三名击杀总数玩家）
			
			暂无击杀
		
			[离开:0]"""
		else:
			a1 = sorted(dicyihou.items(),key = lambda x:x[1],reverse = True)
			str1 = ""
			for i in range(len(a1)):
				if i >= 3: 
					break
				str1 = str1 + a1[i][0] +" " +str(a1[i][1]) + "\n"
			
			say = """活动时间：<font color=\"0xff00ff00\">7月10号0点-7月16号0点</font>
			活动内容：<font color=\"0xff00ff00\">蚁后与驽马王累计击杀数量排名奖励</font>
			活动规则：<font color=\"0xff00ff00\">只有新号参与活动，同IP或同网段有超48级角色无法参与</font>
			
			活动排名：（只显示前三名击杀总数玩家）
			
			{}
		
			[离开:0]""".format(str1)
	elif (Menu == 8):
		dicyihou = GlobalGetObV(GV_PLAYER_JIFENGCOUNT)
		
		if dicyihou is None:
			say = """活动时间：<font color=\"0xff00ff00\">7月14号20点</font>
			活动内容：<font color=\"0xff00ff00\">怪物从沙巴克城墙四角往沙巴克旗台方向行进。</font>
			<font color=\"0xff00ff00\">如果真BOSS到达旗台消失，全服务器物价提高10%一周。</font>
			<font color=\"0xff00ff00\">如果真BOSS被击杀，全服务器经验加成10%一周。</font>
			奖励：积分前10，奖励188；相聚之刃（法）、相聚之刃（战）、相聚之刃（道）、相聚战甲，限时一个月，回收价888
			
			活动积分排名：（只显示积分排名前十玩家）
			
			暂无积分排名
			
			[离开:0]"""
		else:
			a1 = sorted(dicyihou.items(),key = lambda x:x[1],reverse = True)
			str1 = ""
			for i in range(len(a1)):
				if i >= 10: 
					break
				str1 = str1 + a1[i][0] +" " +str(a1[i][1]) + "\n"
			
			say = """活动时间：<font color=\"0xff00ff00\">7月14号20点</font>
			活动内容：<font color=\"0xff00ff00\">怪物从沙巴克城墙四角往沙巴克旗台方向行进。</font>
			<font color=\"0xff00ff00\">如果真BOSS到达旗台消失，全服务器物价提高10%一周。</font>
			<font color=\"0xff00ff00\">如果真BOSS被击杀，全服务器经验加成10%一周。</font>
			
			活动积分排名：（只显示积分排名前十玩家）
			
			{}
			
			[离开:0]""".format(str1)
	elif (Menu == 9):
		today = datetime.datetime.now().weekday() + 1  #判断周几
		if (today == 6):
			if current_time_is_between("22:00:00", "22:14:59"):
				if(PlayerGetV(Sender,GV_PLAYER_LIUYIPAOKUARMOUR) == 0):
					if (GetInventoryCount(Sender) >= 1):
						if (Sender.Gender == MirGender.Male):
							Sender.GiveItem("滑板（男）",1)
						else:
							Sender.GiveItem("滑板（女）",1)
						PlayerSetV(Sender,GV_PLAYER_LIUYIPAOKUARMOUR,1)
						Sender.TeleportByMapIndex(562,36,36)          #飞地图ID X坐标 Y坐标
						say = """<font color=\"0xffff0000\">注意：必须穿戴滑板时装，才可以参与活动，切记别脱掉时装。</font>
						
						[关闭:0]"""
					else:
						say ="""你的包裹没有空格，无法获得时装，
						请整理好包裹在参与活动。
						
						[离开:0]"""
				else:
					Sender.TeleportByMapIndex(562,36,36)          #飞地图ID X坐标 Y坐标
					say = """<font color=\"0xffff0000\">注意：必须穿戴滑板时装，才可以参与活动，切记别脱掉时装。</font>
					
					[关闭:0]"""
			else:
				say = """活动还没开启，请留意活动公告。
				
				[离开:0]"""
		else:
			say = """活动还没开启，请留意活动公告。
			
			[离开:0]"""

#主菜单
	else:
		gregorianCalendar = System.Activator.CreateInstance(System.Globalization.GregorianCalendar)
		#获取指定日期是周数 CalendarWeekRule指定 第一周开始于该年的第一天，DayOfWeek指定每周第一天是星期几　
		weekOfYear= gregorianCalendar.GetWeekOfYear(SEnvir.Now, System.Globalization.CalendarWeekRule.FirstDay, System.DayOfWeek.Monday)
		
		if weekOfYear % 4 == 0:
			say = """这里平时会提供一些节日活动，你可以来看看。
			
			[周六『死亡竞技场活动』:2]
			[周日『周跑船活动』:1]"""
		elif weekOfYear % 4 == 1:
			say = """这里平时会提供一些节日活动，你可以来看看。
			
			[周六『沙巴克地下城活动』:3]
			[周日『周跑船活动』:1]"""
		elif weekOfYear % 4 == 2:
			say = """这里平时会提供一些节日活动，你可以来看看。
			
			[周六『行会夺宝活动』:4]
			[周日『周跑船活动』:1]"""
		elif weekOfYear % 4 == 3:
			say = """这里平时会提供一些节日活动，你可以来看看。
			
			[周六『酷跑活动』:9]
			[周日『周跑船活动』:1]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(311,"OnClick",OnClick)