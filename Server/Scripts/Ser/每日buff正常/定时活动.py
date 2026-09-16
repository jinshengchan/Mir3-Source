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


from Ser import 怪物攻城
from Ser import 定时双倍
from Ser import 天下第一

clr.AddReference("Library")
clr.AddReference('System')
from Library import *
import Server.Envir.SEnvir as SEnvir



def AutoRecycleWeapons(args=None):
    """自动回收武器函数 - 遍历所有在线玩家进行回收"""
    try:
        print("AutoRecycleWeapons: 开始调用武器回收...")
        from Npc.管理中心 import ExecuteEquipmentRecycleForSender
        from Defines import GV_PLAYER_RECYCLE_ENABLED
        print("AutoRecycleWeapons: 导入成功，开始执行...")
        
        # 遍历所有在线玩家进行回收
        for player in SEnvir.Players:
            try:
                # 检查玩家的个人回收开关状态
                recycle_enabled = PlayerGetV(player, GV_PLAYER_RECYCLE_ENABLED)
                if recycle_enabled:
                    ExecuteEquipmentRecycleForSender(player)
                else:
                    print("玩家 {} 的回收功能已关闭，跳过回收".format(player.Character.CharacterName))
            except Exception as e:
                print("玩家 {} 回收失败: {}".format(player.Character.CharacterName, e))
        
        print("AutoRecycleWeapons: 执行完成")
    except Exception as e:
        print("调用武器回收失败: {}".format(e))


# 活动格式为 ((开始时间), (结束时间), 活动函数名)
# 时间格式为 (每周几, 几点, 几分)
# 注意 周日是0 周一是1 以此类推 周六是6
# 注意 时间使用24小时制 结束时间需要晚于开始时间
# 活动函数需要根据传入的bool参数判断是开启活动(True) 还是结束活动(False)
TimedEvents = [
               ((1, 20, 00), (1, 23, 00), 定时双倍.doubleEXP),
               ((2, 20, 00), (2, 23, 00), 定时双倍.doubleEXP),
               ((3, 20, 00), (3, 23, 00), 定时双倍.doubleEXP),
               ((4, 20, 00), (4, 23, 00), 定时双倍.doubleEXP),
               ((5, 20, 00), (5, 23, 00), 定时双倍.doubleEXP),
               ((6, 8, 00), (6, 23, 00), 定时双倍.doubleDrop),
               ((0, 8, 00), (0, 23, 00), 定时双倍.doubleDrop),
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
		SEnvir.ScheduledCall("Ser.定时活动.AutoRecycleWeapons", SEnvir.Now.AddSeconds(1), 0)
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
    return res

# 进入新的一天触发此函数
def OnDayChange(args):
    #判断服务器时间
    day_of_Week = (int)(args[0].DayOfWeek)
    hour = args[0].Hour
    minute = args[0].Minute

    # 每日重置个人变量
    # 请移除PlayerProcess.py中OnDayChange()里面重置个人变量的语句
    # 并改为在这里进行重置
    # 这里复位所有玩家的某个变量 有多个变量需要重置的 都要写
    # SEnvir.ResetVariableForAllPlayers(变量名,默认值)
    SEnvir.ResetVariableForAllPlayers(GV_MEIRILIBAO_ONOFF,0) #每日礼包领取复位
    SEnvir.ResetVariableForAllPlayers(GV_BOSSFB_COUNT,0) #比奇每日副本任务复位
    SEnvir.ResetVariableForAllPlayers(GV_ZDBOSSFB_COUNT,0) #每日副本任务复位
    SEnvir.ResetVariableForAllPlayers(GV_XINSHOUFB_ONOFF,0) #每日奇遇副本任务复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_WMGWCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_WMGWJSCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_WMWSJSCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(GV_KILLMON_ZMGWCOUNT,0) #每日X副本怪物复位
    SEnvir.ResetVariableForAllPlayers(TK_WXDZ_ONOFF,0)
    SEnvir.ResetVariableForAllPlayers(GV_NEW_PLAYER_EXP_BUFF_COUNT, 0)
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_LQZZLBJL, 0)
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_LQNMLBJL, 0)
    SEnvir.ResetVariableForAllPlayers(BV_QT_TODAY,0)  #每日任务复位
    SEnvir.ResetVariableForAllPlayers(BV_QT_KILLMON,0)  #每日任务杀怪复位
    SEnvir.ResetVariableForAllPlayers(BV_QT_KILLNUM,0)   #每日任务杀怪计数复位
    SEnvir.ResetVariableForAllPlayers(BV_NUM_DAILYTASK,0) #每日任务完成数量
    SEnvir.ResetVariableForAllPlayers(GV_PLAYER_RECYCLE_ENABLED, 1)  #回收开关默认开启
    #Sender.Connection.ReceiveChat("******玛法大陆迎来了新的一天******",MessageType.System)	
    #Server.Envir.SEnvir.Log("隔天调用成功")

ServerEvent.add_listener("OnMinuteChange",OnMinuteChange)
ServerEvent.add_listener("OnDayChange",OnDayChange)
