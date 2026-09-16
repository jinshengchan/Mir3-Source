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

#跳转菜单1
	if (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """你快点挑啊？
		挑好了我才能去继续练级。
		
		[关闭:0]"""	
#跳转菜单3卖
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的修理类
		say = """闲置不用的物品我出高价回收。
		
		[返回:99]
		[关闭:0]"""
	elif (Menu == 3):
		say = """在找诅咒之药水吗? 你真幸运,我刚刚拿到了好东西想看看吗? 每一瓶价格是500万金币
		
		[购买:4]
		
		[再想一想:0]"""	
	elif (Menu == 4):
		if(Sender.Gold < 5000000):
			say = """什么? 没钱你还想购买药水? 等你有了钱再来吧
			
			
			[关闭:0]"""	
		else:
			SubGold(Sender,5000000)
			Sender.GiveItem('诅咒之药水',1)
			say = """呵呵,真是有福气的年轻人.随时欢迎你再来.能有像你这样有福气的老顾客,对我来说也不是好事吗?"""
#主菜单
	else:
		say = """见到你真好。这里四处都是怪物，我很担心。。。
		我想把药水卖完之后，赶快离开这儿。
		虽然比村庄贵一些，可是你来之前，我都给人家卖3倍的价格，
		你到其他地方买不到这个价格。
		
		[查看:1] 商店药品
		
		[出售:2] 药品
		
		[购买:3] 诅咒之药水
		
		[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

#类型为 Enums里的普通类
types =[ItemType.Nothing]
goods = collections.OrderedDict(yaodiangoodslist)

NpcEvent.add_listener(197,"OnClick",OnClick)
