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
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """你需要什么东西？
		
		[前一步:99]"""	
#跳转菜单2卖				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把要出售的物品交给我。
		
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
	elif (Menu == 10):
		say = """唉！真是太吃力了，快要挺不住了……
			唔…跟你这样的人诉苦也没什么用……
			虽然为了以在这儿打猎的人为对象做生意，才来到这儿定居。不过虽然利益大，冒的风险也大啊！
			原本遭到官兵讨伐削减了势力消失踪影的半兽人最近推举出了个厉害的半兽勇士，又有组织的聚集到了一起。这里已经受过它们不知多少次的肆虐践踏了！ 
			如果一直是这样的话我也就该关门大吉，回乡养老去了！
			
			[真是让你受苦了，可是或许您知道。。。:11]"""
	elif (Menu == 11):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==95):
			PlayerSetV(Sender,BV_NQ_MAIN,96)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你问半兽人有没有拿着什么特别的东西……？
				嗯……这个, 最近好像没有什么特别的啊……
				不过跟这个比起来，最近王铁匠好像遇到了不少麻烦，你有什么帮助他的办法吗？
				
				[结束:0]"""
	elif (Menu == 12):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==98):
			PlayerSetV(Sender,BV_NQ_MAIN,99)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """你问半兽人有没有拿着的什么特别的东西?
				这个…谁知道呢……让我想想……哦，对了，好像不久前看见过一个 半兽战士 脖子上带了一个样子很奇怪的角笛。
				虽然一次都没有听见过那半兽人吹笛子的声音，但是那个东西好像有点奇怪啊！
				不过我也不知道那个半兽勇士在哪儿，可能在某个洞穴里藏着吧……
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==95):
			say = """欢迎光临，有什么事吗？
			
			[购买:1]药品
			[出售:2]药品
			
			[谈论:10] 最近半兽人的骚乱
			
			[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==96):
			say = """看到王铁匠由于丢了铁锤十分伤心的样子，我就感到十分心疼啊……
				
				[购买:1]药品
				[出售:2]药品
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==97):
			say = """看到王铁匠由于丢了铁锤十分伤心的样子，我就感到十分心疼啊……
				
				[购买:1]药品
				[出售:2]药品
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==98):
			say = """已经帮王铁匠找回铁锤了呀，太厉害了！
				
				[购买:1]药品
				[出售:2]药品
				
				[谈论:12] 半兽人身上的特殊物品
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==99):
			say = """去找找那个半兽人战士带着的角笛怎么样？
				由于有那个半兽勇士我也很忧心啊！
				
				[购买:1]药品
				[出售:2]药品
				
				[结束:0]"""
		else:
			say = """欢迎光临，有什么事吗？
				
				[购买:1]药品
				[出售:2]药品
				
				[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类			
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(yaodiangoodslist)

NpcEvent.add_listener(46,"OnClick",OnClick)



