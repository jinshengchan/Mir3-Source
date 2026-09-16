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
#红名判断
	if(Sender.Stats[Stat.PKPoint] > 199):
		str = """像你这种双手沾满鲜血的人，我是不会理会的。
		
		[关闭:0]"""	

        elif(Menu == 1):
		if (Sender.GameGold < 400):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,400)
			Sender.TeleportByMapIndex(1517,19,20)
			return
        elif(Menu == 2):
		if (Sender.GameGold < 400):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,400)
			Sender.TeleportByMapIndex(1518,19,20)
			return	
        elif(Menu == 3):
		if (Sender.GameGold < 400):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,400)
			Sender.TeleportByMapIndex(1519,19,20)
			return

#主菜单
	else:
		if Sender.Level < 60 : # 等级判断
			say  = """请你离开。
			你实力不够，没有达到60级，无法前往。
			
			[离开:0]"""
		else:
			say = """  你将被传送到一个有桃花盛开的地方，
相传那是一个很美丽的地方，但是那个地方有一群来自
森林深处的怪物把守。
			
[战士练级地图:1]     [道士练级地图:2]    [法师练级地图:3]  
			
<font color=\"0xff00ff00\">进入副本需要等级大于等于60级</font>
<font color=\"0xff00ff00\">进入400元宝门票费/次，练级地图不能挂机</font>
<font color=\"0xff00ff00\">副本对应职业进入，升级效率更高。</font>	
<font color=\"0xff00ff00\">副本开放时间：全天</font>	
<font color=\"0xff00ff00\">练级地图可以去到打宝地图，桃源圣殿有强悍BOSS</font>

			
			[放弃:0]"""


		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(349,"OnClick",OnClick)	