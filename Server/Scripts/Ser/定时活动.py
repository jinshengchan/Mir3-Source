# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
from Defines import *
import ServerEvent
import Server
import clr
import random
import Utils.ServerUtils as ServerUtils
import datetime

from Ser import 怪物攻城
from Ser import 定时双倍
from Ser import 天下第一
from Ser import 死亡竞技场
from Ser import 死亡竞技场刷怪
clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir
import Npc.其他.便捷传送

def AutoRecycleWeapons(args=None):
    """自动回收武器函数 - 遍历所有在线玩家进行回收"""
    try:
        print("AutoRecycleWeapons: 开始调用武器回收...")
        from Npc.其他.便捷传送 import ExecuteEquipmentRecycleForSender, ExecuteCompanionEquipmentRecycleForSender, ExecuteCompanionFragmentForSender
        from Defines import GV_PLAYER_RECYCLE_ENABLED, GV_PLAYER_AUTO_FRAGMENT_ENABLED
        print("AutoRecycleWeapons: 导入成功，开始执行...")
        
        # 遍历所有在线玩家进行回收
        for player in SEnvir.Players:
            try:
                # 检查玩家的个人回收开关状态
                recycle_enabled = PlayerGetV(player, GV_PLAYER_RECYCLE_ENABLED)
                fragment_enabled = PlayerGetV(player, GV_PLAYER_AUTO_FRAGMENT_ENABLED)
                if recycle_enabled:
                    ExecuteEquipmentRecycleForSender(player)
                    ExecuteCompanionEquipmentRecycleForSender(player)
                if fragment_enabled:
                    ExecuteCompanionFragmentForSender(player)
            except Exception as e:
                print("玩家 {} 自动整理失败: {}".format(player.Character.CharacterName, e))
        
        print("AutoRecycleWeapons: 执行完成")
    except Exception as e:
        print("调用武器回收失败: {}".format(e))


# 活动格式为 ((开始时间), (结束时间), 活动函数名)
# 时间格式为 (每周几, 几点, 几分)
# 注意 周日是0 周一是1 以此类推 周六是6
# 注意 时间使用24小时制 结束时间需要晚于开始时间
# 活动函数需要根据传入的bool参数判断是开启活动(True) 还是结束活动(False)
TimedEvents = [
               ((1, 15, 34), (1, 15, 37), 定时双倍.doubleEXP),
               ((2, 20, 00), (2, 23, 00), 定时双倍.doubleEXP),
               ((3, 20, 00), (3, 23, 00), 定时双倍.doubleEXP),
               ((4, 20, 00), (4, 23, 00), 定时双倍.doubleEXP),
               ((5, 20, 00), (5, 23, 00), 定时双倍.doubleEXP),
               ((6, 11, 30), (6, 23, 59), 定时双倍.doubleDrop),
               ((0, 8, 00), (1, 15, 39), 定时双倍.doubleDrop),
#               ((1, 19, 59), (1, 22, 00),怪物攻城.TestSpawn1),
#               ((1, 21, 00), (1, 22, 00),怪物攻城.TestSpawn2),
#               ((1, 21, 58), (1, 22, 00),怪物攻城.TestSpawn3),
#               ((2, 19, 59), (2, 22, 00),怪物攻城.TestSpawn1),
#               ((2, 21, 00), (2, 22, 00),怪物攻城.TestSpawn2),
#               ((2, 21, 58), (2, 22, 00),怪物攻城.TestSpawn3),
#               ((3, 19, 59), (3, 22, 00),怪物攻城.TestSpawn1),
#               ((3, 21, 00), (3, 22, 00),怪物攻城.TestSpawn2),
#               ((3, 21, 58), (3, 22, 00),怪物攻城.TestSpawn3),
#               ((4, 19, 59), (4, 22, 00),怪物攻城.TestSpawn1),
#               ((4, 21, 00), (4, 22, 00),怪物攻城.TestSpawn2),
#               ((4, 21, 58), (4, 22, 00),怪物攻城.TestSpawn3),
#               ((5, 19, 59), (5, 22, 00),怪物攻城.TestSpawn1),
#               ((5, 21, 00), (5, 22, 00),怪物攻城.TestSpawn2),
#               ((5, 21, 58), (5, 22, 00),怪物攻城.TestSpawn3),
               ]

WeekTimedEvents = [
               [((6, 21, 50), (6, 21, 59), 死亡竞技场.doublePKTZ),
               ((6, 21, 55), (6, 21, 57), 死亡竞技场.doublePKTZ1),
               ((6, 22, 00), (6, 23, 59), 死亡竞技场.doublePK),
               ((6, 22, 01), (6, 23, 59), 死亡竞技场.doubleEXP),
               ((6, 22, 02), (6, 23, 59), 死亡竞技场.doubleEXP),
               ((6, 22, 03), (6, 23, 59), 死亡竞技场.doubleEXP),
               ((6, 22, 04), (6, 23, 59), 死亡竞技场.doubleEXP),
               ((6, 22, 06), (6, 23, 59), 死亡竞技场刷怪.TestSpawn1),
               ((6, 22, 12), (6, 23, 59), 死亡竞技场刷怪.TestSpawn2),
               ((6, 22, 18), (6, 23, 59), 死亡竞技场刷怪.TestSpawn3),
               ((6, 22, 24), (6, 23, 59), 死亡竞技场刷怪.TestSpawn4),
               ((6, 22, 30), (6, 23, 59), 死亡竞技场刷怪.TestSpawn5),
               ((6, 22, 36), (6, 23, 59), 死亡竞技场刷怪.TestSpawn6),
               ((6, 22, 42), (6, 23, 59), 死亡竞技场刷怪.TestSpawn7),
               ((6, 22, 48), (6, 23, 59), 死亡竞技场刷怪.TestSpawn8),
               ((6, 22, 54), (6, 23, 59), 死亡竞技场刷怪.TestSpawn9),],


               ]


# 进入新的一分钟时触发此函数

def OnMinuteChange(args):
	#判断服务器时间
	day_of_Week = (int)(args[0].DayOfWeek)
	hour = args[0].Hour
	minute = args[0].Minute
	res = []

	#ServerUtils.SendMsgToAll("day={}， hour={}， minute={}".format(day_of_Week, hour, minute), MessageType.System)
	
	print("OnMinuteChange: 触发时间 {}:{}:{}".format(hour, minute, args[0].Second))
	
	# 每分钟执行一次武器自动回收
	AutoRecycleWeapons()
	
	# 设置定时回收任务，每1秒执行一次
	try:
		SEnvir.PeriodicCall("ServerEvent.AutoRecycleWeapons", SEnvir.Now.AddSeconds(1), 1, 0)
		print("已设置定时回收任务，每1秒执行一次")
	except Exception as e:
		print("设置定时回收任务失败: {}".format(e))

	for event in TimedEvents:
		begin_time = event[0]
		end_time = event[1]

		if begin_time[0] == day_of_Week and begin_time[1] == hour and begin_time[2] == minute:
			# 开启活动
			res.append(event[2](True))
			continue
		if end_time[0] == day_of_Week and end_time[1] == hour and end_time[2] == minute:
			# 结束活动
			res.append(event[2](False))
			continue

	gregorianCalendar = System.Activator.CreateInstance(System.Globalization.GregorianCalendar)
	#获取指定日期是周数 CalendarWeekRule指定 第一周开始于该年的第一天，DayOfWeek指定每周第一天是星期几　
	weekOfYear= gregorianCalendar.GetWeekOfYear(SEnvir.Now, System.Globalization.CalendarWeekRule.FirstDay, System.DayOfWeek.Monday)
	for event in WeekTimedEvents[weekOfYear % len(WeekTimedEvents)]:
		begin_time = event[0]
		end_time = event[1]

		if begin_time[0] == day_of_Week and begin_time[1] == hour and begin_time[2] == minute:
			# 开启活动
			res.append(event[2](True))
			continue
		if end_time[0] == day_of_Week and end_time[1] == hour and end_time[2] == minute:
			# 结束活动
			res.append(event[2](False))
			continue

	return res

# 进入新的一天触发此函数
def OnDayChange(args):
    #判断服务器时间
    day_of_Week = (int)(args[0].DayOfWeek)
    hour = args[0].Hour
    minute = args[0].Minute
    day_of_Month = args[0].Day

    # 每日重置个人变量
    # 请移除PlayerProcess.py中OnDayChange()里面重置个人变量的语句
    # 并改为在这里进行重置
    # 这里复位所有玩家的某个变量 有多个变量需要重置的 都要写
    # SEnvir.ResetVariableForAllPlayers(变量名,默认值)
    SEnvir.ResetVariableForAllPlayers(GV_MEIRILIBAO_ONOFF,0) #每日礼包领取复位
    SEnvir.ResetVariableForAllPlayers(GV_AWMBOSSFB_COUNT,0) #沃玛普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BWMBOSSFB_COUNT,0) #沃玛噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CWMBOSSFB_COUNT,0) #沃玛地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_AZMBOSSFB_COUNT,0) #祖玛普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BZMBOSSFB_COUNT,0) #祖玛噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CZMBOSSFB_COUNT,0) #祖玛地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_AWGBOSSFB_COUNT,0) #蜈蚣普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BWGBOSSFB_COUNT,0) #蜈蚣噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CWGBOSSFB_COUNT,0) #蜈蚣地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_ASGMBOSSFB_COUNT,0) #石阁庙普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BSGMBOSSFB_COUNT,0) #石阁庙噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CSGMBOSSFB_COUNT,0) #石阁庙地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_ASJBOSSFB_COUNT,0) #神舰普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BSJBOSSFB_COUNT,0) #神舰噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CSJBOSSFB_COUNT,0) #神舰地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_ACYBOSSFB_COUNT,0) #赤月普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BCYBOSSFB_COUNT,0) #赤月噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CCYBOSSFB_COUNT,0) #赤月地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_APYBOSSFB_COUNT,0) #潘夜神殿普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BPYBOSSFB_COUNT,0) #潘夜神殿噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CPYBOSSFB_COUNT,0) #潘夜神殿地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_APYSBOSSFB_COUNT,0) #潘夜石窟普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BPYSBOSSFB_COUNT,0) #潘夜石窟噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CPYSBOSSFB_COUNT,0) #潘夜石窟地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_AZTGBOSSFB_COUNT,0) #真天宫普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BZTGBOSSFB_COUNT,0) #真天宫噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CZTGBOSSFB_COUNT,0) #真天宫地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_AHDGBOSSFB_COUNT,0) #黑度宫普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BHDGBOSSFB_COUNT,0) #黑度宫噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CHDGBOSSFB_COUNT,0) #黑度宫地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_ANMBOSSFB_COUNT,0) #诺玛遗址普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BNMBOSSFB_COUNT,0) #诺玛遗址噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CNMBOSSFB_COUNT,0) #诺玛遗址地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_AXSBOSSFB_COUNT,0) #西部沙漠普通副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BXSBOSSFB_COUNT,0) #西部沙漠噩梦副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CXSBOSSFB_COUNT,0) #西部沙漠地狱副本复位
    SEnvir.ResetVariableForAllPlayers(GV_APKSBOSSFB_COUNT,0) #沉鱼落雁副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BPKSBOSSFB_COUNT,0) #闭月羞花副本复位
    SEnvir.ResetVariableForAllPlayers(GV_CPKSBOSSFB_COUNT,0) #红粉骷髅副本复位
    SEnvir.ResetVariableForAllPlayers(GV_BOSSFB_COUNT,0) #比奇每日副本任务复位
    SEnvir.ResetVariableForAllPlayers(GV_ZDBOSSFB_COUNT,0) #每日副本任务复位
    SEnvir.ResetVariableForAllPlayers(GV_XINSHOUFB_ONOFF,0) #每日奇遇副本任务复位
    SEnvir.ResetVariableForAllPlayers(GV_BADA_COUNT,0) #八大暗影每日副本复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_WMGWCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_WMGWJSCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_WMWSJSCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_ZMGWCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_PKSCOUNT,0) #每日破空石副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_ARENAACCESS,0) #死亡竞技场进入次数复位
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_DEATHMATCH,0)  #死亡竞技场击杀人数复位
    SEnvir.ResetVariableForAllPlayers(TK_WXDZ_ONOFF,0)
    SEnvir.ResetVariableForAllPlayers(GV_NEW_PLAYER_EXP_BUFF_COUNT, 0)
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_LQZZLBJL, 0)
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_LQNMLBJL, 0)
    SEnvir.ResetVariableForAllPlayers(BV_QT_TODAY,0)  #每日任务复位
    SEnvir.ResetVariableForAllPlayers(BV_QT_KILLMON,0)  #每日任务杀怪复位
    SEnvir.ResetVariableForAllPlayers(BV_QT_KILLNUM,0)   #每日任务杀怪计数复位
    SEnvir.ResetVariableForAllPlayers(BV_NUM_DAILYTASK,0) #每日任务完成数量
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_RECYCLE_ENABLED, 1)  #回收开关默认开启
    Server.Envir.SEnvir.Log("隔天调用成功")
    if(day_of_Week == 1):   #周判断
        OnWeekChange(args)
    if(day_of_Month == 1):                 #月判断
        OnMonthChange(args)
    
    
ResetVariable = [
	GV_PLAYER_ZHOUPAOCHUANG,  #周跑船任务复位
	GV_PLAYER_ZHOUJINGJICHANG, #周竞技场活动复位
]

def OnWeekChange(args):
	SEnvir.ResetVariableForAllPlayers(ResetVariable,0)
	SEnvir.ResetVariableForAllPlayers(GV_PLAYER_LIUYIPAOKUARMOUR,0)
	SEnvir.ResetVariableForAllPlayers(GV_PLAYER_JINGJIARMOUR,0)
	GlobalSetV(GV_PLAYER_BUFF1, 0) #BUFF1
	GlobalSetV(GV_PLAYER_BUFF2, 0) #BUFF2
	GlobalSetV(GV_PLAYER_BUFF3, 0) #BUFF3
	GlobalSetV(GV_PLAYER_BUFF4, 0) #BUFF4
	GlobalSetV(GV_PLAYER_BUFF5, 0) #BUFF5
	GlobalSetV(GV_PLAYER_BUFF6, 0) #BUFF6
	GlobalSetV(GV_PLAYER_BUFF7, 0) #BUFF7
	GlobalSetV(GV_PLAYER_BUFF8, 0) #BUFF8
	GlobalSetV(GV_PLAYER_BUFF9, 0) #BUFF9
	GlobalSetV(GV_PLAYER_BUFF10, 0) #BUFF10
	GlobalSetV(GV_PLAYER_BUFF11, 0) #BUFF11
	Server.Envir.SEnvir.Log("隔周调用成功")    

ServerEvent.add_listener("OnMinuteChange",OnMinuteChange)
ServerEvent.add_listener("OnDayChange",OnDayChange)
