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
		say = """让我加入王大人的比奇商会？
			你不知道我已经加入传奇商会了吗？呵呵，不过听说王大人那个人也不错，而且比起传奇商会来说条件也要更好。
			但是不管怎么说都要讲点道义啊，怎么能像手心手背那样说翻就翻呢？
			
			[那就没有别的办法了吗？:2]"""
		
	elif (Menu == 2):
		say = """嗯……
			既然你都这么说了……我倒是有一个建议。
			最近比奇省里流行传染病，配制治疗这种病的药所需的原料毒蛇牙齿非常的紧缺。这种毒蛇牙齿在毒蛇山谷村就有卖的，但是我现在马上要给源源不断而来的病人治病，没有去买药材的时间……
			如果你能够买来足够我们所需的毒蛇牙齿，我就会抛开商人的身份来以医生的角度听从您的劝说。
			
			[好的，没问题:3]
			
			[给我点考虑的时间:21]"""
	elif (Menu == 21):
		say = """明白吗。
			千万不要太拖延而忘了一切啊。
			我们所有人啊！
			
			[结束:0]"""
	elif (Menu == 3):
		if(PlayerGetV(Sender,BV_NQ_MAIN) == 70):
			PlayerSetV(Sender,BV_NQ_MAIN,71)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """从这儿向东北部去就能到达毒蛇山谷，可能去 （643 : 15） 附近就能够找得到。
				穿过毒蛇山谷一直向东走就会达到那个村庄。在那儿找施药商 金中医（334 : 224） 向他购买 毒蛇牙齿 。
				现在患者数量仍然呈增加的趋势，所以还不能推测出以后具体需要多少药材。不管怎么样你都要快去快回。
				
				[结束:0]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==73):
			MainQuestRewards(Sender)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """您为病人们做了一件大好事，所以我会听从你的劝说加入王大人的比奇商会的！
				只好对不起崔大夫了……
				啊！对了，收下这个吧！急匆匆地走了这么远的路累坏了吧！喝了这个可以补充一下元气。
				这是金创药！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==70):
			say = """我现在特别忙，有什么事儿吗？
				
				[我是为了劝说你加入比奇商会而来。:1]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==71):
			say = """如果你能够买来足够我们所需的毒蛇牙齿，我就会抛开商人的身份来以医生的角度听从您的劝说。
				怎么样？
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==72):
			if(Sender.GetItemCount('毒蛇牙齿') < 1):
				say = """啊？怎么回事？
					见了金中医为什么没带回所要的东西？
					情况紧急，要抓紧时间啊！
					
					[结束:0]"""
			else:
				PlayerSetV(Sender,BV_NQ_MAIN,73)
				Sender.TakeItem('毒蛇牙齿',1)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """辛苦你啦！
					多亏了你啊！不会再有因为没能及时用药而丢掉了性命的病人了！
					
					[万幸啊！:4]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==73):
			say = """那么请去和王大人好好说说吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN) > 73):
			say = """托您的福，比奇商会一天天的繁盛了起来。
				
				[结束:0]"""
		else:
			say = """我现在不再制作药了，制作要的话去找隔壁的老黄吧。
				你找我有什么事情吗?
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(250,"OnClick",OnClick)
