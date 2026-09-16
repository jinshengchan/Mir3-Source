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
		say = """请选择你所需要的。
		
		[前一步:99]"""	
#跳转菜单2卖				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """你想卖什么药？
		
		[前一步:99]"""			
#跳转菜单3买诅咒药水				
	elif (Menu == 3):
		say = """在找诅咒之药水？你真幸运，我刚刚拿到了好东西想看看
		吗？每一瓶价格是500万金币。
		
		[购买:31]

		[再想一想:32]"""
	elif (Menu == 31):
		if (Sender.Gold < 5000000):
			say = """你没有足够的金币，无法购买。
				
			[结束:0]"""	
		else:
			SubGold(Sender,5000000)
			Sender.GiveItem("诅咒之药水",1)
			say = """呵呵，真是有福气的年轻人。随时欢迎你再来。能有像你这样
			有福气的老顾客，对我来说也不是好事吗？
			
			[结束:0]"""
	elif (Menu == 32):
		say = """如果是这样，就只能作罢。想清楚后再来吧。
		
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
		if(PlayerGetV(Sender,BV_NQ_SJKILL)==5001 and Sender.Level > 32):  #判断神舰任务开启  等级达到33级
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你的样子好奇怪哦，是哪里不舒服吗？
				占卜师 梅山侠 或许能帮助你。。
				
				[结束:0]"""
		else:
			say = """最近外地人常来。你要的是什么来着？
			
			[购买:1]药品
			[出售:2]药品
			
			[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

#类型为 Enums里的普通类
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(yaodiangoodslist)

NpcEvent.add_listener(158,"OnClick",OnClick)



