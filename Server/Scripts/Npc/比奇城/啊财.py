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
#跳转菜单1
	if (Menu == 1):
		say = """请确保携带的金币在你兑换后不会超过上限金币。
		
		请确保包裹里有足够的地方放置兑换后的物品。
		
		[将1,000,000金币兑换成1根金条:22] 手续费:0 金币
		[将1根金条兑换成金币:23] 手续费:5,000 金币
		
		[将100,000,000金币兑换成1张钱票:11] 手续费:0 金币
		[将1张钱票兑换成金币:12] 手续费:5,000,000 金币
			
		[关闭:0]"""	
	elif(Menu == 11):
#判断需要的金币	
		if (Sender.Gold < 100000000):
			say = """你没有足够的金币。
			当你拥有足够的金币时再来。

			[关闭:0]"""
		else:
#上面条件达成，扣除金币，给与钱票
			if (Sender.GiveItem("钱票",1)):
				SubGold(Sender,100000000)		
				say = """你的物品制作成功。
						
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，请先整理下包裹。
				
				[关闭:0]"""	

	elif(Menu == 12):
#判断是否有要求的道具			
		if(Sender.GetItemCount("钱票") < 1):
			say = """你的背包里没有钱票。

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("钱票",1)	
			GiveGold(Sender,95000000)
			say ="""金币兑换成功。
					
			[关闭:0]"""				
	elif (Menu == 2):	
		say = """比奇商会的所有财务都由我来管理，
		像你这样的庶民看到账本里的数字会吓一跳的，呵呵呵。
			
		[关闭:0]"""	

	elif(Menu == 22):
#判断需要的金币	
		if (Sender.Gold < 1000000):
			say = """你没有足够的金币。
			当你拥有足够的金币时再来。

			[关闭:0]"""
		else:
#上面条件达成，扣除金币，给与钱票
			if (Sender.GiveItem("金条",1)):
				SubGold(Sender,1000000)		
				say = """你的物品制作成功。
						
				[关闭:0]"""	
			else:
				say = """你的背包没有空间，请先整理下包裹。
				
				[关闭:0]"""
	elif(Menu == 23):
#判断是否有要求的道具			
		if(Sender.GetItemCount("金条") < 1):
			say = """你的背包里没有金条。

			[关闭:0]"""	
		else:
#上面条件都达成，扣除费用和道具，执行合成
			Sender.TakeItem("金条",1)	
			GiveGold(Sender,995000)
			say = """金币兑换成功。
					
			[关闭:0]"""
#主菜单
	else:	
		say = """请问有什么事吗？
	
		[兑换:1] 钱币
		[交谈:2]
		
		[关闭:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(59,"OnClick",OnClick)