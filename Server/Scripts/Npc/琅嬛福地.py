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
REFINE_REQUIREMENTS={'旋风墙（秘籍）':{'GameGold':500,'Item':{'点化石':1,'高级技能残片':150,'旋风墙':1},},
			'君临步（秘籍）':{'GameGold':500,'Item':{'点化石':1,'高级技能残片':150,'君临步':1},},
			'养生术（秘籍）':{'GameGold':500,'Item':{'点化石':1,'高级技能残片':150,'养生术':1},},
			'焰魔召唤术（秘籍）':{'GameGold':500,'Item':{'点化石':1,'高级技能残片':150,'焰魔召唤术':1},},
			'风之闪避（秘籍）':{'GameGold':500,'Item':{'点化石':1,'高级技能残片':150,'风之闪避':1},},
			'分身术（秘籍）':{'GameGold':1000,'Item':{'点化石':1,'高级技能残片':300,'分身术':1},},
			'集中（秘籍）':{'GameGold':1000,'Item':{'点化石':1,'高级技能残片':300,'集中':1},},
			'移花接木（秘籍）':{'GameGold':1000,'Item':{'点化石':1,'高级技能残片':300,'移花接木':1},},
			'快刀斩马（秘籍）':{'GameGold':1000,'Item':{'点化石':1,'高级技能残片':300,'快刀斩马':1},},
			'魔焰强解术（秘籍）':{'GameGold':1000,'Item':{'点化石':1,'高级技能残片':300,'魔焰强解术':1},},
			'百花盛开（秘籍）':{'GameGold':1000,'Item':{'点化石':1,'高级技能残片':300,'百花盛开':1},}}



def OnClick(args):
	Self = args[0]
	Sender = args[1]
	Menu = args[2]
	Dict={}
	
	if (Menu == 1):
		say = """部分高级功法，我可以协助你完成修复。
		以下高级功法需要150个高级技能残片，500元宝手续费，
		1个点化石，对应技能未鉴定技能书一本

		[旋风墙:11]  [君临步:12]  [焰魔召唤术:13]  [风之闪避:14]  [养生术:15]

		以下高级功法需要300个高级技能残片，1000元宝手续费，
		1个点化石。对应技能未鉴定技能书一本		      

		[分身术:21] [快刀斩马:22] [魔焰强解术:23] [百花盛开:24] [集中:25] [移花接木:26]   

		 

		[关闭:99]"""
		
	elif(Menu == 11):
		say = Refine(Sender,'旋风墙（秘籍）')
	elif(Menu == 12):
		say = Refine(Sender,'君临步（秘籍）')
	elif(Menu == 13):
		say = Refine(Sender,'焰魔召唤术（秘籍）')
	elif(Menu == 14):
		say = Refine(Sender,'风之闪避（秘籍）')
	elif(Menu == 15):
		say = Refine(Sender,'养生术（秘籍）')

	elif(Menu == 21):
		say = Refine(Sender,'分身术（秘籍）')
	elif(Menu == 22):
		say = Refine(Sender,'快刀斩马（秘籍）')
	elif(Menu == 23):
		say = Refine(Sender,'魔焰强解术（秘籍）')
	elif(Menu == 24):
		say = Refine(Sender,'百花盛开（秘籍）')
	elif(Menu == 25):
		say = Refine(Sender,'集中（秘籍）')
	elif(Menu == 26):
		say = Refine(Sender,'移花接木（秘籍）')

				
	elif (Menu == 2):
		say = """部分稀世功法，我可以协助你完成修复。
		以下稀世功法需要200个稀世技能残片，1000元宝手续费，
        1个点化石。
		
		[分身术:50]             [快刀斩马:51]

		[魔焰强解术:52]      [风之闪避:53]
		
		[关闭:99]"""
		
	elif(Menu == 50):
		say = Refine(Sender,'分身术（秘籍）')
	elif(Menu == 51):
		say = Refine(Sender,'快刀斩马（秘籍）')
	elif(Menu == 52):
		say = Refine(Sender,'魔焰强解术（秘籍）')
	elif(Menu == 53):
		say = Refine(Sender,'风之闪避（秘籍）')

	elif (Menu == 4):
		say = """如果你给我列表上的技能书
		我会给你一些高级技能书残片		

		<font color=0xff7fff00>以下技能书每本可兑换 5 张残片</font>

		[铁布衫:100][焰天火雨:101][妙影无踪:102][狂涛涌泉:103]

		[破血狂杀:104][凝血离魂:105][阴阳法环:106][最后抵抗:107]

		<font color=0xff7fff00>以下技能书每本可兑换 10 张残片</font>

		[旋风墙:110]  [君临步:111]  [焰魔召唤术:112]  [风之闪避:113]  [养生术:114]

		<font color=0xff7fff00>以下技能书每本可兑换 15 张残片</font>

		[分身术:120][快刀斩马:121][魔焰强解术:122][百花盛开:123][集中:124][移花接木:125]  

		     

		[关闭:0]"""
#兑换10高级技能书碎片
	elif(Menu == 100):
#判断是否有要求的道具			
		if(Sender.GetItemCount("铁布衫") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("铁布衫",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:100]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 101):
#判断是否有要求的道具			
		if(Sender.GetItemCount("焰天火雨") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("焰天火雨",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:101]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 102):
#判断是否有要求的道具			
		if(Sender.GetItemCount("妙影无踪") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("妙影无踪",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:102]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 103):
#判断是否有要求的道具			
		if(Sender.GetItemCount("狂涛涌泉") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("狂涛涌泉",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:103]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 104):
#判断是否有要求的道具			
		if(Sender.GetItemCount("破血狂杀") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("破血狂杀",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:104]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 105):
#判断是否有要求的道具			
		if(Sender.GetItemCount("凝血离魂") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("凝血离魂",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:105]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 106):
#判断是否有要求的道具			
		if(Sender.GetItemCount("阴阳法环") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("阴阳法环",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:106]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 107):
#判断是否有要求的道具			
		if(Sender.GetItemCount("最后抵抗") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",5)):
				Sender.TakeItem("最后抵抗",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:107]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 

#兑换10张高级技能残片
	elif(Menu == 110):
#判断是否有要求的道具			
		if(Sender.GetItemCount("旋风墙") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",10)):
				Sender.TakeItem("旋风墙",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:110]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 111):
#判断是否有要求的道具			
		if(Sender.GetItemCount("君临步") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",10)):
				Sender.TakeItem("君临步",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:111]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 112):
#判断是否有要求的道具			
		if(Sender.GetItemCount("焰魔召唤术") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",10)):
				Sender.TakeItem("焰魔召唤术",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:112]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 113):
#判断是否有要求的道具			
		if(Sender.GetItemCount("风之闪避") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",10)):
				Sender.TakeItem("风之闪避",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:113]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 114):
#判断是否有要求的道具			
		if(Sender.GetItemCount("养生术") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",10)):
				Sender.TakeItem("养生术",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:114]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 

#兑换15高级技能书碎片
	elif(Menu == 120):
#判断是否有要求的道具			
		if(Sender.GetItemCount("分身术") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",15)):
				Sender.TakeItem("分身术",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:120]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 121):
#判断是否有要求的道具			
		if(Sender.GetItemCount("快刀斩马") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",15)):
				Sender.TakeItem("快刀斩马",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:121]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 122):
#判断是否有要求的道具			
		if(Sender.GetItemCount("魔焰强解术") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",15)):
				Sender.TakeItem("魔焰强解术",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:122]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 123):
#判断是否有要求的道具			
		if(Sender.GetItemCount("百花盛开") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",15)):
				Sender.TakeItem("百花盛开",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:123]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 124):
#判断是否有要求的道具			
		if(Sender.GetItemCount("集中") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",15)):
				Sender.TakeItem("集中",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:124]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 
	elif(Menu == 125):
#判断是否有要求的道具			
		if(Sender.GetItemCount("移花接木") < 1):
			say ="""你没有我需要的技能书。

			[返回:99]"""
		else:
			if (Sender.GiveItem("高级技能残片",15)):
				Sender.TakeItem("移花接木",1)
				say ="""你的技能书已经成功分解成残片。
			
				[继续兑换:125]"""
			else:
				say ="""你的包裹没有空格。
 
				[返回:99]""" 


		
#主菜单
	else:	
		say = """我是琅嬛福地的管理员，你需要了解什么？

		[获取高级技能书:1]	
		
		[获取稀世技能书:3]

		[高级技能书兑换残片:4]

		[稀世技能书兑换残片:5]
		
		[关闭:0]"""
		
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
		
def Refine(Sender,RefineName):
	requirements = REFINE_REQUIREMENTS[RefineName]

	if (Sender.GameGold < requirements['GameGold']):
			return """你没有足够的元宝。
			当你拥有足够的元宝时再来。

			[返回:99]"""		

	if(requirements['Item']):
		for m,n in requirements['Item'].items():
			if (Sender.GetItemCount(m)<n):
				return """你的材料不足。
				请准备好足够的材料再来。

				[返回:99]"""
	if (requirements['Item']):
		for m,n in requirements['Item'].items():
			Sender.TakeItem(m,n)
	SubGameGold(Sender,requirements['GameGold'])	
	Sender.GiveItem(RefineName,1)
	return """祝贺你，
	你的技能书修复成功。

	[返回:99]"""	

	
NpcEvent.add_listener(378,"OnClick",OnClick)
