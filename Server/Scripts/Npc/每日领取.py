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
import Server.Envir.SEnvir as SEnvir
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
import random
from Player.泡点 import *
# 下面两个import用于调用其他NPC
from Utils import ServerUtils
from Npc import *
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
	say="OK"
	Dict={}

#红名判断
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[关闭:0]"""
	elif (Menu == 2):
		if PlayerGetV(Sender,GV_MEIRILIBAO_ONOFF) == 0:
			PlayerSetV(Sender,GV_MEIRILIBAO_ONOFF, 1)
			GiveHuntGold(Sender,1000)
			Sender.GiveItem("双倍经验卷（绑定）",2)
			say = """
				领取成功
				
				得到 1000赏金，2个双倍经验卷
				
				[返回:99]
				"""
		else:
			say = """
			今天已经领过了
			
			[离开:0]
			"""




#主菜单

	else:
		if Sender.Level < 22 : # 等级判断
			say  = """请你离开。
			你需要等级达到22级才能参加每日福利活动。
			
			[离开:0]"""

		elif Sender.Level > 65 : # 等级判断
			say  = """你的能力已经可以独自面对一切了。
			65级后不需要领取福利。
			
			[离开:99]""" 

		else:
			say = """欢迎来到 <font color=\"0xff00ff00\">逍遥传奇3</font>, <font color=\"0xff00ff00\">QQ群：123456789</font> 
        
  
    <font color=\"0xff00ccff\">玩家福利，每天均可领取：1000赏金、多倍经验卷</font>

    <font color=0xffFF00FF>注意包裹至少预留2个以上空格</font>

                    [每日领取福利:2]
 
                    [离开:0]

		"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(226,"OnClick",OnClick)