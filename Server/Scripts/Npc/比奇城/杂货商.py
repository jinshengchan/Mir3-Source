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
		say = """你想买什么？
		
		[前一步:99]"""
#跳转菜单4卖				
	elif (Menu == 4):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """你要卖什么？
		
		[前一步:99]"""
	elif (Menu == 5):
		say = """我们店里有地牢逃脱卷，
		随机传送卷和修复油等，还有只能从怪物那里得到的回城卷
		
		[前一步:99]"""
#物品回购
	elif Menu == 6:
		# types指定回购物品的类型
		Dict['Types'] = types
		Dict['DialogType'] = NPCDialogType.BuySell
		# (售价倍数, 最高显示多少个)
		Dict['Buyback'] = (float(1), 99999)
		
		say = """这里可以回购玩家出售到商店里的道具，来瞧瞧吧。
			
		[关闭:0]"""
	elif (Menu == 20):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 51):
			PlayerSetV(Sender,BV_NQ_MAIN,52)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """找到苍蝇拍的材料的话我就会帮你做苍蝇拍！
				苍蝇拍所需的材料是 牛毛 和 竹棍。
				先帮我找一些 牛毛 来吧， 牛毛可以从 牛 身上弄到。
				[结束:0]"""
	elif (Menu == 21):
		say = """让我去加入比奇商会？呵呵！人啊！要讲信义才行。
			难道能因为最近王大人的比奇商会发展的好就背叛一直以来帮助我们的崔大夫？你是无论如何都不能用钱收买我的。
			人的信义是比钱更重要的，我最近虽然想摆脱街头小贩的出身，开一家像样儿的店铺很需要钱，但是也不能因为一点钱就出卖了自己的良心啊！
			
			[再好好的想一下吧！:22]"""
	elif (Menu == 22):
		say = """“钱”不是重要的，“钱”算什么啊！……
			把我看成什么了……哼？
			
			[多少钱才行呢？:23]
			[既然你如此固执，那我也没办法了。:30]"""
	elif (Menu == 23):
		say = """.........
			
			[嗯。。。听起来也是个不错的建议。:24]"""
	elif (Menu == 24):
		say = """.................
			
			[那么告诉我你需要多少钱吧！:25]"""
	elif (Menu == 25):
		say = """咳……唔! 1万5千钱左右怎么样……
			
			[好，给你1万5千钱。:26]
			[1万2千钱吧！:27]
			[1万钱就足够了吧！:28]"""
	elif (Menu == 26):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 76):
			if Sender.Gold < 15000:
				say = """为了这点钱可不能出卖良心啊！
					你好像很瞧不起人啊!
					不要再和我提起这件事儿了！
					
					[结束:0]"""
			else:
				SubGold(Sender,15000)
				PlayerSetV(Sender,BV_NQ_MAIN,77)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """你不是在跟我开玩笑吧。
					钱有那么了不起吗，为了这点钱就出卖信义？
					刚才我不知怎么回事头脑好像有点发晕。
					但是我说多少你就给多少，这种豪爽的性格的确出乎我的意料啊！
					和你这个朋友很投缘啊……
					
					[结束:0]"""
	elif (Menu == 27):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 76):
			if Sender.Gold < 12000:
				say = """为了这点钱可不能出卖良心啊！
					你好像很瞧不起人啊!
					不要再和我提起这件事儿了！
					
					[结束:0]"""
			else:
				SubGold(Sender,12000)
				PlayerSetV(Sender,BV_NQ_MAIN,77)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """明白了，那么我会加入比奇商会的。
					但是可要先说清楚了，我绝对不是被你的钱所收买的。
					所谓识时务者为俊杰嘛！我只不过是人在江湖身不由己啊！呵呵呵！
					
					[结束:0]"""
	elif (Menu == 28):
		say = """你不是在跟我开玩笑吧？
			钱有那么了不起吗，为了这点钱就出卖信义？
			刚才我不知怎么头脑好像有点发晕。
			
			[结束:0]"""
	elif (Menu == 30):
		say = """哦……那么……你要走？
			
			[我也没有办法。。。既然你那么讨厌钱。:31]
			
			[可不是嘛！人的信义是用钱买不到的。:40]"""
	elif (Menu == 31):
		say = """好……是个比想象中还要精明的朋友。
			没法子……1万2千钱吧！怎么样？
			
			[好啊！给你1万钱。:32]
			
			[7千钱吧。:33]"""
	elif (Menu == 32):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 76):
			if Sender.Gold < 10000:
				say = """为了这点钱可不能出卖良心啊！
					你好像很瞧不起人啊!
					不要再和我提起这件事儿了！
					
					[结束:0]"""
			else:
				SubGold(Sender,10000)
				PlayerSetV(Sender,BV_NQ_MAIN,77)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """明白了，那么我会加入比奇商会的。
					但是可要先说清楚了，我绝对不是被你的钱所收买的。
					所谓识时务者为俊杰嘛！我只不过是人在江湖身不由己啊！呵呵呵！
					
					[结束:0]"""
	elif (Menu == 33):
		say = """为了这点钱不能出卖良心啊！
			你好像很瞧不起人啊!
			不要再和我提起这件事儿。
			
			[结束:0]"""
	elif (Menu == 40):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 76):
			PlayerSetV(Sender,BV_NQ_MAIN,77)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """咳! 唔... 人的信义是不能用钱收买的。
				但是现在世上很难有向你这样的正人君子啊！
				跟我这样的商人之辈说那样的话……呵呵呵。
				和你这个朋友很投缘啊……
				
				[结束:0]"""
	elif (Menu == 41):
		Sender.TakeItem('烧酒',1)
		say = """正好嗓子有点干……
			谢谢了，咕噜……咕噜……
			
			[现在舒服点了吗？:42]"""
	elif (Menu == 42):
		say = """咕噜……嗯……不错，好多啦！
			真是意气相通的朋友啊！
			刚刚要喝酒，就拿着酒来了，呵呵……
			
			[哈哈。。。真是意气相投啊！:43]"""
	elif (Menu == 43):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==77):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """呵呵呵……好就没有笑得这么痛快了！
				你连我这样的杂货商人都没有嫌弃，还这么亲切的对我，我的心也开始摇摆不定了！
				那么我就会加入比奇商会的。
				
			
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==51):
			say = """最近天气异常的炎热，苍蝇拍的库存货都全部卖光了！……你能帮我找些做苍蝇拍的材料来吗？
				
				[好的！:20]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==52):
			if Sender.GetItemCount('牛毛') < 1:
				say = """还没找够牛毛吗？
					牛毛可以从 牛 身上弄到。
					
					[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,53)
				PlayerSetV(Sender,BV_NQ_KILLMON,1)
				PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
				Sender.TakeItem('牛毛',1)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """嗯，牛毛足够了，还需要您帮我再找一些竹子。
					竹子 或许能从 多钩猫 那儿弄到！
					
					[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==53):
			if Sender.GetItemCount('竹子') < 1:
				say = """还没找够竹子吗？
					竹子可以从 多钩猫 身上弄到。
					
					[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,54)
				Sender.TakeItem('竹子',1)
				PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
				Sender.GiveItem('苍蝇拍',1)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """哦. 材料全部找到了啊！请稍等一下……给你。
					
					[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==54):
			say = """哈哈，我做的苍蝇拍有用吗？
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==76):
			say = """欢迎光临，有什么事吗？
				
				[购买:1]物品
				[出售:4]物品
				[询问:21] 有关 比奇商会 的事
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==77):
			if Sender.GetItemCount('烧酒') < 1:
				say = """什么事儿？还是来劝我加入比奇商会吗？
					虽然跟你很投缘……但是毕竟还要讲讲道义啊！我不能就这样抛弃这段时间对我的有恩的崔大夫啊！
					我没有离开传奇商会的打算，你还是赶紧回去吧！
					心一急，嗓子就有点干……
					
					[结束:0]"""
			else:
				say = """嗯？这是什么？
					
					[先喝一杯，边喝边说。:41]"""
		else:
			say = """欢迎光临，有什么事吗？
				
				[购买:1]物品
				[出售:4]物品
				[询问:5]有关商品的事
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Library.Enums里的其他类			
types =[ItemType.Nothing]
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.5)比例倍数
goods = collections.OrderedDict(zahuodiangoodslist)

NpcEvent.add_listener(70,"OnClick",OnClick)

