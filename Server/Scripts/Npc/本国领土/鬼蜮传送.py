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
		say = """像你这种双手沾满鲜血的人，我是不会理会的。
		
		[关闭:0]"""	

	elif(Menu == 1):
		if(Sender.GetItemCount("传送石") < 1):
			say = """无法传送到目的地，
			没有信物：一个“传送石”。

			[离开:0]"""
		elif (Sender.Level < 50):
			say = """你没有修炼到50级，无法传送。
			继续加油。

			[离开:0]"""
		elif (Sender.Gold < 1000000):
			say = """你没有足够的100万金币，无法传送。
			[离开:0]"""
		else:
			SubGold(Sender,1000000)
			Sender.TakeItem("传送石",1)
			Sender.TeleportByMapIndex(1018,33,758)
			return
        elif(Menu == 2):
		if (Sender.GameGold < 200):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,200)
			Sender.TeleportByMapIndex(1518,19,20)
			return	
        elif(Menu == 3):
		if (Sender.GameGold < 200):
			say = """你没有足够的元宝，无法传送。
				
				[关闭:0]"""	
		else:
			SubGameGold(Sender,200)
			Sender.TeleportByMapIndex(1519,19,20)
			return

#主菜单
	else:
		if Sender.Character.Rebirth < 1 : # 等级判断
			say  = """请你离开。
			你实力不够，现在还不能前往。
			
			[离开:0]"""
		else:
			say = """森林深处有奇怪的力量牵引着我
			
[我要去热带雨林:1]  
			
<font color=\"0xff00ff00\">进入鬼蜮地图需要等级1级转生，鬼蜮可以去异界幽灵船和桃花源</font>
<font color=\"0xff00ff00\">进入需要信物“传送石”，100万金币</font>
<font color=\"0xff00ff00\">鬼蜮地图可以获得“高级书籍残片”，可以兑换指定技能书</font>	


			
			[放弃:0]"""


		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
NpcEvent.add_listener(350,"OnClick",OnClick)	