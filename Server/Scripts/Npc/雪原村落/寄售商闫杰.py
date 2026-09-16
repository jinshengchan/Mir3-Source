# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
import Globals
import clr
clr.AddReference("Library")
from Library import *
import collections
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
#跳转菜单1寄售			
	if (Menu == 11):
		say = """你好，我是专门的寄售商人。在我这里，既可以寄售道具，也可以寄售金币，还能寄售账号，其中，寄售道具的交易货币是金币，上架费用为5000元金币，交易成功扣除5%税率；寄售金币和寄售账号的交易货币为赞助币，不抽取交易税率。你看看需要什么帮助。
	
		[道具金币寄售:1]
		[道具元宝寄售:5]
		[我的寄售:6]

		[金币交易行:2]
		[角色寄售行:3]
		[道具拍卖行:4]"""
	
	elif (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.MarketSearch   #类型为NPCDialogType里的寄售类
		say = """查看所有金币寄售的物品。
		
		[结束:0]"""
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.GoldTradingBusiness   #类型为NPCDialogType里的金币交易行
		say = """查看所有金币交易。
		
		[结束:0]"""
	elif (Menu == 3):
		say = """玩家，您好。
		我这里接受角色寄售，每次寄售收取10赞助币。
		说明：
		购买角色后，仅转移人物面板、背包、技能、马匹、忠诚度，
		其他金币、赞助币、仓库仍留存在原账号。
		购买角色的账号，不能有两个角色。
		交易完成后，赞助币直接到原售出账号，有角色的直接到背包；没有角色的，建立小号后到背包。
		
		
		[查看所有角色寄售:31]
		
		[结束:0]"""
	elif (Menu == 31):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.AccountConsignment    #类型为NPCDialogType里的账号寄售行
		say = """查看所有角色寄售。
		
		[结束:0]"""
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Auctions   #类型为NPCDialogType里的拍卖行
		say = """查看所有拍卖物品。
		
		[结束:0]"""
	elif (Menu == 5):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.GameGoldMarketSearch   #类型为NPCDialogType里的寄售类
		say = """查看所有元宝寄售的物品。
		
		[结束:0]"""
	elif (Menu == 6):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.MyMarket   #类型为NPCDialogType里的我的寄售类
		say = """我的寄售物品。
		
		[结束:0]"""
	elif (Menu == 12):
		say = """每个人最多可以寄售20件物品。
			
		[关闭:0]"""		
#主菜单
	else:	
		say = """欢迎光临，你有什么事情？
	
		[寄售商店:11] 
		[交谈:12]
		
		[关闭:0]"""
  
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Enums里的普通类			
types =[ItemType.Nothing]

NpcEvent.add_listener(327,"OnClick",OnClick)