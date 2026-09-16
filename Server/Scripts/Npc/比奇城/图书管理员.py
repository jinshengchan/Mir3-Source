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
#跳转菜单1
	elif (Menu == 1):
		say = """......
			
			[结束:0]"""
	elif (Menu == 103):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==58):
			PlayerSetV(Sender,BV_NQ_MAIN,59)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """关于那个夜市商人嘛……唔……好像除了最近得到一个奇特的寿石之外就没有什么特别的消息了！
				那块寿石倒是蛮稀有的，据说是童子模样的呢！
				
				[这好像真有点不着边际啊！不管了还是去告诉那个妇人吧！:0]"""
	elif (Menu == 104):
		say = """比奇商会?
			啊！啊！知道了！是那个叫做王大人的创办的商人联合会吧！
			可是我已经加入了崔大夫创办的传奇商会，还是去别的地方试试吧！
			
			[也就是说无论如何都不行吗？:105]"""
	elif (Menu == 105):
		say = """无论如何...
			如果你能为我办点事情的话，我也不是不能加入比奇商会的……
			
			[要我帮你做什么事儿才行呢？:106]"""
	elif (Menu == 106):
		say = """其实最近我正在编撰记录比奇省地理和历史的书籍。
			如果想要写好这本书的话必然要从各种各样的人那里收集关于比奇省的资料和信息，可是唯独比奇省的卫士们那里不与我合作啊！
			不管怎么样你也是武林人士，可能和他们能够有通融的地方，所以这就是我要拜托你的事情！
			值班卫士反正也不能和别人说话，所以希望你能替我去那儿找那些休班卫士从他们那里收集关于比奇省历史的故事。
			如果你能做到的话，我会听你的劝告加入比奇商会的。
			
			[嗯，好的！:107]"""
	elif (Menu == 107):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==64):
			PlayerSetV(Sender,BV_NQ_MAIN,65)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """哦？你答应我的请求了？
				好！那我等着你的好消息！
				
				[结束:0]"""
	elif(Menu == 2):
		say = """哦！听说在比奇产生之前，西方的国家为了讨伐某种怪物派种族遣出过远征队，那种怪物是什么种族的呢？
			
			[半兽人和诺玛:21]      [诺玛和内日:21]
			[沃玛和祖玛:21]      [半兽人和内日:20]"""
	elif(Menu == 20):
		say = """噢！原来还是那些家伙啊！
			
			那么在人类来此生活之前的比奇县什么样的地方呢？
			
			[祖玛教主的宫殿:31]      [蛇们的集体栖息地:31]
			[半兽人的领土:3]      [内日族的根据地:31]"""
	elif(Menu == 21):
		say = """那么在人类来此生活之前的比奇县什么样的地方呢？
			
			[祖玛教主的宫殿:31]      [蛇们的集体栖息地:31]
			[半兽人的领土:31]      [内日族的根据地:31]"""
	elif(Menu == 3):
		say = """			那么我们的祖先们回不了故乡，在这个地方落脚定居的原因是什么呢？
			
			[因为发生了大地震:4]      [因为发生了大洪水:41]
			[因为发生了大饥荒:41]      [因为传染病的流行:41]"""
	elif(Menu == 31):
		say = """			那么我们的祖先们回不了故乡，在这个地方落脚定居的原因是什么呢？
			
			[因为发生了大地震:41]      [因为发生了大洪水:41]
			[因为发生了大饥荒:41]      [因为传染病的流行:41]"""
	elif(Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==69):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """怪不得呢……所以越过山脉的路就被隔断了啊！
				你真的是认真努力的调查过啦！托您的福，史书的撰写进度加快了！等这本书全部完成之后一定会在末尾写上你的大名的。
				啊！那么你去把我要加入比奇商会的意思转告给王大人吧！
				
				[结束:0]"""
	elif(Menu == 41):
		say = """奇怪... 根据我的调查好像不是这么回事儿啊！你确定没有听错吗？
			再去打听一下吧！
			
			[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==40):
			say = """唉.. 真是担心啊！论人情吧！又不能把他赶走。要是谁来替我让那个客人走就好了……
				
				[什么事情啊？:100]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==58):
			say = """正所谓书籍是心灵的食粮啊！
				
				[询问:103] 和夜市的商人 老生 有关的问题
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==64):
			say = """很早以前这里就是武林人士聚集的地方。
				呵呵...
				你看起来也像个习武之人，来这里有什么事情吗？
				
				[为了劝说您加入比奇商会而来此的。:104]
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==65):
			say = """你和所有休班卫士进行谈话了吗?
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==66):
			say = """你和所有休班卫士进行谈话了吗?
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==67):
			say = """你看起来还没有听到休班卫士的全部故事啊！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==68):
			say = """没有收集到资历最老的卫士的故事怎么就来了？
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==69):
			say = """你和所有休班卫士进行谈话了吗?
				
				[转达与休班卫士的谈话内容。:2]
				
				[结束:0]"""
		else:
			say = """正所谓书籍是心灵的食粮啊！
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(255,"OnClick",OnClick)
