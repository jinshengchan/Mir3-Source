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
import collections
import NpcEvent
import Server

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
	bg = {}
	font={}
	Dict={}	
	
	if (Menu == 1):
		say = """如果你给我列表上的装备
		我会给你很好的价格		

		<font color=0xff7fff00>拾元宝回收区</font>

		[武圣之戒:20][六棱戒:21][紫金环:22][毁灭魔链:23][流星项链:24][英雄手套:25]
		[破坏项链:26][气血项链:27][虚空道环:28][天机戒指:30][乾坤一气:31]		
		[五行神镜:33][昏暗风印:34][七彩金环:35][心魔戒指:36][怨恨项链:32]

		<font color=0xff7fff00>贰拾元宝回收区</font>

		[霹雷:39][嗜魂法杖:40][龙纹剑:41][死神双剑:42]100元宝

		<font color=0xff7fff00>伍拾元宝回收区</font>

		[屠龙:54][逍遥扇:55][铁轮:56][天命:57] 200元宝

		<font color=0xff7fff00>陆拾元宝回收区</font>

		[天神法杖:72][破山剑:73][泰轮拂尘:74] [锋翼剑:75] 500元宝

		<font color=0xff7fff00>伍仟元宝回收区</font>

		[麻痹戒指:100][护身戒指:101][复活戒指:102][隐身戒指:103][技巧项链:104]            
		[传送戒指:105][防御戒指:106][火焰戒指:107][神力戒指:108][探测项链:109]


		"""

#兑换5元宝
	elif(Menu == 10):
#判断是否有要求的道具			
		if(Sender.GetItemCount("旭日戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("旭日戒指",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:10]
			[离开:0]"""
	elif(Menu == 11):
#判断是否有要求的道具			
		if(Sender.GetItemCount("登天手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("登天手镯",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:11]
			[离开:0]"""

	elif(Menu == 12):
#判断是否有要求的道具			
		if(Sender.GetItemCount("霸王项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("霸王项链",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:12]
			[离开:0]"""
	elif(Menu == 13):
#判断是否有要求的道具			
		if(Sender.GetItemCount("三桓戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("三桓戒指",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:13]
			[离开:0]"""
	elif(Menu == 14):
#判断是否有要求的道具			
		if(Sender.GetItemCount("云龙手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("云龙手镯",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:14]
			[离开:0]"""
	elif(Menu == 15):
#判断是否有要求的道具			
		if(Sender.GetItemCount("避难项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("避难项链",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:15]
			[离开:0]"""
	elif(Menu == 16):
#判断是否有要求的道具			
		if(Sender.GetItemCount("继承戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("继承戒指",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:16]
			[离开:0]"""
	elif(Menu == 17):
#判断是否有要求的道具			
		if(Sender.GetItemCount("至善手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("至善手镯",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:17]
			[离开:0]"""
	elif(Menu == 18):
#判断是否有要求的道具			
		if(Sender.GetItemCount("昆仑项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("昆仑项链",1)
			GiveGameGold(Sender,5)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5个元宝",MessageType.System)
			say="""恭喜您获得5个元宝
			
			[继续兑换:18]
			[离开:0]"""

#10元宝兑换
	elif(Menu == 20):
#判断是否有要求的道具			
		if(Sender.GetItemCount("武圣之戒") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("武圣之戒",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:20]
			[离开:0]"""


	elif(Menu == 21):
#判断是否有要求的道具			
		if(Sender.GetItemCount("六棱戒") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("六棱戒",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:21]
			[离开:0]"""
	elif(Menu == 22):
#判断是否有要求的道具			
		if(Sender.GetItemCount("紫金环") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("紫金环",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:22]
			[离开:0]"""

	elif(Menu == 23):
#判断是否有要求的道具			
		if(Sender.GetItemCount("毁灭魔链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("毁灭魔链",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:23]
			[离开:0]"""
	elif(Menu == 24):
#判断是否有要求的道具			
		if(Sender.GetItemCount("流星项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("流星项链",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:24]
			[离开:0]"""

	elif(Menu == 25):
#判断是否有要求的道具			
		if(Sender.GetItemCount("英雄手套") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("英雄手套",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:25]
			[离开:0]"""
	elif(Menu == 26):
#判断是否有要求的道具			
		if(Sender.GetItemCount("破坏项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("破坏项链",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:26]
			[离开:0]"""

	elif(Menu == 27):
#判断是否有要求的道具			
		if(Sender.GetItemCount("气血项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("破坏项链",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:27]
			[离开:0]"""

	elif(Menu == 28):
#判断是否有要求的道具			
		if(Sender.GetItemCount("虚空道环") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("虚空道环",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加10个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:28]
			[离开:0]"""
#20元宝兑换
	elif(Menu == 30):
#判断是否有要求的道具			
		if(Sender.GetItemCount("天机戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("天机戒指",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:30]
			[离开:0]"""
	elif(Menu == 31):
#判断是否有要求的道具			
		if(Sender.GetItemCount("乾坤一气") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("乾坤一气",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:31]
			[离开:0]"""

	elif(Menu == 32):
#判断是否有要求的道具			
		if(Sender.GetItemCount("怨恨项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("怨恨项链",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:32]
			[离开:0]"""

	elif(Menu == 33):
#判断是否有要求的道具			
		if(Sender.GetItemCount("五行神镜") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("五行神镜",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:33]
			[离开:0]"""


	elif(Menu == 34):
#判断是否有要求的道具			
		if(Sender.GetItemCount("昏暗风印") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("昏暗风印",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:34]
			[离开:0]"""

	elif(Menu == 35):
#判断是否有要求的道具			
		if(Sender.GetItemCount("七彩金环") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("七彩金环",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:35]
			[离开:0]"""

	elif(Menu == 36):
#判断是否有要求的道具			
		if(Sender.GetItemCount("心魔戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("心魔戒指",1)
			GiveGameGold(Sender,10)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得10个元宝
			
			[继续兑换:36]
			[离开:0]"""
	elif(Menu == 37):
#判断是否有要求的道具			
		if(Sender.GetItemCount("杀魔血刀手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("杀魔血刀手镯",1)
			GiveGameGold(Sender,20)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得20个元宝
			
			[继续兑换:37]
			[离开:0]"""

	elif(Menu == 38):
#判断是否有要求的道具			
		if(Sender.GetItemCount("杀魔血刀项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("杀魔血刀项链",1)
			GiveGameGold(Sender,20)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加20个元宝",MessageType.System)
			say="""恭喜您获得20个元宝
			
			[继续兑换:38]
			[离开:0]"""
#100元宝武器兑换
	elif(Menu == 39):
#判断是否有要求的道具			
		if(Sender.GetItemCount("霹雷") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("霹雷",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:39]
			[离开:0]"""

	elif(Menu == 40):
#判断是否有要求的道具			
		if(Sender.GetItemCount("嗜魂法杖") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("嗜魂法杖",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:40]
			[离开:0]"""
	elif(Menu == 41):
#判断是否有要求的道具			
		if(Sender.GetItemCount("龙纹剑") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("龙纹剑",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:41]
			[离开:0]"""
	elif(Menu == 42):
#判断是否有要求的道具			
		if(Sender.GetItemCount("死神双剑") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("死神双剑",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:42]
			[离开:0]"""



#50元宝兑换
	elif(Menu == 45):
#判断是否有要求的道具			
		if(Sender.GetItemCount("日月戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("日月戒指",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:45]
			[离开:0]"""

	elif(Menu == 46):
#判断是否有要求的道具			
		if(Sender.GetItemCount("日月手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("日月手镯",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:46]
			[离开:0]"""
	elif(Menu == 47):
#判断是否有要求的道具			
		if(Sender.GetItemCount("日月项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("日月项链",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:47]
			[离开:0]"""
	elif(Menu == 48):
#判断是否有要求的道具			
		if(Sender.GetItemCount("天辉戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("天辉戒指",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:48]
			[离开:0]"""
	elif(Menu == 49):
#判断是否有要求的道具			
		if(Sender.GetItemCount("天辉手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("天辉手镯",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:49]
			[离开:0]"""
	elif(Menu == 50):
#判断是否有要求的道具			
		if(Sender.GetItemCount("天辉项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("天辉项链",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:50]
			[离开:0]"""
	elif(Menu == 51):
#判断是否有要求的道具			
		if(Sender.GetItemCount("消魂戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("消魂戒指",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:51]
			[离开:0]"""
	elif(Menu == 52):
#判断是否有要求的道具			
		if(Sender.GetItemCount("消魂手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("消魂手镯",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:52]
			[离开:0]"""
	elif(Menu == 53):
#判断是否有要求的道具			
		if(Sender.GetItemCount("消魂项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("消魂项链",1)
			GiveGameGold(Sender,50)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加50个元宝",MessageType.System)
			say="""恭喜您获得50个元宝
			
			[继续兑换:53]
			[离开:0]"""
#200元宝武器兑换
	elif(Menu == 54):
#判断是否有要求的道具			
		if(Sender.GetItemCount("屠龙") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("屠龙",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加200个元宝",MessageType.System)
			say="""恭喜您获得200个元宝
			
			[继续兑换:54]
			[离开:0]"""
	elif(Menu == 55):
#判断是否有要求的道具			
		if(Sender.GetItemCount("逍遥扇") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("逍遥扇",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加200个元宝",MessageType.System)
			say="""恭喜您获得200个元宝
			
			[继续兑换:55]
			[离开:0]"""
	elif(Menu == 56):
#判断是否有要求的道具			
		if(Sender.GetItemCount("铁轮") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("铁轮",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加200个元宝",MessageType.System)
			say="""恭喜您获得200个元宝
			
			[继续兑换:56]
			[离开:0]"""
	elif(Menu == 57):
#判断是否有要求的道具			
		if(Sender.GetItemCount("天命") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("天命",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加200个元宝",MessageType.System)
			say="""恭喜您获得200个元宝
			
			[继续兑换:57]
			[离开:0]"""




#60元宝兑换区
	elif(Menu == 60):
#判断是否有要求的道具			
		if(Sender.GetItemCount("龙血戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("龙血戒指",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:60]
			[离开:0]"""
	elif(Menu == 61):
#判断是否有要求的道具			
		if(Sender.GetItemCount("龙血手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("龙血手镯",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:61]
			[离开:0]"""
	elif(Menu == 62):
#判断是否有要求的道具			
		if(Sender.GetItemCount("龙血项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("龙血项链",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:62]
			[离开:0]"""

	elif(Menu == 63):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵天链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵天链",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:63]
			[离开:0]"""

	elif(Menu == 64):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵天环") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵天环",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:64]
			[离开:0]"""
	elif(Menu == 65):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵天戒") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵天戒",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:65]
			[离开:0]"""
	elif(Menu == 66):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵魔链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵魔链",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:66]
			[离开:0]"""

	elif(Menu == 67):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵魔环") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵魔环",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:67]
			[离开:0]"""

	elif(Menu == 68):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵魔戒") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵魔戒",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:68]
			[离开:0]"""

	elif(Menu == 69):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵之月龙项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵之月龙项链",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:69]
			[离开:0]"""

	elif(Menu == 70):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵之月龙手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵之月龙手镯",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:70]
			[离开:0]"""
	elif(Menu == 61):
#判断是否有要求的道具			
		if(Sender.GetItemCount("玄灵之月龙戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("玄灵之月龙戒指",1)
			GiveGameGold(Sender,60)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加60个元宝",MessageType.System)
			say="""恭喜您获得60个元宝
			
			[继续兑换:71]
			[离开:0]"""
#500元宝武器兑换
	elif(Menu == 72):
#判断是否有要求的道具			
		if(Sender.GetItemCount("天神法杖") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("天神法杖",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:72]
			[离开:0]"""
	elif(Menu == 73):
#判断是否有要求的道具			
		if(Sender.GetItemCount("破山剑") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("破山剑",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:73]
			[离开:0]"""
	elif(Menu == 74):
#判断是否有要求的道具			
		if(Sender.GetItemCount("泰轮拂尘") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("泰轮拂尘",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:74]
			[离开:0]"""
	elif(Menu == 75):
#判断是否有要求的道具			
		if(Sender.GetItemCount("锋翼剑") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("锋翼剑",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:75]
			[离开:0]"""



#100元宝兑换
	elif(Menu == 80):
#判断是否有要求的道具			
		if(Sender.GetItemCount("虎影戒") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("虎影戒",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:80]
			[离开:0]"""
	elif(Menu == 81):
#判断是否有要求的道具			
		if(Sender.GetItemCount("永柳戒") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("永柳戒",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:81]
			[离开:0]"""
	elif(Menu == 82):
#判断是否有要求的道具			
		if(Sender.GetItemCount("咒恶戒") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("咒恶戒",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:82]
			[离开:0]"""
	elif(Menu == 83):
#判断是否有要求的道具			
		if(Sender.GetItemCount("神魔手镯") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("神魔手镯",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:83]
			[离开:0]"""
	elif(Menu == 84):
#判断是否有要求的道具			
		if(Sender.GetItemCount("神魔项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("神魔项链",1)
			GiveGameGold(Sender,100)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加100个元宝",MessageType.System)
			say="""恭喜您获得100个元宝
			
			[继续兑换:84]
			[离开:0]"""
#600元宝武器兑换
	elif(Menu == 85):
#判断是否有要求的道具			
		if(Sender.GetItemCount("天狼刀") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("天狼刀",1)
			GiveGameGold(Sender,600)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加600个元宝",MessageType.System)
			say="""恭喜您获得600个元宝
			
			[继续兑换:85]
			[离开:0]"""
	elif(Menu == 86):
#判断是否有要求的道具			
		if(Sender.GetItemCount("阴阳刀") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("阴阳刀",1)
			GiveGameGold(Sender,600)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加600个元宝",MessageType.System)
			say="""恭喜您获得600个元宝
			
			[继续兑换:86]
			[离开:0]"""
	elif(Menu == 87):
#判断是否有要求的道具			
		if(Sender.GetItemCount("拐杖") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("拐杖",1)
			GiveGameGold(Sender,600)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加600个元宝",MessageType.System)
			say="""恭喜您获得600个元宝
			
			[继续兑换:87]
			[离开:0]"""
#200元宝兑换
	elif(Menu == 88):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃之夭夭") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃之夭夭",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加200个元宝",MessageType.System)
			say="""恭喜您获得200个元宝
			
			[继续兑换:88]
			[离开:0]"""
	elif(Menu == 89):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃之灼灼") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃之灼灼",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加200个元宝",MessageType.System)
			say="""恭喜您获得200个元宝
			
			[继续兑换:89]
			[离开:0]"""
	elif(Menu == 90):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源之心") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源之心",1)
			GiveGameGold(Sender,200)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加200个元宝",MessageType.System)
			say="""恭喜您获得200个元宝
			
			[继续兑换:90]
			[离开:0]"""
#500元宝装备兑换
	elif(Menu == 91):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源仙甲（男）") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源仙甲（男）",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:90]
			[离开:0]"""
	elif(Menu == 92):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源仙甲（女）") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源仙甲（女）",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:92]
			[离开:0]"""

	elif(Menu == 93):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源盔") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源盔",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:93]
			[离开:0]"""
	elif(Menu == 94):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源靴") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源靴",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加500个元宝",MessageType.System)
			say="""恭喜您获得500个元宝
			
			[继续兑换:94]
			[离开:0]"""
#1000元宝武器兑换
	elif(Menu == 95):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源虎翼刀") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源虎翼刀",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加1000个元宝",MessageType.System)
			say="""恭喜您获得1000个元宝
			
			[继续兑换:95]
			[离开:0]"""
	elif(Menu == 96):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源曜灵杖") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源曜灵杖",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加1000个元宝",MessageType.System)
			say="""恭喜您获得1000个元宝
			
			[继续兑换:96]
			[离开:0]"""
	elif(Menu == 97):
#判断是否有要求的道具			
		if(Sender.GetItemCount("桃源三焰扇") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("桃源三焰扇",1)
			GiveGameGold(Sender,500)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加1000个元宝",MessageType.System)
			say="""恭喜您获得1000个元宝
			
			[继续兑换:97]
			[离开:0]"""
#5000元宝特戒兑换
	elif(Menu == 100):
#判断是否有要求的道具			
		if(Sender.GetItemCount("麻痹戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("麻痹戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:100]
			[离开:0]"""
	elif(Menu == 101):
#判断是否有要求的道具			
		if(Sender.GetItemCount("护身戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("护身戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:101]
			[离开:0]"""

	elif(Menu == 102):
#判断是否有要求的道具			
		if(Sender.GetItemCount("复活戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("复活戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:102]
			[离开:0]"""

	elif(Menu == 103):
#判断是否有要求的道具			
		if(Sender.GetItemCount("隐身戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("隐身戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:103]
			[离开:0]"""

	elif(Menu == 104):
#判断是否有要求的道具			
		if(Sender.GetItemCount("技巧项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("技巧项链",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:104]
			[离开:0]"""

	elif(Menu == 105):
#判断是否有要求的道具			
		if(Sender.GetItemCount("传送戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("传送戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:105]
			[离开:0]"""

	elif(Menu == 106):
#判断是否有要求的道具			
		if(Sender.GetItemCount("防御戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("防御戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:106]
			[离开:0]"""


	elif(Menu == 107):
#判断是否有要求的道具			
		if(Sender.GetItemCount("火焰戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("火焰戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:107]
			[离开:0]"""


	elif(Menu == 108):
#判断是否有要求的道具			
		if(Sender.GetItemCount("神力戒指") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("神力戒指",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:108]
			[离开:0]"""

	elif(Menu == 109):
#判断是否有要求的道具			
		if(Sender.GetItemCount("探测项链") < 1):
			say ="""你没有我要的装备，请离开。

			[离开:0]"""	
		else:
#如果有装备，扣除物品，给与元宝
			Sender.TakeItem("探测项链",1)
			GiveGameGold(Sender,5000)
			Sender.Connection.ReceiveChat("装备兑换成功！你已增加5000个元宝",MessageType.System)
			say="""恭喜您获得5000个元宝
			
			[继续兑换:109]
			[离开:0]"""

#主菜单
	else:
		
		say = """
		<font color=0xffFF3366>有钱走遍天下，无钱寸步难行</font>
		
		[兑换元宝:1] 大侠，拿出你珍藏的宝贝。
		
		[舍不得:0]"""
	
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(354,"OnClick",OnClick)
