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
#粉碎物品获得初级碎片	
	if(Menu == 1):
		Dict['DialogType']= NPCDialogType.ItemFragment	
		say = """请给我看看你要分解的东西。
		我可以分解，武器，盔甲，头盔，项链，手镯，戒指和鞋子。

		普通物品会分解出初级碎片。

		高级物品将分解出中级碎片。

		[返回:99]
		[离开:0]"""
#合成中级碎片		
	elif(Menu == 2):
#判断需要的金币	
		if (Sender.Gold < 100000):
			say = """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("初级碎片") < 100):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("中级碎片",1)):
				SubGold(Sender,100000)
				Sender.TakeItem("初级碎片",100)
				say ="""你的材料合成成功。
			
				[继续:2]			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""				
#合成高级碎片		
	elif(Menu == 3):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say = """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("中级碎片") < 200):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("高级碎片",1)):
				SubGold(Sender,1000000)
				Sender.TakeItem("中级碎片",200)
				say ="""你的高级碎片合成成功。
			
				[继续:3]			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""

#合成超级碎片		
	elif(Menu == 4):
#判断需要的金币	
		if (Sender.Gold < 10000000):
			say = """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("高级碎片") < 50):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("超级碎片",1)):
				SubGold(Sender,10000000)
				Sender.TakeItem("高级碎片",50)
				say ="""你成功合成一颗超级碎片。
			
				[继续:4]			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""						
	if (Menu == 5):
		say = """<font color=\"0xffff0000\">碎片合成武器修炼石，每次需要支付一定元宝</font>
		
	[武器修炼石初级:111]成功率增加2％ 需要20颗中级碎片 10元宝
	[武器修炼石高级:113]成功率增加5％  需要50颗中级碎片20元宝
	[武器修炼石稀世:115]成功率增加20％ 需要1颗高级碎片50元宝
		 
	[不兑换返回主页:99]                                  

		"""

	elif (Menu == 111):
		if (Sender.GameGold < 10):
			say= """世界上的事情没有免费的，我也要养家，下次不要忘了带够炼制费用。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("中级碎片") < 20):
			say ="""在可以证明你有得到我给你服务之前。请首先找到中级碎片物品。
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGameGold(Sender,10)
			Sender.TakeItem("中级碎片",20)
			Sender.GiveItem("初级武器修炼石",1)
			say = """炼制成功了，恭喜你。
			
				[继续:111]
			
				[离开:0]"""


	elif (Menu == 113):
		if (Sender.GameGold < 20):
			say= """世界上的事情没有免费的，我也要养家，下次不要忘了带够炼制费用。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("中级碎片") < 50):
			say ="""在可以证明你有得到我给你服务之前。请首先找到中级碎片物品。
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGameGold(Sender,20)
			Sender.TakeItem("中级碎片",50)
			Sender.GiveItem("高级武器修炼石",1)
			say = """炼制成功了，恭喜你。
			
				[继续:113]
			
				[离开:0]"""
	elif (Menu == 115):
		if (Sender.GameGold < 50):
			say= """世界上的事情没有免费的，我也要养家，下次不要忘了带够炼制费用。
			
			[结束:0]
			"""
		#判断是否有要求的道具
		elif(Sender.GetItemCount("高级碎片") < 1):
			say ="""在可以证明你有得到我给你服务之前。请首先找到高级碎片物品。
			
			[结束:0]
			"""
		else:
		#上面条件都达成，扣除费用和道具
			SubGameGold(Sender,50)
			Sender.TakeItem("高级碎片",1)
			Sender.GiveItem("稀世武器修炼石",1)
			say = """炼制成功了，恭喜你。
			
				[继续:115]
			
				[离开:0]"""
#主菜单		
	else:		
		say = """你好，欢迎。。。我该如何帮助你？

		[粉碎物品:1] :将物品粉碎，获得初级碎片。

		[合成中级碎片:2] :用100个初级碎片 +  10W金币= 1个中级碎片
		[合成高级碎片:3] :用200个中级碎片+100W金币 = 1个高级碎片
		[合成超级碎片:4] :用50个高级碎片+1000W金币 = 1个超级碎片

		[碎片合成武器修炼石:5]  武器修炼石可以提高武器炼制的几率

		[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	

NpcEvent.add_listener(143,"OnClick",OnClick)