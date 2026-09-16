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
#跳转菜单1
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library里的NPCDialogType买卖类
		say = """你想买首饰？
			
			[前一步:99]"""
#跳转菜单4修理				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Repair   #类型为NPCDialogType里的修理类
		say = """你想修理饰品？
			
			[前一步:99]"""	
#跳转菜单5卖				
	elif (Menu == 5):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """你想出售饰品？
			
			[前一步:99]"""			
#物品回购
	elif Menu == 2:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
			[关闭:0]"""
	elif (Menu == 10):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 46):
			PlayerSetV(Sender,BV_NQ_MAIN,47)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """这个……我知道的就只有这些了。唉.. 人世艰辛啊！
				前不久我们店里也来过一个  <font color=\"0xff00ff00\">失魂落魄的女子</font>  ，据说她在逃难时失去了丈夫要靠自己来混口饭吃。
				那个人好像有什么难言之隐，一直少言寡语。
				我们商店因为人手够，所以介绍她去 棉布店 工作了。
				不过依我看那个女子好像和洪气霖是从一个地方来的！
				
				[结束:0]"""
	elif (Menu == 20):
		say = """加入王大人的商会？
			杂货商不加入我也不会加入的。你先把他劝服再来吧！
			
			[结束:0]"""
	elif (Menu == 21):
		say = """是来说服我加入比奇商会的吧！
			嗯……我没有这个打算。
			
			[商界的形势已经开始向一边倾斜了。:22]"""
	elif (Menu == 22):
		say = """你是说杂货商已经加入到比奇商会了？
			呵呵呵，不要以为我和杂货商是一类人！
			现在这个店铺规模也很大，生意也不错！
			可不是和那种小商贩一样能够随便收买得了的。
			
			[但是。。。:23]"""
	elif (Menu == 23):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 78):
			PlayerSetV(Sender,BV_NQ_MAIN,79)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """这个生意一直以来都是靠有不同新花样的新鲜玩艺儿来维持的，可是进来却很难看到新鲜的东西，实在是很郁闷！
				可是又不能扔下店里事情去外面采购些新的货物……
				所以你要是能替我找来些一眼就能相中的 新鲜玩艺儿 的话，我就会加入比奇商会。
				
				[结束:0]"""
	elif (Menu == 24):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 79):
			if(Sender.GetItemCount('角笛') > 0):
				Sender.TakeItem('角笛',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊？这个到底是什么呢？
					地位很高的半兽人战士在指挥半兽人们时使用的笛子，虽然外表很难看，但是却可以发出非常好听的声音！
					真是太美妙了！没想到会看见这种东西……
					
					好的！你帮我搜集到了这么多奇珍异宝，我应该听从你的劝说！
					崔大夫？嗯，管它呢！
					
					[结束:0]"""
			elif(Sender.GetItemCount('不死牌') > 0):
				Sender.TakeItem('不死牌',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊？这个到底是什么呢？
					你说这是能够借助器物的力量突破所设困魔咒的那种叫做不死牌的护身符？现在亲眼见到后，果然能感觉到这股神圣的力量！
					真是太美妙了！没想到会看见这种东西……
					
					好的！你帮我搜集到了这么多奇珍异宝，我应该听从你的劝说！
					崔大夫？嗯，管它呢！
					
					[结束:0]"""
			elif(Sender.GetItemCount('灵魂护卫') > 0):
				Sender.TakeItem('灵魂护卫',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊？这个到底是什么呢？
					很有古香古色神秘的感觉。
					天哪！你说这是从古代流传下来的有着佛师魔法的东西？
					真是太美妙了！没想到会看见这种东西……
					
					好的！你帮我搜集到了这么多奇珍异宝，我应该听从你的劝说！
					崔大夫？嗯，管它呢！
					
					[结束:0]"""
			elif(Sender.GetItemCount('毁灭护身符') > 0):
				Sender.TakeItem('毁灭护身符',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊？这个到底是什么呢？
					这是能够摄人魂魄的妖怪携带的东西？那么能用这个盛装灵魂？这个实在是太神奇太让我吃惊了！
					
					好的！你帮我搜集到了这么多奇珍异宝，我应该听从你的劝说！
					崔大夫？嗯，管它呢！
					
					[结束:0]"""
			elif(Sender.GetItemCount('沃玛金牌') > 0):
				Sender.TakeItem('沃玛金牌',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊？这个到底是什么呢？
					你说什么？连你都不知道这是什么？呵呵呵……
					不过你说这是在沃玛寺庙找到的东西，所以一定也不会是平常的东西！这里面好像藏着什么大秘密。令我心里七上八下的。
					
					好的！你帮我搜集到了这么多奇珍异宝，我应该听从你的劝说！
					崔大夫？嗯，管它呢！
					
					[结束:0]"""
			elif(Sender.GetItemCount('地狱神钟') > 0):
				Sender.TakeItem('地狱神钟',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊？这个到底是什么呢？
					过去沃玛教徒们使用过的东西？天哪！这是什么时候的事儿啦……
					能看到只在传说种听说过的沃玛教遗物我真是太幸运了！
					
					好的！你帮我搜集到了这么多奇珍异宝，我应该听从你的劝说！
					崔大夫？嗯，管它呢！
					
					[结束:0]"""
			elif(Sender.GetItemCount('灵魂明珠') > 0):
				Sender.TakeItem('灵魂明珠',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """啊？这个到底是什么呢？
					是盛着很久以前牺牲的人们灵魂的玉石？哦！真是听起来让人惋惜的事儿……
					但是这玉石实在是太漂亮了！我还是头一次见到这种散射出若隐若现光芒的玉石呢…
					
					好的！你帮我搜集到了这么多奇珍异宝，我应该听从你的劝说！
					崔大夫？嗯，管它呢！
					
					[结束:0]"""
			else:
				say = """这不是什么新鲜玩艺儿啊！你在耍我吗？
					
					[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 46):
			if(Sender.GetItemCount('气霖证书') < 1):
				say = """没有带着气霖证书来啊！我也是很忙的人，请不要和我开玩笑。
					
					[结束:0]"""
			else:
				say = """嗯.. 这个是洪气霖那个人的证书啊！对不起，我们也不能收下这证书！
					那么你知道关于洪气霖这个人的事儿吗？ 真是越想越觉得蹊跷！
					抛弃好好的家，过着四处流浪的生活。好不容易遇到知己，结为百年好合……但是因为这家伙是土匪和妻子分手了。
					两个人分手的时候约定在比奇省这儿见面，于是就遵照约定这样一直在这儿等下去…… 啧啧……
					
					[那么还知道关于这个人其他的什么事儿吗？:10]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 47):
			say = """这个……我知道的就只有这些了。唉.. 人世艰辛啊！
				前不久我们店里也来过一个  <font color=\"0xff00ff00\">  失魂落魄的女子 </font> ，据说她在逃难时失去了丈夫要靠自己来混口饭吃。
				那个人好像有什么难言之隐，一直少言寡语。
				我们商店因为人手够，所以介绍她去  <font color=\"0xff00ff00\">  棉布店 </font> 工作了。
				不过依我看那个女子好像和洪气霖是从一个地方来的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 76):
			say = """欢迎光临，你想要什么？
				
				[购买:1]饰品
				[出售:5]饰品
				[修理:4]饰品
				
				[邀请:20] 恩实 加入比奇商会
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 78):
			say = """欢迎光临，你想要什么？
				
				[购买:1]饰品
				[出售:5]饰品
				[修理:4]饰品
				
				[邀请:21] 恩实 加入比奇商会
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) == 79):
			say = """欢迎光临，你想要什么？
				
				[购买:1]饰品
				[出售:5]饰品
				[修理:4]饰品
				
				[邀请:24] 恩实 加入比奇商会
				
				[结束:0]"""
		else:
			say = """欢迎光临，你想要什么？
				
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

NpcEvent.add_listener(57,"OnClick",OnClick)
