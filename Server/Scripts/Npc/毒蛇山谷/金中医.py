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
		say = """你需要什么东西？
		
		[前一步:99]"""	
#跳转菜单2卖				
	elif (Menu == 2):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """请把要出售的物品交给我。
		
		[前一步:99]"""
	elif (Menu == 10):
		say = """噢！是来买毒蛇牙齿的啊！
			
			[是的:11]"""
	elif (Menu == 11):
		say = """唔，看起来你不是要药材商或者从医的人吧……
			这倒无所谓！
			不过作为药用的毒蛇牙齿的产量是固定的，每天充其量能供给几包而已。难道你不知道吗？
			
			[其实我是受比奇省药剂师之托而来的……:12]"""		
	elif (Menu == 12):
		say = """比奇省发生传染病? 你说的是真的吗？那我现在就卖给你一包吧！
			现在只有这些，如果需要的话再来吧！
			价格是100钱一颗，给我1000钱就行。
			
			[全额付款买下来:13]
			[讨价还价:14]"""
	elif (Menu == 13):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==71):
			if (Sender.GiveItem("毒蛇牙齿",1)):
				if (Sender.Gold < 1000):
					PlayerSetV(Sender,BV_NQ_MAIN,72)
					Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
					say = """啊？没有钱还来买药？
					真是没办法，先免费给你快拿去给病人们治病用吧！
					
					[结束:0]"""
				else:
					PlayerSetV(Sender,BV_NQ_MAIN,72)
					SubGold(Sender,1000)
					Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
					say = """很着急的样子啊！
					给你，快去比奇省看看吧！
					
					[结束:0]"""
			else:
				say ="""你的包裹满了，整理下在来。
				
				[结束:0]"""
	elif (Menu == 14):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==71):
			if (Sender.GiveItem("毒蛇牙齿",1)):
				if (Sender.Gold < 100):
					PlayerSetV(Sender,BV_NQ_MAIN,72)
					Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
					say = """啊？没有钱还来买药？
					真是没办法，先免费给你快拿去给病人们治病用吧！
					
					[结束:0]"""
				else:
					PlayerSetV(Sender,BV_NQ_MAIN,72)
					SubGold(Sender,100)
					Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
					say = """城内的情况这么紧急的话我就赔本卖给你吧！
					每颗10钱，只付100钱就行。
					连加工费都去掉就按成本给你啦！
					
					[谢谢啦！:15]"""
			else:
				say ="""你的包裹满了，整理下在来。
				
				[结束:0]"""
	elif (Menu == 15):
		say = """谢什么啊！这是我本来就该做的嘛！
			东西都在这儿快快拿去吧！
			
			[结束:0]"""
	elif (Menu == 20):
		say = """你说解蛇毒的药？啊！是说珍珍那孩子吧！
			我也在为了寻找治疗这孩子的药而四处奔波，可是却一直没能找到。
			其实在这蛇儿们聚集的毒蛇山谷建下了村庄而生活的我们一直认为蛇毒没什么大不了的。
			然而看起来咬了珍珍的蛇好像不是普通的蛇啊！
			
			[毒蛇山谷都有什么样的蛇呢？:21]"""
	elif (Menu == 21):
		say = """的确如此！
			如果是被其中一种咬了的话，我也不至于无法解毒啊！但是珍珍所中的毒诱发了一种我从来没见过的罕见症状。
			毒性非常之剧就连用最好的解毒药都一点效果也没有。
			唉……现在几乎所有可用的办法都用过了，唯一的一点希望就只剩最后的一种方法了！
			
			[是什么呢？:22]"""
	elif (Menu == 22):
		say = """就是传说中千年毒蛇胆汁！这种蛇通身雪白，只有北斗七星形状的黑色花纹，被称作“万蛇之王”。
			此种蛇非常之少见，而且毒性也是剧毒无比，不过据说这千年毒蛇的胆汁可以解所有的蛇毒。 
			尽管不知道这世界上是否真的有这种叫作千年毒蛇的蛇，但是种种迹象都值得怀疑，咬了珍珍的好像就是这种千年毒蛇！ 
			如果真的是这样的话，那么这千年毒蛇就应该存在于这毒蛇山谷之中的某个地方，那么这七点毒蛇胆不也就能够弄到手吗？ 
			
			[那么抓到千年毒蛇弄到他的胆就行了！:23]"""
	elif (Menu == 23):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==111):
			PlayerSetV(Sender,BV_NQ_MAIN,112)
			PlayerSetV(Sender,BV_NQ_KILLMON,1)
			PlayerSetV(Sender,BV_NQ_ITEMGOT,0)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """那当然了……我现在也一直在找……可是还没能找到！
				你也帮我一起找找吧！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==71):
			say = """欢迎光临，有什么事吗？
				
				[购买:1]药品
				[出售:2]药品
				
				[购买:10] 毒蛇牙齿
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==72):
			say = """干嘛呢？还不快去比奇省。
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==111):
			say = """欢迎光临，有什么事吗？
				
				[购买:1]药品
				[出售:2]药品
				
				[询问:20] 珍珍的病情
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==112):
			if (Sender.GetItemCount('千年毒蛇胆汁') < 1):
				say = """找到千年毒蛇胆汁的话，就可以为珍珍解毒了！
					
					[购买:1]药品
					[出售:2]药品
					[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,113)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """哇！原来真的有这种传说中的千年毒蛇啊！
					啊！现在还不是说这个的时候……赶快去把这个蛇胆给珍珍的奶奶送去吧！
					
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

NpcEvent.add_listener(81,"OnClick",OnClick)



