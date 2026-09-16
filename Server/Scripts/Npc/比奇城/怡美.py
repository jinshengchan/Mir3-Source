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
#跳转菜单1衣服	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
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
#物品回购
	elif Menu == 5:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
	elif (Menu == 6):
		say = """您就是最近一直为比奇商会四处游说的人吧！ ！久仰久仰！
			看起来你也是来劝说我加入比奇商会的吧！
			但是现在形势还不明朗，我不便加入。下次再说吧！
			
			[结束:0]"""
	elif (Menu == 10):
		say = """你是来劝我加入比奇商会的吧……
			看来由于您的活动，比奇省的商权现在确实将要全部揽到王大人的手中啊！
			如果连我都加入比奇商会的话，崔大夫的传奇商会将彻底瓦解了！
			
			[这是大势所趋，你还是作出明智的选择吧！:11]"""
	elif (Menu == 11):
		say = """就像其它商人一样，我也有个条件。
			如果你答应我的条件的话，我就会加入比奇商会。
			
			[什么条件呢:12]"""
	elif (Menu == 12):
		say = """像我们这样的普通人由于怪物们的威胁不能在城以外的地方自由活动。
			不久之前我在城外遇到了怪物，使用地牢逃脱卷不但没能逃会城里，反而渐渐到了更加奇怪的地方，差点儿丢了性命。
			
			[看来你没有回城卷啊！:13]"""		
	elif (Menu == 13):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==80):
			PlayerSetV(Sender,BV_NQ_MAIN,81)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """是啊！我要是有能够使我安全回到城里的回城卷的话我就不会经历那种可怕的事情了。
				所以我的条件就是给我一包回城卷。如果你能找来 回城卷 10个 给我的话，我就会加入比奇商会。
				
				[结束:0]"""
	elif (Menu == 14):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 81):
			if(Sender.GetItemCount('回城卷') < 10): 
				say = """嗯，如果能给我 回城卷 10个 ，我就会听从你的劝说。
					
					[结束:0]"""	
			else:
				Sender.TakeItem('回城卷',10)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """谢谢，现在有了回城卷我就不会像以前那样再遇到那么危险的状况了。
					既然这样我会遵守诺言加入比奇商会的。
					替我转告王大人一声吧！
					
					[结束:0]"""
	elif (Menu == 20):
		say = """哦！是你啊！久仰久仰！
			不过……看起来你今天的穿着还是那么回事儿啊！呵呵呵！
			不知你是否知道我们店里所卖的轻型盔甲呢？
			
			[知道:21]
			[我不太清楚:22]"""
	elif (Menu == 21):
		say = """那我就不必给你说明啦！
			其实，我有一件关于这种盔甲的事情要拜托你……
			
			[有什么要拜托的事情请您尽管说。:23]"""
	elif (Menu == 22):
		say = """“轻型盔甲”是等级达到11级之后才可以穿上的防御服。
			主要部分都是用钢铁打造的，所以比起布衣要重的多，但是防御力也特别的好。
			我有一件关于这种盔甲的事情要拜托你……
			
			[有什么要拜托的事情请您尽管说。:23]"""
	elif (Menu == 23):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 84):
			PlayerSetV(Sender,BV_NQ_MAIN,85)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """是这样的，最近来买轻型盔甲的顾客非常多，可是用来做辅强剂的铁矿不够用了。
				所以您要是能够给我找来 5个纯度13以上的铁矿 的话，我就会为你特别制作一套轻型盔甲。
				
				[到哪儿去找铁矿呢？:24]
				[知道了。:0]"""
	elif (Menu == 24):
		say = """先去武器店或铁匠铺买把鹤嘴锄，再去 矿山 就可以挖到各种矿石！
			挑出我所需要的纯度在13以上的铁矿之后，剩下的还可以卖给武器店赚到很多钱。
			如果你觉得麻烦不想去矿山挖矿的话也可以去武器店购买铁矿，但是那样的话就有点亏本哦！
			
			[结束:0]"""
	elif (Menu == 25):
		say = """先去武器店或铁匠铺买把鹤嘴锄，再去 矿山 就可以挖到各种矿石！
			挑出我所需要的纯度在13以上的铁矿之后，剩下的还可以卖给武器店赚到很多钱。
			如果你觉得麻烦不想去矿山挖矿的话也可以去武器店购买铁矿，但是那样的话就有点亏本哦！
			
			[到哪儿去找铁矿呢？:25]"""
#主菜单
	else:
		if(75 < PlayerGetV(Sender,BV_NQ_MAIN) < 80):
			say = """欢迎光临，有什么事吗？
				
				[购买:1]防御工具
				[出售:4]防御工具
				[修理:3]防御工具
				
				[邀请:6] 怡美 加入比奇商会
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 80):
			say = """欢迎光临，有什么事吗？
				
				[购买:1]防御工具
				[出售:4]防御工具
				[修理:3]防御工具
				
				[邀请:10] 怡美 加入比奇商会
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 81):
			say = """欢迎光临，有什么事吗？
				
				[购买:1]防御工具
				[出售:4]防御工具
				[修理:3]防御工具
				
				[邀请:14] 怡美 加入比奇商会
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 82):
			say = """如果你去王大人那里的话，就替我转告他我会加入比奇商会的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 84):
			say = """我正忙得要命呢，不要总来打扰我。
				不想帮我的忙就别来妨碍我做生意……
				
				[让我来帮您吧！:20]
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 85):
			if(Sender.GetItemCount('铁矿') < 5):
				say = """还没有带来我要的铁矿啊！
					
					[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,86)
				Sender.TakeItem('铁矿',5)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """拿来铁矿了啊！
					嘻嘻，现在不用担心原料不足，可以稳定的供应顾客的需求啦！
					太谢谢你啦!这是我说好为你定做的特制轻型盔甲。
					这可是我特地为您精心制作的哦，所以要像对我一样珍惜爱护啊！呵呵呵~！
					
					[结束:0]"""
		else:
			say = """欢迎光临，有什么事吗？
				
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

NpcEvent.add_listener(76,"OnClick",OnClick)




