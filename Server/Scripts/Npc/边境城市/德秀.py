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
from 主线任务奖励 import *
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
		say = """请选择要购买的武器。
		
		[前一步:99]
		[结束:0]"""
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """请把要修理的武器放上去。
		
		[前一步:99]
		[结束:0]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把要出售的武器摆上来。
		
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
		if (PlayerGetV(Sender,BV_NQ_MAIN)==2):
			if (Sender.GetItemCount('肉汤') < 1 ):
				say = """肉汤在哪？
					好像这肉汤都发出臭味儿了，不要耍弄人啊！
					
					[结束:0]"""
			else:
				Sender.TakeItem('肉汤',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say =  """呵呵~ 饿了半天了！多谢你给我带吃的过来啊！
					送你一把我们店里卖的木剑就当是报答你了。挺有用的。
					现在再去肉铺找一下肉店金老板，或许有什么让你做的事儿......
					
					[结束:0]"""
		elif (PlayerGetV(Sender,BV_NQ_MAIN)==3):
			say = """肉铺店不是在 <font color=\"0xff00ff00\"> 425:274 </font> 那儿嘛！
				快点回去看看吧！
				
				[结束:0]"""
		else:
			say = """欢迎，感谢光临！
				
				[购买:1]武器
				[出售:3]武器
				[修理:2]武器
				
				[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的武器类			
types =[ItemType.Weapon]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goods = collections.OrderedDict(wuqidiangoodslist)

NpcEvent.add_listener(118,"OnClick",OnClick)