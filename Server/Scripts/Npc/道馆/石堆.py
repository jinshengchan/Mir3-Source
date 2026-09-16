# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
clr.AddReference("Library")
from Library import *
import collections
import MapEvent
import NpcEvent
import Server.Envir.SEnvir as SEnvir
import Utils.ServerUtils as ServerUtils
import time
from 主线任务奖励 import *
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

#跳转菜单1
	if (Menu == 1):
		say = """

                       石头机关
        
        
               ●                    ●
             ●●●                ○●●
               ○                    ●
               
                      [推动石头:90]
                        
            [顺时针转:2]             [顺时针转:12]
            [逆时针转:4]             [逆时针转:14]"""    
	elif (Menu == 12):
		say = """

                       石头机关
        
        
               ●                    ○
             ●●●                ●●●
               ○                    ●
               
                      [推动石头:90]
                        
            [顺时针转:22]             [顺时针转:13]
            [逆时针转:42]             [逆时针转:1]"""    
	elif (Menu == 13):
		say = """

                       石头机关
        
        
               ●                    ●
             ●●●                ●●○
               ○                    ●
               
                      [推动石头:90]
                        
            [顺时针转:23]             [顺时针转:14]
            [逆时针转:43]             [逆时针转:12]"""    
	elif (Menu == 14):
		say = """

                       石头机关
        
        
               ●                    ●
             ●●●                ●●●
               ○                    ○
               
                      [推动石头:90]
                        
            [顺时针转:24]             [顺时针转:1]
            [逆时针转:44]             [逆时针转:13]"""    
	elif (Menu == 2):
		say = """

                       石头机关
        
        
               ●                    ●
             ○●●                ○●●
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:3]             [顺时针转:22]
            [逆时针转:1]             [逆时针转:24]"""    
	elif (Menu == 22):
		say = """

                       石头机关
        
        
               ●                    ○
             ○●●                ●●●
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:32]             [顺时针转:23]
            [逆时针转:12]             [逆时针转:2]"""    
	elif (Menu == 23):
		say = """

                       石头机关
        
        
               ●                    ●
             ○●●                ●●○
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:33]             [顺时针转:24]
            [逆时针转:13]             [逆时针转:22]"""    
	elif (Menu == 24):
		say = """

                       石头机关
        
        
               ●                    ●
             ○●●                ●●●
               ●                    ○
               
                      [推动石头:90]
                        
            [顺时针转:34]             [顺时针转:2]
            [逆时针转:14]             [逆时针转:23]"""    
	elif (Menu == 3):
		say = """

                       石头机关
        
        
               ○                    ●
             ●●●                ○●●
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:4]             [顺时针转:32]
            [逆时针转:2]             [逆时针转:34]"""    
	elif (Menu == 32):
		say = """

                       石头机关
        
        
               ○                    ○
             ●○●                ●○●
               ●                    ●
               
                      [推动石头:9]
                        
            [顺时针转:42]             [顺时针转:33]
            [逆时针转:22]             [逆时针转:3]"""    
	elif (Menu == 33):
		say = """

                       石头机关
        
        
               ○                    ●
             ●●●                ●●○
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:43]             [顺时针转:34]
            [逆时针转:23]             [逆时针转:32]"""    
	elif (Menu == 34):
		say = """

                       石头机关
        
        
               ○                    ●
             ●●●                ●●●
               ●                    ○
               
                      [推动石头:90]
                        
            [顺时针转:44]             [顺时针转:3]
            [逆时针转:24]             [逆时针转:33]"""    
	elif (Menu == 4):
		say = """

                       石头机关
        
        
               ●                    ●
             ●●○                ○●●
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:1]             [顺时针转:42]
            [逆时针转:3]             [逆时针转:44]"""    
	elif (Menu == 42):
		say = """

                       石头机关
        
        
               ●                    ○
             ●●○                ●●●
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:12]             [顺时针转:43]
            [逆时针转:32]             [逆时针转:4]"""    
	elif (Menu == 43):
		say = """

                       石头机关
        
        
               ●                    ●
             ●●○                ●●○
               ●                    ●
               
                      [推动石头:90]
                        
            [顺时针转:13]             [顺时针转:44]
            [逆时针转:33]             [逆时针转:42]"""    
	elif (Menu == 44):
		say = """

                       石头机关
        
        
               ●                    ●
             ●●○                ●●●
               ●                    ○
               
                      [推动石头:90]
                        
            [顺时针转:14]             [顺时针转:4]
            [逆时针转:34]             [逆时针转:43]"""    
	elif (Menu == 90):
		say = """（装置运转了一下，又停下来了，过一会儿再试吧。）

[结束:0]"""
	elif (Menu == 9):
		map = SEnvir.GetMap(473)
		if (map.PlayerCount < 1):
			PlayerSetV(Sender,BV_NQ_MAIN,160)
			Sender.TeleportByMapIndex(473,62,68)
			PlayerSetV(Sender,BV_MAP_TARGET,473)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			if map.MonsterCount > 0:
				map.ClearAllMonsters()
			ServerUtils.SpawnMonsters(473,100032,20,40,40,30)
			ServerUtils.SpawnMonsters(473,100033,20,40,40,30)
			ServerUtils.SpawnMonsters(473,100034,20,40,40,30)
			ServerUtils.SpawnMonsters(473,100035,20,40,40,30)
			ServerUtils.SpawnMonsters(473,100037,20,40,40,30)
			say = """进来了。。。
			啊~~~怎么这么多怪物。。。。"""
		else:
			say = """好像还是推不动石头，等一下再试试吧。
			
			[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==159):
			say = """（这就是无名老人提到过的机关装置吗？）
				
				[移动装置:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==160):
			say = """（这就是无名老人提到过的机关装置吗？）
				
				[移动装置:1]"""
		else:
			say = """（无名的力量。）
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(286,"OnClick",OnClick)
