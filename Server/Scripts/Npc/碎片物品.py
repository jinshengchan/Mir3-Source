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
		if (Sender.Gold < 20000):
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
				SubGold(Sender,20000)
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
		if (Sender.Gold < 50000):
			say = """你没有足够的金币。
			当你拥有足够的金币时再来。

			[离开:0]"""
#判断是否有要求的道具			
		elif(Sender.GetItemCount("中级碎片") < 25):
			say ="""你的材料不足。
			请准备好足够的材料在来。

			[离开:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成		
			if (Sender.GiveItem("高级碎片",1)):
				SubGold(Sender,50000)
				Sender.TakeItem("中级碎片",25)
				say ="""你的材料合成成功。
			
				[继续:3]			
				[离开:0]"""
			else:
				say ="""你的包裹没有空格。

				[离开:0]"""
						
#主菜单		
	else:		
		say = """你好，欢迎。。。我该如何帮助你？

		[粉碎物品:1] :将物品粉碎，获得初级碎片。

		[合成中级碎片:2] :用100个初级碎片 + 20,000金币= 1个中级碎片
		[合成高级碎片:3] :用25个中级碎片 + 50,000金币 = 1个高级碎片

		[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict	
	
