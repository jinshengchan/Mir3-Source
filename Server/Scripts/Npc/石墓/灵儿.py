# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
from Npc.商店列表 import *
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
		say = """我不愿意和你这样的人进行交易。
		
		[结束:0]"""	
#跳转菜单1戒指	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library里的NPCDialogType买卖类
		say = """你想买饰品？买什么？仔细挑选一下吧。
		
		[前一步:99]"""
#跳转菜单4修理				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为NPCDialogType里的修理类
		say = """那我给你修吧。你要修什么？
        
		[前一步:99]"""	
#跳转菜单5卖				
	elif (Menu == 5):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把不用的饰品卖给我。
		
		[前一步:99]"""
#主菜单
	else:
		say = """欢迎光临，你需要什么？

		[购买:1]饰品
		[出售:5]饰品
		[修理:4]饰品
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Library.ItemType里的首饰类
types =[ItemType.Necklace,ItemType.Ring,ItemType.Bracelet]
goods = collections.OrderedDict(shoushidiangoodslist)

NpcEvent.add_listener(308,"OnClick",OnClick)

