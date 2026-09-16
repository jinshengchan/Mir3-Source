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
#跳转菜单1杂货	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """有什么需要的尽管挑。
		
		[前一步:99]"""
#跳转菜单4卖				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把不用的东西卖给我。
		我给你个合理的价钱。
		
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
	elif (Menu == 800):
		say = """是士官派你来的？
			嗯,那么先吩咐你做件简单的事儿吧！你能去把这个护身符交给武器库的啊潘道友吗?
			
			[好的，没问题:801]"""
	elif (Menu == 801):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==21):
			if (Sender.GiveItem('幸运护身符',1)):
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊潘道友还在等着呢！尽快把这个护身符给他带过去吧！
				他现在一定饿极了......
				从这出去再向右上方一直走就是啊潘道友所在的武器库入口。准确位置在   <font color=\"0xff00ff00\">（429:120）</font> ！
				
				[结束:0]"""
			else:
				say ="""你的包裹满了，整理下在来。

				[结束:0]"""
	elif (Menu == 802):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==23):
			PlayerSetV(Sender,BV_NQ_MAIN,24)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """太好了！
				我在这等你， <font color=\"0xff00ff00\"> 1瓶鸡血</font>  就拜托给你了哦！
				
				[结束:0]"""
	elif (Menu == 803):
		if (Sender.GetItemCount('鸡血') < 1):
			say = """嗯？ 看来这不是 <font color=\"0xff00ff00\"> 鸡血</font>  啊？
				你好象是看错了？
				
				[结束:0]"""
		else:
			if(PlayerGetV(Sender,BV_NQ_MAIN)==24):
				Sender.TakeItem('鸡血',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """辛苦了！
					多亏了你，我才能及时画完所有的护身符啊！
					这是辛苦费请你收下，再回去找找士官吧！
					或许还有别的事情要你做呢！
					
					[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			say = """这里出售道馆里使用的东西。
				
				[购买:1]物品
				[出售:4]物品
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==21):
			say = """这里出售道馆里使用的东西。
				
				[购买:1]物品
				[出售:4]物品
				
				[传达:800] 士官 的话
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==22):
			say = """出去后向右上方一直走就是武器库的入口。
				位置在 <font color=\"0xff00ff00\">（429:120）</font> 。见到啊潘道友后把道力护身符交给他。
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==23):
			say = """把护身符交给啊潘道友了吧? 那么我会信任施主并且再拜托施主办另外的事儿的！
				倒没什么特别的，只是在道馆北部的灌木林中最近总有怪物出没，跑出来骚扰百姓，所以需要许多护身符。
				但是我又有其他的急事要办没时间去弄制护身符所需的鸡血，
				所以希望你替我收集  <font color=\"0xff00ff00\">1瓶鸡血</font>  来。
				嗯, 只要去猎到鸡自然就会有鸡血了，所以不用特别担心！
				
				[好的，我这就去找:802]
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==24):
			say = """哦，找来鸡血了吗？
				
				[找来了！:803]"""
		else:
			say = """这里出售道馆里使用的东西。
				
				[购买:1]物品
				[出售:4]物品
				
				[结束:0]"""
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的其他类
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(zahuodiangoodslist)

NpcEvent.add_listener(37,"OnClick",OnClick)
