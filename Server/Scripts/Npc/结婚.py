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
#结婚	
	if (Menu == 1):
		say = """请面对你的伴侣......
			当你准备好时，请告诉我。
			为了一次成功的婚姻，我将向你们收取50万金币。
		
			[继续:11]
		
			[返回:99]"""
	elif(Menu == 11):
		say = """请面对你的伴侣......
			当你准备好时，请告诉我。
			为了一次成功的婚姻，我将向你们收取50万金币。
			
			[继续:12]
		
			[返回:99]"""
	elif(Menu == 12):
##结婚的等级要求和金币要求，如需修改，记得修改上面的对话内容
		Sender.MarriageRequest(22,500000);   
		return
	elif(Menu == 2):
		say = """你确定要离婚吗？
			它将花费你100万金币。
		
			[继续:21]
		
			[返回:99]"""
	elif(Menu == 21):
		if(Sender.Character.Partner):
			if (Sender.Gold < 1000000):
				say = """你没有足够的金币来使用此服务。
				
				[离开:0]"""
			else:
##离婚扣除的金币			
				SubGold(Sender,1000000)
				Sender.MarriageLeave()
				return
		else:
		    say = """我无法为你提供所要求的服务。
			你没有结婚。
			
			[离开:0]"""
	elif(Menu == 3):
		say = """你确定要取下结婚戒指吗？
			它将花费你20万金币。
		
			[移除戒指:31]
		
			[离开:0]"""
	elif(Menu == 31):
		if (Sender.Gold < 200000):
			say = """你没有足够的金币来使用此服务。
				
				[离开:0]"""
##判断是否有结婚戒指
		elif(Sender.Equipment[int(EquipmentSlot.RingL)]):
			if ((Sender.Equipment[int(EquipmentSlot.RingL)].Flags & UserItemFlags.Marriage) == UserItemFlags.Marriage):
##移除戒指需要扣除的金币
				SubGold(Sender,200000)
				Sender.MarriageRemoveRing()
				return
			else:
				say = """我无法为你提供所要求的服务。
					你现在没有结婚戒指。
			
					[离开:0]"""	
		else:
		    say = """我无法为你提供所要求的服务。
			你现在没有结婚戒指。
			
			[离开:0]"""		
	elif(Menu == 4):
		if(Sender.Character.Partner):
			Dict['DialogType'] = NPCDialogType.WeddingRing  #类型为Library里的NPCDialogType结婚戒指类
			say = """我知道你有一枚戒指，作为结婚戒指。
				请给我看看你想用的戒指。
		
				[返回:99]
		
				[离开:0]"""
##判断是否有结婚戒指				
			if(Sender.Equipment[int(EquipmentSlot.RingL)]):
				if ((Sender.Equipment[int(EquipmentSlot.RingL)].Flags & UserItemFlags.Marriage) == UserItemFlags.Marriage):
					Dict['DialogType'] = NPCDialogType.None
					say ="""我无法为你提供所要求的服务。
					你已经有一个结婚戒指。
					
					[离开:0]"""						
		else:
		    say = """我无法为你提供所要求的服务。
			你没有结婚。
			
			[离开:0]"""	
	else:
		say = """你好，需要我如何帮助你呢？
		
			[申请结婚:1]
			[申请离婚:2]
			[摘下结婚戒指:3]
			[制作结婚戒指:4]
		
			[离开:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict		
	
NpcEvent.add_listener(164,"OnClick",OnClick)	