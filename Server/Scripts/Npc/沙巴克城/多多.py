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
		Dict['CastleName'] = '沙巴克' # 此NPC隶属沙巴克 受到沙巴克税收和折扣的影响
		say = """来~挑选适合自己的饰品啊。
		
		[前一步:99]"""
#跳转菜单4修理				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为NPCDialogType里的修理类
		say = """可以修理饰品，手套和皮革盔甲。
        
		[前一步:99]"""	
#跳转菜单5卖				
	elif (Menu == 5):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """你想出售饰品？
		顺便说一下，本店还经营手套。
		
		[前一步:99]"""			
#物品回购
	elif Menu == 6:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
#主菜单
	else:
		say = """欢迎光临，本店专门经营饰品。你想买什么样的饰品？


		[购买:1]饰品
		[出售:5]饰品
		[修理:4]饰品
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Library.ItemType里的首饰类
types =[ItemType.Necklace,ItemType.Ring,ItemType.Bracelet]
goods = collections.OrderedDict(shoushidiangoodslist)

NpcEvent.add_listener(98,"OnClick",OnClick)



