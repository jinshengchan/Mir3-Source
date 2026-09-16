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
		say = """请你离开。
		
		我不想和红名交易。
		
		[离开:0]"""	
#跳转菜单1关于生锈配饰	
	elif(Menu == 1):	
		say = """清洁费是100万，但由于物品的使用年限太长，这个过程效果不是很好。

		[生锈师承戒指:11]
		[生锈龙马戒指:12]
		[生锈青云戒指:13]
		[生锈破荒项链:14]
		[生锈魔云项链:15]
		[生锈定心项链:16]
		[生锈金棱手镯:17]
		[生锈思过手镯:18]
		[生锈世尊手镯:19]"""
#生锈师承戒指
	elif(Menu == 11):
		say = """选择你所需要兑换的元素戒指
		
		[师承戒指（火）:111]      [师承戒指（冰）:112]
		[师承戒指（雷）:113]      [师承戒指（风）:114]
		[师承戒指（神圣）:115]    [师承戒指（暗黑）:116]
		"""
	elif(Menu == 111):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈师承戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈师承戒指",1)
			Sender.GiveItem("师承戒指（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 112):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈师承戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈师承戒指",1)
			Sender.GiveItem("师承戒指（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 113):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈师承戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈师承戒指",1)
			Sender.GiveItem("师承戒指（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 114):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈师承戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈师承戒指",1)
			Sender.GiveItem("师承戒指（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 115):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈师承戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈师承戒指",1)
			Sender.GiveItem("师承戒指（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 116):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈师承戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈师承戒指",1)
			Sender.GiveItem("师承戒指（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 117):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈师承戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈师承戒指",1)
			Sender.GiveItem("师承戒指（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈龙马戒指
	elif(Menu == 12):
		say = """选择你所需要兑换的元素戒指
		
		[龙马戒指（火）:121]      [龙马戒指（冰）:122]
		[龙马戒指（雷）:123]      [龙马戒指（风）:124]
		"""
	elif(Menu == 121):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈龙马戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈龙马戒指",1)
			Sender.GiveItem("龙马戒指（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 122):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈龙马戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈龙马戒指",1)
			Sender.GiveItem("龙马戒指（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 123):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈龙马戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈龙马戒指",1)
			Sender.GiveItem("龙马戒指（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 124):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈龙马戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈龙马戒指",1)
			Sender.GiveItem("龙马戒指（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 125):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈龙马戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈龙马戒指",1)
			Sender.GiveItem("龙马戒指（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 126):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈龙马戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈龙马戒指",1)
			Sender.GiveItem("龙马戒指（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 127):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈龙马戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈龙马戒指",1)
			Sender.GiveItem("龙马戒指（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈青云戒指
	elif(Menu == 13):
		say = """选择你所需要兑换的元素戒指
		
		[青云戒指（神圣）:135]    [青云戒指（暗黑）:136]
		[青云戒指（幻影）:137]
		"""
	elif(Menu == 131):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈青云戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈青云戒指",1)
			Sender.GiveItem("青云戒指（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 132):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈青云戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈青云戒指",1)
			Sender.GiveItem("青云戒指（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 133):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈青云戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈青云戒指",1)
			Sender.GiveItem("青云戒指（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 134):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈青云戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈青云戒指",1)
			Sender.GiveItem("青云戒指（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 135):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈青云戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈青云戒指",1)
			Sender.GiveItem("青云戒指（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 136):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈青云戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈青云戒指",1)
			Sender.GiveItem("青云戒指（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 137):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈青云戒指") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈青云戒指",1)
			Sender.GiveItem("青云戒指（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈破荒项链
	elif(Menu == 14):
		say = """选择你所需要兑换的元素戒指
		
		[破荒项链（火）:141]      [破荒项链（冰）:142]
		[破荒项链（雷）:143]      [破荒项链（风）:144]
		[破荒项链（神圣）:145]    [破荒项链（暗黑）:146]
		"""
	elif(Menu == 141):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈破荒项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈破荒项链",1)
			Sender.GiveItem("破荒项链（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 142):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈破荒项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈破荒项链",1)
			Sender.GiveItem("破荒项链（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 143):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈破荒项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈破荒项链",1)
			Sender.GiveItem("破荒项链（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 144):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈破荒项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈破荒项链",1)
			Sender.GiveItem("破荒项链（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 145):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈破荒项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈破荒项链",1)
			Sender.GiveItem("破荒项链（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 146):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈破荒项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈破荒项链",1)
			Sender.GiveItem("破荒项链（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 147):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈破荒项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈破荒项链",1)
			Sender.GiveItem("破荒项链（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈魔云项链
	elif(Menu == 15):
		say = """选择你所需要兑换的元素戒指
		
		[魔云项链（火）:151]      [魔云项链（冰）:152]
		[魔云项链（雷）:153]      [魔云项链（风）:154]
		"""
	elif(Menu == 151):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈魔云项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈魔云项链",1)
			Sender.GiveItem("魔云项链（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 152):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈魔云项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈魔云项链",1)
			Sender.GiveItem("魔云项链（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 153):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈魔云项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈魔云项链",1)
			Sender.GiveItem("魔云项链（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 154):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈魔云项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈魔云项链",1)
			Sender.GiveItem("魔云项链（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 155):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈魔云项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈魔云项链",1)
			Sender.GiveItem("魔云项链（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 156):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈魔云项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈魔云项链",1)
			Sender.GiveItem("魔云项链（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 157):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈魔云项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈魔云项链",1)
			Sender.GiveItem("魔云项链（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈定心项链
	elif(Menu == 16):
		say = """选择你所需要兑换的元素戒指
		
		[定心项链（神圣）:165]    [定心项链（暗黑）:166]
		[定心项链（幻影）:167]
		"""
	elif(Menu == 161):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈定心项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈定心项链",1)
			Sender.GiveItem("定心项链（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 162):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈定心项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈定心项链",1)
			Sender.GiveItem("定心项链（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 163):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈定心项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈定心项链",1)
			Sender.GiveItem("定心项链（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 164):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈定心项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈定心项链",1)
			Sender.GiveItem("定心项链（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 165):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈定心项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈定心项链",1)
			Sender.GiveItem("定心项链（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 166):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈定心项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈定心项链",1)
			Sender.GiveItem("定心项链（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 167):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈定心项链") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈定心项链",1)
			Sender.GiveItem("定心项链（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈金棱手镯
	elif(Menu == 17):
		say = """选择你所需要兑换的元素戒指
		
		[金棱手镯（火）:171]      [金棱手镯（冰）:172]
		[金棱手镯（雷）:173]      [金棱手镯（风）:174]
		[金棱手镯（神圣）:175]    [金棱手镯（暗黑）:176]
		"""
	elif(Menu == 171):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈金棱手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈金棱手镯",1)
			Sender.GiveItem("金棱手镯（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 172):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈金棱手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈金棱手镯",1)
			Sender.GiveItem("金棱手镯（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 173):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈金棱手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈金棱手镯",1)
			Sender.GiveItem("金棱手镯（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 174):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈金棱手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈金棱手镯",1)
			Sender.GiveItem("金棱手镯（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 175):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈金棱手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈金棱手镯",1)
			Sender.GiveItem("金棱手镯（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 176):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈金棱手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈金棱手镯",1)
			Sender.GiveItem("金棱手镯（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 177):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈金棱手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈金棱手镯",1)
			Sender.GiveItem("金棱手镯（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈思过手镯
	elif(Menu == 18):
		say = """选择你所需要兑换的元素戒指
		
		[思过手镯（火）:181]      [思过手镯（冰）:182]
		[思过手镯（雷）:183]      [思过手镯（风）:184]
		"""
	elif(Menu == 181):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈思过手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈思过手镯",1)
			Sender.GiveItem("思过手镯（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 182):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈思过手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈思过手镯",1)
			Sender.GiveItem("思过手镯（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 183):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈思过手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈思过手镯",1)
			Sender.GiveItem("思过手镯（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 184):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈思过手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈思过手镯",1)
			Sender.GiveItem("思过手镯（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 185):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈思过手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈思过手镯",1)
			Sender.GiveItem("思过手镯（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 186):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈思过手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈思过手镯",1)
			Sender.GiveItem("思过手镯（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 187):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈思过手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈思过手镯",1)
			Sender.GiveItem("思过手镯（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#生锈世尊手镯
	elif(Menu == 19):
		say = """选择你所需要兑换的元素戒指
		
		[世尊手镯（神圣）:195]    [世尊手镯（暗黑）:196]
		[世尊手镯（幻影）:197]
		"""
	elif(Menu == 191):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈世尊手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈世尊手镯",1)
			Sender.GiveItem("世尊手镯（火）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 192):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈世尊手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈世尊手镯",1)
			Sender.GiveItem("世尊手镯（冰）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 193):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈世尊手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈世尊手镯",1)
			Sender.GiveItem("世尊手镯（雷）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 194):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈世尊手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈世尊手镯",1)
			Sender.GiveItem("世尊手镯（风）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 195):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈世尊手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈世尊手镯",1)
			Sender.GiveItem("世尊手镯（神圣）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 196):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈世尊手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈世尊手镯",1)
			Sender.GiveItem("世尊手镯（暗黑）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
	elif(Menu == 197):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say= """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("生锈世尊手镯") < 1):
			say ="""你没有生锈的首饰。

			[离开:0]"""
		else:
#上面条件都达成，扣除费用和道具，给予道具		
			SubGold(Sender,1000000)
			Sender.TakeItem("生锈世尊手镯",1)
			Sender.GiveItem("世尊手镯（幻影）",1)
			say="""祝贺你，
			你的戒指在清理过程中幸存下来。

			[离开:0]"""
#跳转菜单2关于陈旧配饰
	elif(Menu == 2):
		say = """锻造费是2000万金币，5个生锈，7个陈旧，10个裂开。

		[日月戒指:21]
		[日月手镯:22]
		[日月项链:23]
		[天辉戒指:24]
		[天辉手镯:25]
		[天辉项链:26]
		[消魂戒指:27]
		[消魂手镯:28]
		[消魂项链:29]"""
	elif(Menu == 21):
		say = Refine(Sender,'日月戒指')
	elif(Menu == 22):
		say = Refine(Sender,'日月手镯')
	elif(Menu == 23):
		say = Refine(Sender,'日月项链')
	elif(Menu == 24):
		say = Refine(Sender,'天辉戒指')
	elif(Menu == 25):
		say = Refine(Sender,'天辉手镯')
	elif(Menu == 26):
		say = Refine(Sender,'天辉项链')
	elif(Menu == 27):
		say = Refine(Sender,'消魂戒指')
	elif(Menu == 28):
		say = Refine(Sender,'消魂手镯')
	elif(Menu == 29):
		say = Refine(Sender,'消魂项链')
#主菜单
	else:		
		say = """欢迎光临！

		[询问:1] 关于生锈配饰
		[询问:2] 关于陈旧配饰

		[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
#############################################################
###
###特殊精炼工艺要求判断
###
#############################################################	
def Refine(Sender,RefineName):
	list = RefineList[RefineName]
#判断金币
	if (Sender.Gold < list['Gold']):
			return """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""			
#判断包裹内是否有足够的材料		
	elif(list['Item']):
		for (k,v) in list['Item'].items():
			if (Sender.GetItemCount(k)<v):
				return """你的材料不足。
				请准备好足够的材料在来。

				[离开:0]"""
#如果材料达到要求，那么扣除材料	
	if (list['Item']):
		for (k,v) in list['Item'].items():
			Sender.TakeItem(k,v)
#扣除金币给予物品
	SubGold(Sender,list['Gold'])	
	Sender.GiveItem(RefineName,1)
	return """祝贺你，
	你的戒指锻造成功。

	[离开:0]"""	
#############################################################
###
###合成陈旧配饰条件
###合成需要的金币要求  Item需要的材料  
#############################################################		
RefineList={'日月戒指':{'Gold':20000000,'Item':{'生锈的日月戒指':10,'裂开的日月戒指':10,'陈旧的日月戒指':10},},
			'日月手镯':{'Gold':20000000,'Item':{'生锈的日月手镯':5,'裂开的日月手镯':7,'陈旧的日月手镯':10},},
			'日月项链':{'Gold':20000000,'Item':{'生锈的日月项链':5,'裂开的日月项链':7,'陈旧的日月项链':10},},
			'天辉戒指':{'Gold':20000000,'Item':{'生锈的天辉戒指':5,'裂开的天辉戒指':7,'陈旧的天辉戒指':10},},
			'天辉手镯':{'Gold':20000000,'Item':{'生锈的天辉手镯':5,'裂开的天辉手镯':7,'陈旧的天辉手镯':10},},
			'天辉项链':{'Gold':20000000,'Item':{'生锈的天辉项链':5,'裂开的天辉项链':7,'陈旧的天辉项链':10},},
			'消魂戒指':{'Gold':20000000,'Item':{'生锈的消魂戒指':5,'裂开的消魂戒指':7,'陈旧的消魂戒指':10},},
			'消魂手镯':{'Gold':20000000,'Item':{'生锈的消魂手镯':5,'裂开的消魂手镯':7,'陈旧的消魂手镯':10},},
			'消魂项链':{'Gold':20000000,'Item':{'生锈的消魂项链':5,'裂开的消魂项链':7,'陈旧的消魂项链':10},},			
			}


NpcEvent.add_listener(219,"OnClick",OnClick)
