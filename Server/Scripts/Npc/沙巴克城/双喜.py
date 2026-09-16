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
		Dict['CastleName'] = '沙巴克' # 此NPC隶属沙巴克 受到沙巴克税收和折扣的影响
		say = """你要买什么？
		
		[前一步:99]"""
#跳转菜单3修理				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """确定要修理吗？
		
		[前一步:99]"""	
#跳转菜单4卖				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把要出售的衣服拿出来，我来估估价。
		这里头盔和帽子都有收购，就在这儿卖吧。
		
		[前一步:99]"""		
#主菜单
	else:
		say = """欢迎光临，我们店里有各式各样的衣服，你随便挑选。
		
		[购买:1]防御工具
		[出售:4]防御工具
		[修理:3]防御工具
		
		[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Library.Enums里的衣服头盔鞋子盾牌类
types =[ItemType.Armour,ItemType.Helmet,ItemType.Shoes,ItemType.Shield]
goods = collections.OrderedDict(buyidiangoodslist)

NpcEvent.add_listener(100,"OnClick",OnClick)




