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
#跳转菜单1衣服	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """人类勇士总认为这个价格太贵。但如果他们知道弄这些东西
		有多困难，就应该能接受这个价格。少一分钱我也不会卖。
		
		[前一步:99]"""
#跳转菜单3修理				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """想修理旧衣服？怎么，你怀疑我的技术吗？我虽然刚刚开始修
		理人类的衣服，但以我多年修理诺玛族盔甲的经验来看，修理
		人类的衣服也没问题。
		
		[前一步:99]"""	
#跳转菜单4卖				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """我们诺玛族已经习惯了沙漠的气候，根本就不用穿多余的衣服。
		但人类不同...反正，先让我看看你的东西。
		
		[前一步:99]"""		
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
		say = """虽然我进货的时候比较仓促，但所进的都是好货色，尽管挑吧。
		
		[购买:1]防御工具
		[出售:4]防御工具
		[修理:3]防御工具
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的衣服头盔鞋子盾牌类			
types =[ItemType.Armour,ItemType.Helmet,ItemType.Shoes,ItemType.Shield]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(buyidiangoodslist)

NpcEvent.add_listener(176,"OnClick",OnClick)




