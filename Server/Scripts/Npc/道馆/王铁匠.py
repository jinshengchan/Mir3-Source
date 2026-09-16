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
		
		[前一步:99]"""
#跳转菜单2修理				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为Library.Enums里的修理类
		say = """请把要修理的武器放上去。
		
		[前一步:99]"""	
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把要出售的武器摆上来。
		
		[前一步:99]"""	
	elif (Menu == 4):
		say = """商店里出售的武器基本上都差不多，但从怪物那里抢来的武
		器则根据不同的情况，可能具有超凡的能力。如果你把那类
		武器拿到商店里来卖，我可以出个好价钱。还有，武器的价
		格随着种类的不同而不同，但基本上持久性越强，价格就越
		高。
		
		[前一步:99]"""
	elif (Menu == 10):
		say = """你可能已经听华玉那儿听说了吧，由于遭受了好几次洗劫，现在店里已经没什么可用的东西了！ 
			如果是其他的东西也就算了，但可一定要找回我的铁锤才行啊！你有所不知，对于我们铁匠来说，铁锤就是和性命一样重要的东西啊！
			况且那还是用千年木制成的珍品呢！~
			
			[竟有这样的事儿！:11]"""
	elif (Menu == 11):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==96):
			PlayerSetV(Sender,BV_NQ_MAIN,97)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """所以就拜托您了！这附近的混蛋半兽人中应该有一个拿着我铁锤的家伙，请你去帮我找回来吧！ \
				我一定会报答你的！
				
				[结束:0]"""
	elif (Menu == 12):
		say = """不管怎么样，这个是我对你帮我找回铁锤的报答！
			我身上只有这个了，不好意思！
			
			[结束:0]"""
	elif (Menu == 13):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==149):
			PlayerSetV(Sender,BV_NQ_MAIN,150)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """真是年代十分久远的东西啊！不过不知道还有什么用处，好像除了作为古董没什么别的价值了……
				听说比奇省的富豪王大人收集这些东西，拿去卖给他换成钱要比就这么带着更好！
			
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==96):
			say = """欢迎光临，有什么事吗？
				
				[修理:2]武器
				[特殊修理:2]武器
				
				[谈论:10] 最近半兽人的骚乱
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==97):
			if(Sender.GetItemCount('王铁匠的铁锤') < 1):
				say = """我的铁锤可能被这附近的其中一个半兽人拿着呢……
					
					[结束:0]"""
			else:
				Sender.TakeItem('王铁匠的铁锤',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """把我的铁锤找回来了啊！太谢谢你啦！这个铁锤被半兽人抢走后不知道我有多么伤心呢……
					可是……虽然您这么辛苦帮我回了铁锤，却不知哪一天就又会被抢走！可能那时候我连命都也会搭进去呢！
					只有能够除掉那个半兽勇士，让半兽人像以前那样不敢为非作歹，这事情才算完全的解决了啊……唉！
					
					[我会做到的！:12]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==149):
			say = """欢迎光临，有什么事吗？
				
				[修理:2]武器
				[特殊修理:2]武器
				
				[展示:13] 沃玛金牌
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==150):
			say = """据说王大人喜欢收集这些古董，去比奇省看看怎么样？
				
				[修理:2]武器
				[特殊修理:2]武器
				
				[结束:0]"""
		else:
			say = """欢迎光临，有什么事吗？
				
				[修理:2]武器
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的武器类
types =[ItemType.Weapon]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数
goods = collections.OrderedDict(wuqidiangoodslist)

NpcEvent.add_listener(48,"OnClick",OnClick)