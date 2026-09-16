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
		say = """这些都是从沙漠土城商人那里采购的货物，肯定有你需要的。
		
		[前一步:99]"""
#跳转菜单4修理				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为NPCDialogType里的修理类
		say = """你想修理旧饰品，把要修理的饰品拿来吧。
		我的修理技术不会比沙漠土城的工匠差的。
        
		[前一步:99]"""	
#跳转菜单5卖				
	elif (Menu == 5):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """我这里高价回收就的饰品。把你要出售的饰品拿来吧。
		
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
		say = """大家来瞧一瞧看一看啊，这里回收各种项链和戒指，还可以对
		饰品进行修理。快来看啊，都是上好的货色。

		[购买:1]饰品
		[出售:5]饰品
		[修理:4]饰品
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.ItemType里的首饰类			
types =[ItemType.Necklace,ItemType.Ring,ItemType.Bracelet]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goods = collections.OrderedDict(shoushidiangoodslist)

NpcEvent.add_listener(177,"OnClick",OnClick)



