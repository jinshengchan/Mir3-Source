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
import Server.Models.MonsterObject as Monster
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
from Utils.PlayerUtils import *
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
import random
from 变量.默认变量 import *
from 变量.任务杀怪 import *
from 主线任务奖励 import *
from string import digits

# 击杀怪物的index
# KILL_MON = [] 为任意怪物
KILL_MON = [10114,10115,10116,10117,10118]  #诺玛的怪物
KILL_MONDZ = [20022]  #诺玛的怪物
# 副本怪物的index
KILL_DUNG_MON1 = [100579]  #副本的怪物1
KILL_DUNG_MON2 = [100581]  #副本的怪物2
KILL_DUNG_MON3 = [100580]  #副本的怪物3
# 副本小boss的index
KILL_DUNG_ELITE = [100569,100570,100572,100576,100577,100578,100573,100574]  #副本的小BOSS
# 破空石小boss的index
KILL_PKS_ELITE = [106630,106631,106632,106633]  #副本的小BOSS



		
def OnKillMon(args):
	Sender = args[0]
	MonsterInfo = args[1]
	kill_map = SEnvir.GetMap(Sender.Character.CurrentMap)
    
	current_map = SEnvir.GetMap(Sender.Character.CurrentMap)        #获取当前角色所在的地图
	NEW_PLAYER_EXP_BUFF_INDEX = 149
	list = MonsterInfo.MonsterName                                  #获取怪物名称
        monList = [                                                 #设定需要的命运怪物
        ("奔波儿灞2"),
        ("钻风小队2"),   
        ("麋鹿"),      
        ("灞波儿奔2"),]


	
	if MonsterInfo.Index in KILL_MON:  #判断击杀诺玛怪物的信息
		PlayerSetV(Sender,GV_KILLMON_NMGWCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWCOUNT) + 1)   #新书兑换任务变量增加
		PlayerSetV(Sender,GV_KILLMON_NMGWJSCOUNT,PlayerGetV(Sender,GV_KILLMON_NMGWJSCOUNT) + 1)  #杀死诺玛怪物变量增加
	#Sender.Connection.ReceiveChat("你成功击杀了怪物{}".format(MonsterInfo.MonsterName), MessageType.System)

	if MonsterInfo.Index in KILL_MONDZ:  #判断击杀诺玛队长的信息
		PlayerSetV(Sender,GV_KILLMON_NMDZJSCOUNT,PlayerGetV(Sender,GV_KILLMON_NMDZJSCOUNT) + 1)   #杀死诺玛队长变量增加

	if(PlayerGetV(Sender,GV_KILLMON_NMGWJSCOUNT)== 200):  #如果杀死诺玛怪物的数量达到200只
		PlayerSetV(Sender,GV_KILLMON_NMGWJSCOUNT,0)   #先把杀死诺玛怪物的计数清零
		#在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 2格范围内 刷怪的名字  刷怪的数量)
		Sender.CurrentMap.CreateMon(Sender.CurrentLocation.X,Sender.CurrentLocation.Y,2,'诺玛突击队长',1)
		#系统发出公告提示
		Sender.Connection.ReceiveChat("由于玩家 {} 杀死了诺玛怪物200个，触发了队长的复仇，诺玛突击队长出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)

	if(PlayerGetV(Sender,GV_KILLMON_NMDZJSCOUNT)== 100):  #如果杀死诺玛队长的数量达到100只
		PlayerSetV(Sender,GV_KILLMON_NMDZJSCOUNT,0)   #先把杀死诺玛队长的计数清零
		#在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 5格范围内 刷怪的名字  刷怪的数量)
		Sender.CurrentMap.CreateMon(Sender.CurrentLocation.X,Sender.CurrentLocation.Y,5,'诺玛教主',1)
		#系统发出公告提示
		Sender.Connection.ReceiveChat("由于玩家 {} 杀死了诺玛突击队长100个，触发了教主的复仇，诺玛教主出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)

	#古墓3小BOSS 古墓土偶护卫武士
	#if MonsterInfo.Index == 389:
		#击杀古墓3小BOSS.OnKillGumuBoss1()



	# 副本怪计数
	#
	# 副本全局变量注释：
	# 怪物1：GV_KILLMON_WMGWCOUNT
	# 怪物2：GV_KILLMON_WMGWJSCOUNT
	# 怪物3：GV_KILLMON_WMWSJSCOUNT
	# 小boss：GV_KILLMON_ZMGWCOUNT
	#
	if(Sender.GroupMembers):                    # 队伍判断
		# 判断小怪
		if MonsterInfo.Index in KILL_DUNG_MON1:  # 判断副本小怪1
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_WMGWCOUNT,PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_WMGWCOUNT) + 1)  #杀死副本怪物1变量增加

		if MonsterInfo.Index in KILL_DUNG_MON2:  # 判断副本小怪2
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_WMGWJSCOUNT,PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_WMGWJSCOUNT) + 1)  #杀死副本怪物2变量增加

		if MonsterInfo.Index in KILL_DUNG_MON3:  # 判断副本小怪3
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_WMWSJSCOUNT,PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_WMWSJSCOUNT) + 1)  #杀死副本怪物3变量增加
			#Sender.Connection.ReceiveChat("你成功击杀了怪物{}".format(MonsterInfo.MonsterName), MessageType.System)

		# 判断小boss
		if MonsterInfo.Index in KILL_DUNG_ELITE:  #判断副本小boss
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_ZMGWCOUNT,PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_ZMGWCOUNT) + 1)   #杀死副本小BOSS变量增加

		# 生成小boss
		if(PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_WMGWCOUNT) == 200): # 生成小boss
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_WMGWCOUNT,0) # 清除计数
			#在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 2格范围内 刷怪的名字  刷怪的数量)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,5,'霸王教主【副本】',1)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,10,'地天灭王【副本】',1)
			#系统发出公告提示
			Sender.Connection.ReceiveChat("由于玩家 {} 杀死了副本怪物200个，触发了队长的复仇，霸王教主【副本】出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
			Sender.Connection.ReceiveChat("由于玩家 {} 杀死了副本怪物200个，触发了队长的复仇，地天灭王【副本】出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)

		if(PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_WMGWJSCOUNT) == 200): # 生成小boss2
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_WMGWJSCOUNT,0) # 清除计数
			#在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 2格范围内 刷怪的名字  刷怪的数量)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,100,'辣手将军',1)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,200,'摧花将军',1)
			#系统发出公告提示
			Sender.Connection.ReceiveChat("由于玩家 {} 杀死了副本怪物200个，触发了队长的复仇，辣手将军出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
			Sender.Connection.ReceiveChat("由于玩家 {} 杀死了副本怪物200个，触发了队长的复仇，摧花将军出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)

		if(PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_WMWSJSCOUNT) == 150): # 生成小boss3
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_WMWSJSCOUNT,0) # 清除计数
			#在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 N格范围内 刷怪的名字  刷怪的数量)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,150,'赤翼教主',1)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,150,'蓝翼教主',1)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,150,'伯光兄',1)
			#系统发出公告提示
			Sender.Connection.ReceiveChat("由于玩家 {} 杀死了副本怪物150个，触发了队长的复仇，赤翼教主出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
			Sender.Connection.ReceiveChat("由于玩家 {} 杀死了副本怪物150个，触发了队长的复仇，蓝翼教主出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
			Sender.Connection.ReceiveChat("由于玩家 {} 杀死了副本怪物150个，触发了队长的复仇，伯光兄出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)

		# 生成大boss并清除计数值
		if(PlayerGetV(Sender.GroupMembers[0],GV_KILLMON_ZMGWCOUNT) == 8): # ！！数字对应着小boss数量
			PlayerSetV(Sender.GroupMembers[0],GV_KILLMON_ZMGWCOUNT,0)   #先把杀小BOSS的计数清零
			#在玩家当前地图刷出指定的怪物(刷怪的X和Y坐标 5格范围内 刷怪的名字  刷怪的数量)
			Sender.CurrentMap.CreateMon(Sender.GroupMembers[0].CurrentLocation.X,Sender.CurrentLocation.Y,200,'玛珐之主',1)
			#系统发出公告提示
			Sender.Connection.ReceiveChat("由于玩家 {} 打败了无数魔王的爪牙，触发了教主的怒火，玛珐之主出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
	# 副本怪计数结束

	# 奇遇地图怪物脚本
        if (list) in monList:
        	Sender.Connection.ReceiveChat("你成功击杀了奇遇怪物{}，幸运之轮已经启动".format(MonsterInfo.MonsterName), MessageType.System)
        	select = random.randint(0,1000)
        	if select < 5:
        			Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.Luck, 1, StatSource.Enhancement)   #给手里武器1点幸运属性并刷新属性值
        			Sender.Connection.ReceiveChat("天降机缘，你的武器幸运增加了1点", MessageType.System)
        	elif select < 30:
        			Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.CriticalChance, 1, StatSource.Enhancement)   #给手里武器增加1%暴击几率属性并刷新属性值
        			Sender.Connection.ReceiveChat("天降机缘，你的武器增加了1%暴击几率", MessageType.System)
        	elif select < 40:
        			Sender.ItemStatsChangeRefresh(int(EquipmentSlot.Weapon), Stat.DropRate, 1, StatSource.Enhancement)   #给手里武器增加1%爆率几率属性并刷新属性值
        			Sender.Connection.ReceiveChat("天降机缘，你的武器增加了1%爆率几率", MessageType.System)
        	elif select < 45:
        			Sender.GiveItem("新能源（小）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物新能源", MessageType.System)
        	elif select < 50:
        			Sender.GiveItem("虚空宝珠（衣服）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物", MessageType.System)
        	elif select < 50:
        			Sender.GiveItem("虚空宝珠（鞋子）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物", MessageType.System)
        	elif select < 50:
        			Sender.GiveItem("虚空宝珠（头盔）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物", MessageType.System)
        	elif select < 60:
        			Sender.GiveItem("虚空宝珠（戒指）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物", MessageType.System)
        	elif select < 70:
        			Sender.GiveItem("虚空宝珠（项链）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物", MessageType.System)
        	elif select < 80:
        			Sender.GiveItem("虚空宝珠（手镯）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物", MessageType.System)
        	elif select < 120:
        			Sender.GiveItem("黑龙宝珠",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物黑龙宝珠", MessageType.System)
        	elif select < 130:
        			Sender.GiveItem("召唤券（田园犬）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物召唤券", MessageType.System)
        	elif select < 130:
        			Sender.GiveItem("召唤券（精灵猫）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物召唤券", MessageType.System)
        	elif select < 130:
        			Sender.GiveItem("召唤券（机灵鼠）",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物召唤券", MessageType.System)
        	elif select < 140:
        			Sender.GiveItem("经验爆率补药",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你我收藏的宝物经验爆率补药", MessageType.System)
        	elif select < 150:
        			current_map.CreateMon(102,110,10,'红月教主', 1)  #在指定地图刷的怪物 （怪物名字或者ID，怪物数量，刷怪坐标X,Y,范围,)
        			Sender.Connection.ReceiveChat("玩家 {} 在奇遇地图冒险，大地颤抖，红月教主出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
        	elif select < 150:
        			current_map.CreateMon(173,62,5,'蓝月教主', 1)  #在指定地图刷的怪物 （怪物名字或者ID，怪物数量，刷怪坐标X,Y,范围,)
        			Sender.Connection.ReceiveChat("玩家 {} 在奇遇地图冒险，周围突然寂静无声，蓝月教主出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
        	elif select < 200:
        			current_map.CreateMon(161,188,20,'飞羽卫',2)  #在当前地图刷的怪物 （刷怪坐标X,Y,范围,怪物名字或者ID，怪物数量)
        			Sender.Connection.ReceiveChat("玩家 {} 杀死了奇遇地图的怪物，天空一道闪电，飞羽卫出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
        	elif select < 250:
        			current_map.CreateMon( 179, 85, 10,'麋鹿', 3)  #在指定地图刷的怪物 （怪物名字或者ID，怪物数量，刷怪坐标X,Y,范围,)
        			Sender.Connection.ReceiveChat("玩家 {} 在奇遇地图冒险，天降祥瑞，麋鹿出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)
        	#elif select < 400:
        			#Sender.TeleportByMapIndex(2,40,33)	#飞地图ID X坐标 Y坐标
        			#Sender.Connection.ReceiveChat("移动巴拉巴拉写什么", MessageType.System)
        	elif select < 380:
        			Sender.GiveItem("金条",1)         #给道具+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你一条小黄鱼", MessageType.System)
        	elif select < 400:
        			GiveGameGold(Sender,1000)         #给元宝+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你1000元宝", MessageType.System)
        	elif select < 400:
        			GivePrestige(Sender,200)         #给元宝+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你200声望", MessageType.System)

        	elif select < 600:
        			GiveGameGold(Sender,500)         #给元宝+数量
        			Sender.Connection.ReceiveChat("别杀我，我给你500元宝", MessageType.System)
        	elif select < 650:
        			GivePrestige(Sender,100)         #给声望+数量
        			Sender.Connection.ReceiveChat("别杀我，给你100点声望", MessageType.System)
        	elif select < 700:
        			GiveGameGold(Sender,100)         #给元宝+数量
        			Sender.Connection.ReceiveChat("别打我，我给你100元宝", MessageType.System)
        	elif select < 800:
        			GivePrestige(Sender,50)         #给声望+数量
        			Sender.Connection.ReceiveChat("别杀我，给你50点声望", MessageType.System)

        	else:
        			Sender.CustomBuffAdd(NEW_PLAYER_EXP_BUFF_INDEX)      #给自定义BUFF
        			Sender.Connection.ReceiveChat("怪物的祝福BUFF", MessageType.System)

	# PKS副本怪计数
	#
	# 副本全局变量注释：

	# 小boss：GV_KILLMON_PKSCOUNT
	# 
	if(Sender.GroupMembers):                    # 队伍判断
		if MonsterInfo.Index in KILL_PKS_ELITE:  #判断击杀诺玛队长的信息
			PlayerSetV(Sender,GV_KILLMON_PKSCOUNT,PlayerGetV(Sender,GV_KILLMON_PKSCOUNT) + 1)   #杀小BOSS变量增加

		if(PlayerGetV(Sender,GV_KILLMON_PKSCOUNT)== 4):  #如果杀死小BOSS的数量达到4只
			PlayerSetV(Sender,GV_KILLMON_PKSCOUNT,0)   #先把杀死小BOSS的计数清零
			#Sender.CurrentMap.CreateMon(Sender.CurrentLocation.X,Sender.CurrentLocation.Y,5,'红拂',1)
			#系统发出公告提示
			current_map.CreateMon(77, 82, 1,'红拂', 1)  #在指定地图刷的怪物 （怪物名字或者ID，怪物数量，刷怪坐标X,Y,范围,)
			Sender.Connection.ReceiveChat("玩家 {} 在破碎虚空杀死魔王无数，周围突然寂静无声，强大的“红拂”出现在 {} [{}:{}]".format(Sender.Name, Sender.CurrentMap.Info.Description, Sender.CurrentLocation.X, Sender.CurrentLocation.Y), MessageType.System)






	if(Sender.GroupMembers):                                        #检测是否组队
		for player in Sender.GroupMembers:                          #遍历队员
			pc_map = SEnvir.GetMap(player.Character.CurrentMap)     #定位队员的地图信息
			if pc_map == kill_map:                                  #检测同组队员处于同一地图
				X = Sender.Character.CurrentLocation.X
				Y = Sender.Character.CurrentLocation.Y
				X1 = player.Character.CurrentLocation.X
				Y1 = player.Character.CurrentLocation.Y
				if X - 16 < X1 < X + 16 and Y - 16 < Y1 < Y + 16:
					if PlayerGetV(player,BV_QT_KILLMON) == 1:
						TaskNumber = PlayerGetV(player,BV_QT_TODAY)
						if TaskNumber > 0:
							DailyTaskList = GetDailyTaskList(player,TaskNumber)
							if DailyTaskList:
								DailyKillMon(player,MonsterInfo,DailyTaskList)
					if PlayerGetV(player,BV_NQ_KILLMON) == 1:
						if PlayerGetV(player,BV_NQ_MAIN) in MainTaskMonsters:
							MainQuestList = MainTaskMonsters[PlayerGetV(player,BV_NQ_MAIN)]
							if MainQuestList:
								zdq = MainQuestList.get('组队')
								if zdq == 1:
									NQKillMon(player,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_MAIN))
					if PlayerGetV(player,BV_NQ_SKILLMON) == 1:
						if PlayerGetV(player,BV_NQ_SKILL) in SkillTaskMonsters:
							MainQuestList = SkillTaskMonsters[PlayerGetV(player,BV_NQ_SKILL)]
							if MainQuestList:
								zdq = MainQuestList.get('组队')
								if zdq == 1:
									NQSKillMon(player,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SKILL))
					if PlayerGetV(player,BV_NQ_SJKILLMON) == 1:
						if PlayerGetV(player,BV_NQ_SJKILL) in ShipTaskMonsters:
							MainQuestList = ShipTaskMonsters[PlayerGetV(player,BV_NQ_SJKILL)]
							if MainQuestList:
								zdq = MainQuestList.get('组队')
								if zdq == 1:
									NQShipKillMon(player,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SJKILL))
					
	else:
		if PlayerGetV(Sender,BV_QT_KILLMON) == 1:
			TaskNumber = PlayerGetV(Sender,BV_QT_TODAY)
			if TaskNumber > 0 :
				DailyTaskList = GetDailyTaskList(Sender,TaskNumber)
				if DailyTaskList:
					DailyKillMon(Sender,MonsterInfo,DailyTaskList)
		if PlayerGetV(Sender,BV_NQ_KILLMON) == 1:
			if PlayerGetV(Sender,BV_NQ_MAIN) in MainTaskMonsters:
				MainQuestList = MainTaskMonsters[PlayerGetV(Sender,BV_NQ_MAIN)]
				if MainQuestList:
					NQKillMon(Sender,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_MAIN))
		if PlayerGetV(Sender,BV_NQ_SKILLMON) == 1:
			if PlayerGetV(Sender,BV_NQ_SKILL) in SkillTaskMonsters:
				MainQuestList = SkillTaskMonsters[PlayerGetV(Sender,BV_NQ_SKILL)]
				if MainQuestList:
					NQSKillMon(Sender,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SKILL))
		if PlayerGetV(Sender,BV_NQ_SJKILLMON) == 1:
			if PlayerGetV(Sender,BV_NQ_SJKILL) in ShipTaskMonsters:
				MainQuestList = ShipTaskMonsters[PlayerGetV(Sender,BV_NQ_SJKILL)]
				if MainQuestList:
					NQShipKillMon(Sender,MonsterInfo,MainQuestList,PlayerGetV(Sender,BV_NQ_SJKILL))





















####万事通任务杀怪
def DailyKillMon(Sender,MonsterInfo,DailyTaskList):
	kn = PlayerGetV(Sender,BV_QT_KILLNUM)               #kn = 万事通任务杀怪数量
	mk = MonsterInfo.MonsterName                        #获取怪物名称
	mks = MonsterInfo.MonsterName
	mks = mks.translate(None,digits)  #怪物名去除数字后缀
	nt = DailyTaskList.get('杀怪数量')
	if DailyTaskList.get('任务怪物'):
		if mk in DailyTaskList.get('任务怪物'):
			kn += 1
			PlayerSetV(Sender,BV_QT_KILLNUM,kn)
			
			if kn < nt:
				
				Sender.Connection.ReceiveChat("万事通任务：您打败了 1 只 {} ，累计 {} 只怪物！".format(mks,kn), MessageType.Combat)
				return
			else:
				PlayerSetV(Sender,BV_QT_KILLMON,0)
				Sender.Connection.ReceiveChat("万事通任务：您已经打败足够的 {} ，可以回去交差了。".format(mks), MessageType.Combat)

####江湖任务杀怪
def NQKillMon(Sender,MonsterInfo,MainQuestList,index):
	knq = PlayerGetV(Sender,BV_NQ_KILLNUM)              #knq = 江湖任务杀怪数量
	mk = MonsterInfo.MonsterName                        #获取怪物名称
	igq = PlayerGetV(Sender,BV_NQ_ITEMGOT)              #ig = 江湖任务杀怪获得道具变量
	tiq = MainQuestList.get('任务道具')
	ig = MainQuestList.get('道具数量')
	ntq = MainQuestList.get('目标参数')
	if mk in MainQuestList.get('任务怪物'):
		if ig == '':
			knq += 1
			PlayerSetV(Sender,BV_NQ_KILLNUM,knq)
			if knq < ntq:
				return
			else:
				PlayerSetV(Sender,BV_NQ_KILLMON,0)
				mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
				mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
				mynpc.NPCCall(Sender)
				Sender.Connection.ReceiveChat("江湖任务：完成杀怪！", MessageType.Combat)
		elif igq < ig:
			select = random.randint(0,1000)
			if select < ntq:
				igq += 1
				Sender.GiveItem(tiq,1)
				PlayerSetV(Sender,BV_NQ_ITEMGOT,igq)
				if igq == ig:
					PlayerSetV(Sender,BV_NQ_KILLMON,0)
					PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
					mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
					mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
					mynpc.NPCCall(Sender)
					Sender.Connection.ReceiveChat("江湖任务：完成！", MessageType.Combat)
			else:
				Sender.Connection.ReceiveChat("任务：没有找到 {} ，继续寻找吧...".format(tiq), MessageType.Combat)


####神舰任务杀怪
def NQShipKillMon(Sender,MonsterInfo,MainQuestList,index):
	knq = PlayerGetV(Sender,BV_NQ_SJKILLNUM)              #knq = 神舰任务杀怪数量
	mk = MonsterInfo.MonsterName                        #获取怪物名称
	igq = PlayerGetV(Sender,BV_NQ_SJKILLITEMGOT)              #ig = 神舰任务杀怪获得道具变量
	tiq = MainQuestList.get('任务道具')
	ig = MainQuestList.get('道具数量')
	ntq = MainQuestList.get('目标参数')
	if mk in MainQuestList.get('任务怪物'):
		if ig == '':
			knq += 1
			PlayerSetV(Sender,BV_NQ_SJKILLNUM,knq)
			if knq < ntq:
				return
			else:
				PlayerSetV(Sender,BV_NQ_SJKILLMON,0)
				mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
				mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
				mynpc.NPCCall(Sender)
				Sender.Connection.ReceiveChat("神舰任务：完成杀怪！", MessageType.Combat)
		elif igq < ig:
			select = random.randint(0,1000)
			if select < ntq:
				igq += 1
				Sender.GiveItem(tiq,1)
				PlayerSetV(Sender,BV_NQ_SJKILLITEMGOT,igq)
				if igq == ig:
					PlayerSetV(Sender,BV_NQ_SJKILLMON,0)
					PlayerSetV(Sender,BV_NQ_SJKILLITEMGOT,0)
					mynpc = System.Activator.CreateInstance(Server.Models.NPCObject)
					mynpc.NPCInfo = Server.Envir.SEnvir.GetNpcInfo(277)
					mynpc.NPCCall(Sender)
					Sender.Connection.ReceiveChat("神舰任务：完成！", MessageType.Combat)
			else:
				Sender.Connection.ReceiveChat("任务：没有找到 {} ，继续寻找吧...".format(tiq), MessageType.Combat)

PlayerEvent.add_listener("OnKillMon",OnKillMon)

