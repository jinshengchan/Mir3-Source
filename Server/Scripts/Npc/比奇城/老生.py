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
	elif (Menu == 100):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 57):
			PlayerSetV(Sender,BV_NQ_MAIN,58)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """嘿，什么话？
				我虽然是个做生意的，但我可不是诱拐别人家的孩子那种没头没脑的人。
				你要是就为这件事来找我，还是赶快走吧！
				
				[结束:0]"""
	elif (Menu == 101):
		say = """哦，原来如此
			那你好好看看吧... 都是稀罕玩意儿。。.
			种类多着呢。这些东西商店里都不卖，而且一旦卖出去了，我就不会再进第二次货。你好好想想再买吧。
			这些都是为了得到了又失去的人准备的。。你就算现在买了也没什么用。
			
			[童子像:102]（价格未订）
			[鸡皮:201] 1000金币
			[道力护身符:202] 1000金币
			[肉汤:203] 1000金币
			[古籍:204] 1000金币
			[毒蛇牙齿:205] 8000金币
			[金氏的铁锤:206] 8000金币
			[角笛:207] 20000金币
			[半块不死牌:208] 20000金币
			[不死牌:209] 20000金币
			[千年毒蛇胆汁:210] 50000金币
			[雷电僵尸骨:211] 100000金币
			[僧侣僵尸骨:212] 100000金币
			[毁灭护身符:213] 100000金币
			
			[结束:0]"""
	elif(Menu == 102):
		say = """那个有点困难.. 这东西很少见，我不想卖。
			
			[那我也要买:103]"""
	elif(Menu == 103):
		if(Sender.Gold < 3000):
			say = """我倒是真有心想便宜卖给你，可你连钱都没有。
				你要真想要那个寿石，要么拿个稀罕玩意儿来，要么就拿 3000金币 来。
				
				[结束:0]"""
		else:
			say = """哼... 那就算 3000金币 吧，再有这种稀罕的东西，别忘了拿出来 。
				
				[知道了:104]"""
	elif(Menu == 104):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 60):
			if(Sender.GetItemCount('制魔宝玉') < 1):
				if(Sender.Gold < 3000):
					say = """钱呢？
						
						[结束:0]"""
				else:
					PlayerSetV(Sender,BV_NQ_MAIN,61)
					SubGold(Sender,3000)
					Sender.GiveItem('童子像',1)
					Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
					say = """真是大甩卖了。你到底知不知道那东西的价值啊？
						那玩意儿不是普通的东西，是蕴含着灵气的。 
						你小心点弄它吧。
						
						[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,61)
				Sender.TakeItem('制魔宝玉',1)
				Sender.GiveItem('童子像',1)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """噢噢..这不是制魔宝玉嘛。
					这稀罕玩意儿你从哪儿弄来的？
					
					真不错，把这个寿石给你吧。
					不过，那个童子形状的寿石你一定要小心，那里好像蕴藏了一些让人无从知晓的秘密。
					
					[结束:0]"""
	elif(Menu == 201):
		say = Selist(Sender,'鸡皮')
	elif(Menu == 202):
		say = Selist(Sender,'道力护身符')
	elif(Menu == 203):
		say = Selist(Sender,'肉汤')
	elif(Menu == 204):
		say = Selist(Sender,'古籍')
	elif(Menu == 205):
		say = Selist(Sender,'毒蛇牙齿')
	elif(Menu == 206):
		say = Selist(Sender,'金氏的铁锤')
	elif(Menu == 207):
		say = Selist(Sender,'角笛')
	elif(Menu == 208):
		say = Selist(Sender,'半块不死牌')
	elif(Menu == 209):
		say = Selist(Sender,'不死牌')
	elif(Menu == 210):
		say = Selist(Sender,'千年毒蛇胆汁')
	elif(Menu == 211):
		say = Selist(Sender,'雷电僵尸骨')
	elif(Menu == 212):
		say = Selist(Sender,'僧侣僵尸骨')
	elif(Menu == 213):
		say = Selist(Sender,'毁灭护身符')
	elif(Menu == 214):
		say = Selist(Sender,'牛毛')
	elif(Menu == 215):
		say = Selist(Sender,'竹子')
	elif(Menu == 216):
		say = Selist(Sender,'灵魂护卫')
	elif(Menu == 217):
		say = Selist(Sender,'沃玛金牌')
	elif(Menu == 218):
		say = Selist(Sender,'无名日志')
	elif(Menu == 219):
		say = Selist(Sender,'地狱神钟')
	elif(Menu == 220):
		say = Selist(Sender,'灵魂明珠')
	elif(Menu == 221):
		say = Selist(Sender,'沃玛神铁锤')
	elif(Menu == 222):
		say = Selist(Sender,'沃玛角')
	elif(Menu == 223):
		say = Selist(Sender,'诺玛石')
	elif(Menu == 224):
		say = Selist(Sender,'成致日志')
	elif(Menu == 225):
		say = Selist(Sender,'灵珠')
	elif(Menu == 226):
		say = Selist(Sender,'起爆石')
	elif(Menu == 227):
		say = Selist(Sender,'七点白蛇胆')
	elif(Menu == 228):
		say = Selist(Sender,'气霖证书')
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==57):
			say = """深更半夜的什么事啊？
				你来找我有什么事？
				
				[我来找比奇省的一名妇人的孩子:100]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==58):
			say = """嘿， 你怎么还在？
				你要是再说那种没头没尾的话，就赶快给我走！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==59):
			say = """怎么还是你！ 你要是不买东西就赶快走!
				
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==60):
			say = """怎么还是你！ 你要是不买东西就赶快走!
				
				[今天我是来买东西的。:101]
				
				[结束:0]"""
		else:
			say = """你好好看看。都是些稀罕玩意儿。
				种类多着呢。这些东西商店里都不卖，而且一旦卖出去了，我就不会再进第二次货。你好好想想再买吧。
				这些都是为了得到了又失去的人准备的。。你就算现在买了也没什么用。
				
[鸡皮:201] （1000金币）
[道力护身符:202] （1000金币）
[气霖证书:228]（2000金币）
[肉汤:203] （1000金币）
[古籍:204] （1000金币）
[毒蛇牙齿:205] （2000金币）
[金氏的铁锤:206] （4000金币）
[角笛:207] （4000金币）
[半块不死牌:208] （4000金币）
[不死牌:209] （4000金币）
[千年毒蛇胆汁:210] （4000金币）
[雷电僵尸骨:211] （4000金币）
[僧侣僵尸骨:212] （4000金币）
[毁灭护身符:213] （4000金币）
[牛毛:214] （500金币）
[竹子:215] （500金币）
[灵魂护卫:216] （4000金币）
[沃玛金牌:217] （8000金币）
[无名日志:218] （8000金币）
[地狱神钟:219] （8000金币）
[灵魂明珠:220] （8000金币）
[沃玛神铁锤:221]（8000金币）
[沃玛角:222] （2000金币）
[诺玛石:223]（4000金币）
[成致日志:224] （4000金币）
[灵珠:225] （4000金币）
[起爆石:226]（4000金币）
[七点白蛇胆:227]（8000金币）

				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
def Selist(Sender,GoodName):
	m = goodlist.get(GoodName)
	if (Sender.Gold < m):
		return """天下没有免费的午餐，打工赚够钱再来找我吧！！！
			
			[离开:0]"""
	else:
		SubGold(Sender,m)
		Sender.GiveItem(GoodName,1)
		return """嘿嘿嘿......
			老板请收下。
			
			[结束:0]"""
			
goodlist = {'牛毛':500,
			'竹子':500,
			'鸡皮':1000,
			'道力护身符':1000,
			'肉汤':1000,
			'古籍':1000,
			'毒蛇牙齿':2000,
			'金氏的铁锤':4000,
			'角笛':4000,
			'半块不死牌':4000,
			'不死牌':4000,
			'灵魂护卫':4000,
			'千年毒蛇胆汁':4000,
			'雷电僵尸骨':4000,
			'僧侣僵尸骨':4000,
			'毁灭护身符':4000,
			'沃玛金牌':8000,
			'无名日志':8000,
			'地狱神钟':8000,
			'灵魂明珠':8000,
			'沃玛神铁锤':8000,
			'沃玛角':2000,
			'诺玛石':4000,
			'成致日志':4000,
			'灵珠':4000,
			'起爆石':4000,
			'七点白蛇胆':8000,
			'气霖证书':2000,
}
NpcEvent.add_listener(254,"OnClick",OnClick)
