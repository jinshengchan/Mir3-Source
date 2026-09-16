# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
from Defines import *
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
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """在这种危险的地方，武器就是我的第二生命，你想用这里面
		的哪种武器？
		
		[前一步:99]
		[结束:0]"""
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """虽然我的手艺不太好，不过一般的武器都能修。可是武器的
		持久性可能会有所损伤。
		
		[前一步:99]
		[结束:0]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """你想卖哪种武器？收购价钱不会太高，你还是好好想想再决
		定吧。
		
		[前一步:99]
		[结束:0]"""
#物品回购
	elif Menu == 5:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
#主菜单
	else:
		say = """欢迎光临，一般的武器我们这儿全都有，你先看看
		
		[购买:1]武器
		[出售:3]武器
		[修理:2]武器
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Enums里的武器类
types =[ItemType.Weapon]
goods = collections.OrderedDict(wuqidiangoodslist)

NpcEvent.add_listener(168,"OnClick",OnClick)