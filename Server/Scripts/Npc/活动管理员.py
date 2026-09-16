# -*- coding: utf-8 -*-
#载入模块SYS
import sys
from datetime import datetime, timedelta
#引用模块的地址
from Globals import *
import clr
import System
s1 = clr.Reference[System.Object]()
clr.AddReference("Library")
from Library import *
import NpcEvent
from Defines import *
import Server
import NpcEvent
from Utils.TimeUtil import *
BadaShadow = __import__('Npc.BOSS副本.八大暗影', fromlist=['OnClick'])
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
	if Menu in (80, 81, 82):
		shadowMenu = 1 if Menu == 80 else (11 if Menu == 81 else 12)
		return BadaShadow.OnClick((Self, Sender, shadowMenu))
#跳转菜单1
	if (Menu == 1):
		say = """<font color=\"0xff00ff00\">副本内会爆各种装备武器宠物升级材料</font>
		
		
		[离开:0]"""
		if current_time_is_between("17:59:00", "23:00:00"):                #定义时间变量
			if(Sender.GetItemCount("魔晶石") > 1):           #判断队长材料
				if(PlayerGetV(Sender,GV_ZDBOSSFB_COUNT) == 0):    #定义个人全局变量 数值代表进入次数
					if(Sender.GroupMembers):                    #队伍判断
						if(Sender == Sender.GroupMembers[0]):   #队长判断
							bOpen = True
							if len(Sender.GroupMembers) < 4:    #判断队伍人数
								bOpen = False
								say = """队员数不足5人,无法进入.
								
								[离开:0]"""
							else:
								for player in Sender.GroupMembers:                 #遍历所有队员
									if(PlayerGetV(player,GV_ZDBOSSFB_COUNT) == 1):  #队员变量判断  数值判断是否进入次数
										bOpen = False
										say = """队伍中有队员已经去过副本了
										无法进入
										
										[离开:0]"""
										break
									if player.Level < 50 :                      #队员等级判断
										bOpen = False
										say = """队伍中有队员等级不够50级，去了躺板板
										无法进入
										
										[离开:0]"""
										break
									if (player.GameGold < 100):                   #队员金币判断
										bOpen = False
										say = """队伍中有队员元宝不足，需要100元宝的门票！
										无法进入
										
										[离开:0]"""
										break
									if(player.GetItemCount("魔晶石") < 2):  #队员材料判断
										bOpen = False
										say = """队伍中有队员“魔晶石”都不带一颗，想混水摸鱼哦~
										无法进入
										
										[离开:0]"""
										break
							if bOpen:    #如果可以开启
								map = Server.Envir.SEnvir.CreateMap(1530)               #开启副本地图  （地图ID）
								map.MapTime = datetime.now()+timedelta(minutes=120)    #副本地图关卡时间设置（分钟）
								map.CreateMon(48,44,2,'沃玛教主【副本】',1)
								map.CreateMon(48,56,100,'石岩射手',40)
								map.CreateMon(106,43,100,'石岩射手',40)
								map.CreateMon(148,51,100,'石岩射手',30)
								map.CreateMon(65,113,100,'石岩射手',30)
								map.CreateMon(118,83,100,'石岩射手',30)
								map.CreateMon(237,58,100,'石岩射手',30)
								map.CreateMon(227,96,100,'反手一刀',30)
								map.CreateMon(184,53,100,'反手一刀',30)
								map.CreateMon(188,104,100,'反手一刀',30)
								map.CreateMon(212,155,100,'反手一刀',30)
								map.CreateMon(137,55,100,'反手一刀',30)
								map.CreateMon(162,176,100,'蓝色背刺',40)
								map.CreateMon(207,145,100,'蓝色背刺',40)
								map.CreateMon(231,188,100,'蓝色背刺',40)
								map.CreateMon(179,232,100,'蓝色背刺',40)
								map.CreateMon(228,234,100,'蓝色背刺',40)
								PlayerSetV(Sender,GV_ZDBOSSFB_COUNT,1)
								PlayerSetV(Sender,GV_KILLMON_WMGWCOUNT,0)
								PlayerSetV(Sender,GV_KILLMON_WMGWJSCOUNT,0)
								PlayerSetV(Sender,GV_KILLMON_WMWSJSCOUNT,0)
								PlayerSetV(Sender,GV_KILLMON_ZMGWCOUNT,0)
								for player in Sender.GroupMembers:                     #遍历所有队员
									PlayerSetV(player,GV_ZDBOSSFB_COUNT,1)             #赋值变量为1，代表进入
									SubGameGold(player,100)                              #扣除金币
									player.TakeItem("魔晶石",2)                    #扣除材料
									player.Teleport(map,90,121)                        #把全组人传送进副本
						else:
							say = """不是队长
							
							[离开:0]"""
					else:
						say = """没有队伍
						
						[离开:0]"""
				else:
					say = """你今天已经不能再进入了。。。。。。
					
					[离开:0]"""
			else:
				say = """队长身上至少两颗“魔晶石”，无法进入
				
				[离开:0]"""
		else:
			say = """不在活动时间内（星期一至星期五20点至22点哦）
			
			[返回:99]"""
	elif (Menu == 2):       
		if (PlayerGetV(Sender,GV_BOSSFB_COUNT)<1):   #定义个人全局变量
			PlayerSetV(Sender,GV_BOSSFB_COUNT,PlayerGetV(Sender,GV_BOSSFB_COUNT)+1)     #赋值个人全局变量为1，代表进入过
			if(Sender.GameGold > 199):                #判断需要的物品数量
				SubGameGold(Sender,200)                  #扣除物品
				if (Sender.GroupMembers):   
					Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
				map = Server.Envir.SEnvir.CreateMap(1505)                     #开启副本地图  （地图ID）
				map.CreateMon(104,27,1,'超级沃玛教主',1)
				map.MapTime = datetime.now()+ timedelta(minutes=20);  #副本地图关卡时间设置
				Sender.Teleport(map,31,107)	#飞地图ID X坐标 Y坐标   
				return Dict   #不执行提示框
			else:
				say = "元宝不足，无法进入副本。。。。。"
		else:
			say = """每天只有2次探宝机会，你今天已经用完了

			[离开:0]"""
			
		Dict['Say']=say
		return Dict

	elif (Menu == 6):
		if Sender.Level < 46 : # 等级判断
			say  = """你的实力不够，请你离开。
			你需要46级才能进入
			
			[离开:99]"""             
		elif Sender.Level > 55 : # 等级判断
			say  = """你的实力已经不允许在这里玩了。
			你的实力已经足够了。
			
			[离开:99]"""    
                       
		elif (Sender.GameGold < 300):
			say = """你没有足够的元宝，无法传送。
			[离开:99]"""
		else:       
			map = Server.Envir.SEnvir.CreateMap(1529)                         #开启副本地图（地图ID）
			map.MapTime = datetime.now()+ timedelta(minutes=60);  #副本地图关卡时间设置
			Sender.Teleport(map,32,168)	#飞地图ID X坐标 Y坐标
			map.CreateMon(43,146,200,'经验大鸡鸡',1000)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			SubGameGold(Sender,300)
			return
	elif (Menu == 5):
		if Sender.Level < 35 : # 等级判断
			say  = """你的实力不够，请你离开。
			你需要35级才能进入
			
			[离开:99]"""             
		elif Sender.Level > 45 : # 等级判断
			say  = """你的实力已经不允许在这里玩了。
			你的实力已经足够了。
			
			[离开:99]"""    
                       
		elif (Sender.GameGold < 200):
			say = """你没有足够的元宝，无法传送。
			[离开:99]"""
		else:       
			map = Server.Envir.SEnvir.CreateMap(1528)                         #开启副本地图（地图ID）
			map.MapTime = datetime.now()+ timedelta(minutes=60);  #副本地图关卡时间设置
			Sender.Teleport(map,21,146)	#飞地图ID X坐标 Y坐标
			map.CreateMon(82,115,200,'经验小兔兔',800)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			SubGameGold(Sender,200)
			return
	elif (Menu == 4):
		if Sender.Level < 20 : # 等级判断
			say  = """你的实力不够，请你离开。
			你需要20级才能进入
			
			[离开:99]"""             
		elif Sender.Level > 35 : # 等级判断
			say  = """你的实力已经不允许在这里玩了。
			你的实力已经足够了。
			
			[离开:99]"""    
                       
		elif (Sender.GameGold < 100):
			say = """你没有足够的元宝，无法传送。
			[离开:99]"""
		else:       
			map = Server.Envir.SEnvir.CreateMap(1527)                         #开启副本地图（地图ID）
			map.MapTime = datetime.now()+ timedelta(minutes=60);  #副本地图关卡时间设置
			Sender.Teleport(map,164,22)	#飞地图ID X坐标 Y坐标
			map.CreateMon(127,69,200,'经验美羊羊',600)           #副本地图刷新的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量）
			SubGameGold(Sender,100)
			return



	elif (Menu == 8):
		if(PlayerGetV(Sender,GV_XINSHOUFB_ONOFF) == 0):    #定义个人全局变量 数值代表进入次数
			if (Sender.Prestige > 999):           #判断队长进入条件判断
				if(Sender.GroupMembers):                    #队伍判断
					if(Sender == Sender.GroupMembers[0]):   #队长判断
						bOpen = True
						if len(Sender.GroupMembers) < 2:    #判断队伍人数
							bOpen = False
							say = """队员数不足3人,无法进入.
								
							[离开:0]"""
						else:
							for player in Sender.GroupMembers:                 #遍历所有队员
								if(PlayerGetV(player,GV_XINSHOUFB_ONOFF) == 1):  #队员变量判断  数值判断是否进入次数
									bOpen = False
									say = """队伍中有队员已经去过副本了
									无法进入
										
									[离开:0]"""
									break

								if(Sender.Prestige < 1000):                #判断需要的声望
									bOpen = False
									say = """队伍中有队员“声望”不足1000，无法进入~
										
									[离开:0]"""
									break
						if bOpen:    #如果可以开启
							map = Server.Envir.SEnvir.CreateMap(502)               #开启副本地图  （地图ID）
							map.MapTime = datetime.now()+timedelta(minutes=60)    #副本地图关卡时间设置（分钟）
							map.CreateMon(50,175,100,'奔波儿灞',50)
							map.CreateMon(50,175,100,'奔波儿灞1',2)
							map.CreateMon(50,175,100,'奔波儿灞2',4)
							map.CreateMon(50,175,100,'钻风小队2',2)
							map.CreateMon(50,175,100,'钻风小队',25)
							map.CreateMon(132,104,100,'奔波儿灞',350)
							map.CreateMon(132,104,100,'奔波儿灞1',2)
							map.CreateMon(132,104,100,'奔波儿灞2',2)
							map.CreateMon(132,104,100,'钻风小队2',2)
							map.CreateMon(132,104,100,'钻风小队',25)
							map.CreateMon(261,34,100,'奔波儿灞',50)
							map.CreateMon(261,34,100,'奔波儿灞1',2)
							map.CreateMon(261,34,100,'奔波儿灞2',4)
							map.CreateMon(50,175,50,'灞波儿奔',30)
							map.CreateMon(50,175,50,'灞波儿奔1',2)
							map.CreateMon(50,175,50,'灞波儿奔2',2)
							map.CreateMon(132,104,100,'灞波儿奔',50)
							map.CreateMon(132,104,100,'灞波儿奔1',2)
							map.CreateMon(132,104,100,'灞波儿奔2',2)
							map.CreateMon(261,34,100,'灞波儿奔',50)
							map.CreateMon(261,34,100,'灞波儿奔1',5)
							map.CreateMon(261,34,100,'灞波儿奔2',2)
							map.CreateMon(261,34,100,'钻风小队',25)
							map.CreateMon(261,34,100,'钻风小队2',4)
							PlayerSetV(Sender,GV_XINSHOUFB_ONOFF,1)
							for player in Sender.GroupMembers:                     #遍历所有队员
								PlayerSetV(player,GV_XINSHOUFB_ONOFF,1)             #赋值变量为1，代表进入
								SubPrestige(player,200)                              #扣除声望
								player.Teleport(map,26,220)                        #把全组人传送进副本
					else:
						say = """不是队长
							
						[离开:0]"""
				else:
					say = """没有队伍
						
					[离开:0]"""
			else:
				say = """队长声望不够。。。。。。
					
				[离开:0]"""

		else:
			say = """每天只有1次探宝机会，已经不能再进入了。。。。。。
			
			[返回:99]"""
			
		Dict['Say']=say
		return Dict



	elif (Menu == 11):       
		if current_time_is_between("20:00:00", "22:00:00"):                #定义时间变量
			if(Sender.GameGold > 199):                #判断需要的物品数量
				SubGameGold(Sender,200)                  #扣除物品
				if (Sender.GroupMembers):   
					Sender.GroupLeave()  #如果判断有组，那么直接退出队伍在进入副本
				map = Server.Envir.SEnvir.CreateMap(440)                     #开启副本地图  （地图ID）
				map.CreateMon(280,142,20,'副本-暗黑战士',10)
				map.CreateMon(280,110,1,'副本-百花王',1)
				map.MapTime = datetime.now()+ timedelta(minutes=40);  #副本地图关卡时间设置
				Sender.Teleport(map,50,50)	#飞地图ID X坐标 Y坐标   
				return Dict   #不执行提示框
			else:
				say = "元宝不足，无法进入副本。。。。。"
		else:
			say = """时间未到

			[离开:0]"""
			
		Dict['Say']=say
		return Dict
	elif (Menu == 12):
		say = """<font color=\"0xff00ff00\">寻花之旅副本注意事项</font>

	<font color=\"0xffFFFF99\">副本开放时间：</font>

	<font color=\"0xff00ff00\">每日晚上8点至晚上10点</font>
	   
	<font color=\"0xff00ff00\">进入条件：200元宝，进入第二层需要1颗“魔晶石”/50元宝</font>
	
	<font color=\"0xff00ff00\">主要产出：1、“彼岸花”制作材料；集齐材料后可以在制作系统里完成。</font>	

	<font color=\"0xff00ff00\">2、初级时装制作材料，元宝，经验珠等物品</font>
		

		[返回:99]"""

	elif (Menu == 10):
		say = """<font color=\"0xff00ff00\">副本注意事项</font>

	<font color=\"0xffFFFF99\">雪原荒村副本：</font>

	<font color=\"0xff00ff00\">需要等级大于等于50级，每日一次机会</font>

	<font color=\"0xff00ff00\">开放时间：每日20点-22点</font>
	   
	<font color=\"0xff00ff00\">进入条件：至少5人组队，2魔晶石，100元宝</font>
	
	<font color=\"0xff00ff00\">主要产出：各类装备强化石、元宝、口哨</font>	

	<font color=\"0xffFFFF99\">生死挑战副本：</font>

	<font color=\"0xff00ff00\">全天开放，无等级限制，每日两次机会</font>	

	<font color=\"0xff00ff00\">进入条件：单人，门票200元宝/次</font>
	
	<font color=\"0xff00ff00\">产出：各类经验卷、元宝、碎片、船票</font>		

	<font color=\"0xffFFFF99\">奇遇副本：</font>

	<font color=\"0xff00ff00\">进入条件：声望大于等于1000，每次扣除200声望</font>	

	<font color=\"0xff00ff00\">至少三人组队进入</font>

	<font color=\"0xff00ff00\">杀怪有几率获得声望、元宝、特殊buff及特殊boss</font>			

		[返回:99]"""


#主菜单
	else:
		say = """==================欢迎进入副本探宝==================

	[寻花之旅副本介绍:12]
			
		           [寻花之旅:11] 

	[八大暗影:80]
    

		

	
	[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

def DelayCall(args):
	Sender=args[0]
	Sender.Connection.ReceiveChat("123",MessageType.System)
	Server.Envir.SEnvir.Log('delay开始了')

NpcEvent.add_listener(332, "OnClick", OnClick)
