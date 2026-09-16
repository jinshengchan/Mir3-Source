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
#红名
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不会和双手沾满血腥的人说话的。
			
			[关闭:0]"""
#跳转菜单
	elif (Menu == 1):
		if(Sender.GetItemCount("古籍") < 1):
			say = """我的书呢？
				可能不知道丢哪儿去了吧……
				找到了的话带来吧！
				
				[结束:0]"""
		else:
			Sender.TakeItem('古籍',1)
			MainQuestRewards(Sender)
			PlayerSetV(Sender,BV_NQ_MAIN,38)
			SEnvir.UpdateNPCLook(246, permanent = False, name = None, 
                nameColor = None,
                libraryFile = LibraryFile.None, bodyShape = 0, overlay = None,
                updateIcon = True, icon = QuestIcon.None, player = Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """我就是你要找的王某人..
				啊哈，这就是我以前想要的古书。远道而来，辛苦你啦！
				这是给你的辛苦费，请收下吧！
				对了, 或许以后还需要你的帮助呢……下次再来吧！
				
				[结束:0]"""
	elif (Menu == 2):
		PlayerSetV(Sender,BV_NQ_MAIN,64)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """真的太感谢了！我期待着你能带来好消息！
				传奇商会所属的其它商人仍然还有很多，但是现在凭我自己的力量很难一一说服。虽然从好几个方面同时下手。
				不管怎样？难道不该先避免沦为乞丐吗？
				所以拜托啦！
				
				[结束:0]"""
	elif (Menu == 3):
		say = """不行……？
			那么我只好再去找其他人了。
			
			[结束:0]"""
	elif (Menu == 4):
		MainQuestRewards(Sender)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """这个虽然菲薄但是我的诚意，请收下吧！
			
			[结束:0]"""
	elif (Menu == 5):
		say = """事情是这样的。
			我有个经营牛生意的远房亲戚叫做王小二，可是最近不知怎么回事儿，她的女儿好像中了邪似的灵魂脱壳了……
			为了能够让那个孩子恢复知觉用尽了各种各样办法，却一点效果都没有！而且最近又流传着很多诡异的传闻…… 
			王小二听说这次您粉碎了半兽人的阴谋的事迹，所以就来求我拜托你了……他说你算是他最后的希望了……
			
			[有什么诡异的传闻呢？:6]"""
	elif (Menu == 6):
		say = """唔嗯……这个你直接去听听就知道了！
			不过这件事儿能不能就拜托给你呢？他们会重重谢你的！
			
			[好吧！去哪儿找他呢？:7]"""
	elif (Menu == 7):
		PlayerSetV(Sender,BV_NQ_MAIN,116)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """你去比奇省西北城门之外 357:273 就能找到他们家了。王小二这个名字很好记吧……
			
			[结束:0]"""
	elif (Menu == 8):
		if (Sender.GetItemCount('沃玛金牌') < 1):
			say = """好像没有带着沃玛金牌啊！这是怎么回事儿？ 
				
				[结束:0]"""
		else:
			say = """哦！真是很久以前的古董了啊!能告诉我这是什么东西吗？ 
				
				[在沃玛神殿中偶然得到的，但我也不知道是什么东西。:9]"""
	elif (Menu == 9):
		say = """唔……那么对你来说没什么用啊！这样吧！就把这个沃玛金牌卖给我，我会给你个好价钱的……
			怎么样？能卖给我吗？
			
			[好的，卖给你！:10]
			[现在还不想卖！:11]"""
	elif (Menu == 10):
		if (Sender.GetItemCount('沃玛金牌') < 1):
			say = """好像没有带着沃玛金牌啊！这是怎么回事儿？ 
				
				[结束:0]"""
		else:
			Sender.TakeItem('沃玛金牌',1)
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """您为了我们比奇商会做了很多事情，一定会给你个高价来买的！
				
				[谢谢！:0]"""
	elif (Menu == 11):
		say = """呵呵……可惜啊！好久没有看到这样的古董了，特别想买下来……
			如果你改变主意了的话，什么时候来都行！
			
			[结束:0]"""
	elif (Menu == 12):
		PlayerSetV(Sender,BV_NQ_MAIN,152)
		say = """有传闻说在道馆附近的什么地方有一位独自生活的老人，他有很多过去沃玛教中曾经使用过的古董。
			我也听说了这事儿并派人去他那儿买，可是都失败了！如果你去沃玛神殿附近打猎的时候遇到那个老人的话，就告诉他我王某人想要出高价购买他的东西！
			那个无名老人隐居在 道馆西北部的小山谷里 的一个小茅屋中，不过 进入他隐居地的入口 可不太好找！
			
			[结束:0]"""
	elif (Menu == 13):
		say = """嗯？又发生什么事儿了？要拿走沃玛金牌？
			
			[请您听一下我在道馆遇到的无名老人所说的话吧！:14]"""
	elif (Menu == 14):
		PlayerSetV(Sender,BV_NQ_MAIN,156)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """嗯……原来还有这等事情啊……我不知竟是如此，结果又犯了一个错误啊……其实那个沃玛金牌已经不在我的手中了！
			要去沙漠的贸易商需要这种物品作为礼物送给当地土著部落族长，所以来求我。本来我不想给他的，但是那是个非常重要的贸易线，实在没办法拒绝啊！
			不过既然除掉沃玛教主必需那个金牌的话……尽快去追那个人还来得及，那个贸易商说要去沙漠，快去追的话还能追上。
			
			[结束:0]"""
	elif (Menu == 15):
		say = """......
			
			[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==7):
			say = """嗯，这位勇士，有事吗？
				
				[递交古籍:1] 给王大人
				
				[你认错人了吧:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==17):
			say = """嗯，这位大师，有事吗？
				
				[递交古籍:1] 给王大人
				
				[你认错人了吧:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==27):
			say = """嗯，这位道友，有事吗？
				
				[递交古籍:1] 给王大人
				
				[你认错人了吧:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==37):
			say = """啊，难道仇敌找上门来了吗？
				
				[递交古籍:1] 给王大人
				
				[你认错人了吧:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) < 37):
			say = """随便闯入别人家你难道一点都不觉得不好意思吗？
				
				[你认错人了吧:0]"""
		elif(37 < PlayerGetV(Sender,BV_NQ_MAIN) < 63):
			say = """嗯，有事吗？
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==63):
			say = """噢！你来啦！
				你要是不来我正好要派人去叫你呢？
				其实我是有事情要拜托你做！
				是这样的！最近以我为会长的比奇商会和以那个姓崔的贪得无厌的家伙为首的传奇商会正在互相争夺势力……
				啊！当然不是真刀真枪的动武啦！
				是为了争夺商权而展开的势力之争。
				不管怎么样，胜者为王败者寇，在这场斗争中失败者将被排挤出比奇省。
				因此想要求你帮我办点事情，为了增强我们比奇商会的势力，请你去说服图书管理人和施药商药剂师从传奇商会中退出，来加入我们比奇商会。
				
				[嗯，好的:2]
				
				[不，我现在还有别的事情:3]"""
		elif(63 < PlayerGetV(Sender,BV_NQ_MAIN) < 74):
			say = """有进展了吗？
				再加把劲儿……
				只要图书管理人和药剂师加入我们这一方的话就是一次值得的斗争！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==74):
			say = """
				噢！哦！我们终于让图书管理人和药剂师从传奇商会退出了！
				他们真的说同意加入比奇商会啦？
				做得好！做得实在是太棒啦！哈哈哈！
				
				[您过奖啦！:4]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==75):
			say = """嗯……现在那个姓崔的家伙的传奇商会就要完蛋啦！呵…呵…
				
				[结束:0]"""
		elif(75 < PlayerGetV(Sender,BV_NQ_MAIN) < 82):
			say = """听说……你最近……
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==82):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """噢！你来啦！
				真没想到啊！不知不觉中就把传奇商会的商家拉拢到我们这一方啦！
				真是手腕精明啊！由于你的活动终于使我们比奇商会统一了比奇地区商权。
				这是为了报答你的功劳准备的一点小小礼物，请不要谦让务必收下。
				
				[结束:0]"""
		elif(82 < PlayerGetV(Sender,BV_NQ_MAIN) < 115):
			say = """我已经听说了有关你的事儿，你真是这个了不起的朋友啊。 哈哈哈！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==115):
			say = """啊！正好想要再派人去找你来呢，其实，是因为又有点奇怪的事儿发生，所以需要你的帮助！
				
				[是什么事儿呢？:5]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==116):
			say = """去西北城门外（357:273）找叫王小二的人吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==117):
			say = """找到他家了吧！那就多多拜托了！最近由于那个妖怪的传闻搅得民心惶惶的！
				
				[结束:0]"""
		elif(112 < PlayerGetV(Sender,BV_NQ_MAIN) < 121):
			say = """你不和我是一家人嘛！
				什么时候来都行啊！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==150):
			say = """您又为何事而来呢？
				
				[给你看沃玛金牌来了！:8]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==151):
			say = """呵呵！越看越神奇啊!对了，你听说过关于那个有很多沃玛神殿中物品的老人的故事吗？
				
				[没有，没听过！:12]"""
		elif(151 < PlayerGetV(Sender,BV_NQ_MAIN) < 155):
			say = """好像你找到住在道馆附近的老人了吧？
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==155):
			say = """好像你找到住在道馆附近的老人了吧？
				
				[其实……我是来要回沃玛金牌的！:13]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==156):
			say = """您的侠义心肠实在是了不起啊！祝你一定能够找到那个去沙漠的贸易商！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==157):
			PlayerSetV(Sender,BV_NQ_MAIN,158)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """嗯！你说贸易商要求用其他能代替沃玛金牌的东西吗？咳！那个人也必须给当地土著送这种东西做礼物，实在是没办法啊！
				啊！或许那个十分了解沃玛神殿的老人知道他要什么呢！去那个无名老人那儿打听一下吧！
				
				[结束:0]"""
		elif(157 < PlayerGetV(Sender,BV_NQ_MAIN) <161 ):
			say = """不知道那个老人是有何种内力的人啊！ 
				
				[结束:0]"""
		elif(160 < PlayerGetV(Sender,BV_NQ_MAIN) <163 ):
			say = """是地狱神钟啊……真是让我贪心的东西啊！但是已经有主儿了，我也只能无可奈何了。用这个完全可以换回沃玛金牌的！ 
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==162):
			say = """是地狱神钟啊……真是让我贪心的东西啊！但是已经有主儿了，我也只能无可奈何了。用这个完全可以换回沃玛金牌的！ 
				
				[结束:0]"""
		else:
			say = """我已经听说了有关你的事儿，你真是这个了不起的朋友啊。 哈哈哈！
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(246,"OnClick",OnClick)
