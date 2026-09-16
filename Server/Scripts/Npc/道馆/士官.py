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
#跳转菜单1
	elif (Menu == 1):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			say = """那么，首先我会教你做一些简单但值得去做的事情，一边做一边慢慢的熟悉一下这个边境城市。\
			啊，这之前如果有什么不明白的地方，尽管来问吧！
			
			[我要做的事情是什么？:4]
			[道士是什么？:31]
			[道馆是个什么样的地方？:32]
			[士官是做什么的人？:33]"""
		else:
			say = """贫道想要说的话只有这个。
				“道”是无处不在的。 要牢牢的铭记这句话。
				
				[结束:0]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			PlayerSetV(Sender,BV_NQ_MAIN,21)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """这个, 嗯…… 详细的情况请到收罗杂货的  <font color=\"0xff00ff00\">大老板</font>  道友那儿打听吧。
				大老板道友就在道馆内。从这往下走，在右侧可以看到杂货店，进去就可以见到他了。 
				杂货店入口的大概位置在  <font color=\"0xff00ff00\">（394 : 169）</font>  ， 请参考一下吧！
				
				[结束:0]"""
	elif (Menu == 5):
		if (Sender.Level < 3):
			say = """现在没有什么合适的任务交给施主做呀！
			请级别高一点，修练到3级以上再来吧！
			祝您好运嗷！
			
			[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==25):
			say = """施主的实力真是大有所增啊！
				现在你需要摆脱道馆的周围，将视野放到更宽广的地方去才行。
				首先从这里通过东南方的通路  <font color=\"0xff00ff00\">（516:580）</font>  到达比奇县后，就可以找到首都比奇省。
				那里是政治、经济、文化的中心地。想修炼成为道士，一定要了解人间苦暖才行，所以这是个必须去的地方！
				正好贫道有一样东西要送到比奇省，这件事情就拜托给你吧！ 
				
				[明白了:6]"""
	elif (Menu == 6):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==25):
			if (Sender.GiveItem('古籍',1)):
				PlayerSetV(Sender,BV_NQ_MAIN,26)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """往比奇省西南方向走就能找到一个叫做  <font color=\"0xff00ff00\">王大人</font>  的人了。
				准确位置在比奇县  <font color=\"0xff00ff00\">389:396</font>  。
				找到他，然后把这本书转交给他，他自然会支付给你报酬。
				从这儿通过东南部的通路  <font color=\"0xff00ff00\">（563:68）</font>  到达比奇县后，就可以找到首都比奇省。
				对了，去之前先找一下道士高手  <font color=\"0xff00ff00\">清明子</font>  。
				这位高手能给像施主这样的道士入门者传授一些基本的魔法，施主一定会有所收获的。
				清明子就在本馆内。从本馆左边往上走就可以找到了。准确位置在  <font color=\"0xff00ff00\">（429:96）</font>  。
				
				[明白了:0]"""
			else:
				say ="""你的包裹满了，整理下在来。
				
				[结束:0]"""
	elif (Menu == 31):
		say = """所谓道士就是每天努力洗脱罪过，修身养性，救济人间的人。
			我们遵从上仙药手的教诲，追求的是进入一个陌生之地潜心修炼以达到长生不老，得道成仙的目的。
			另外，我们还会帮助与怪物战斗的武士，道士的治愈术和防御术对在与怪物战斗中的武士是非常有用的。
			
			主动直接与敌人交手违背了我们上仙药手的教诲。因此在战斗中我们主要采取防御保护的方式。
			
			[返回:1]"""
	elif (Menu == 32):
		say = """这道馆在很久以前建成至今，有无数的道士都已经修道祭天了！
			虽然我们无法得知曾经有多少得道成仙的道人，但是现任馆主波观昊道长的道力却是非常高深莫测的！
			
			[返回:1]"""
	elif (Menu == 33):
		say = """贫道在这里负责为本派门生传道！
			施主既然了解本派的门道，就不必太费神啦！
			
			[返回:1]"""
#主菜单
	else:
		if Sender.Class == Sender.Class.Taoist:
			if(0 < PlayerGetV(Sender,BV_NQ_MAIN) < 25 ):
				say = """和杂货店<font color=\"0xff00ff00\">  （394:169）  </font>的大老板道友聊过了吗?
					
					[结束:0]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==25):
				say = """施主的实力真是大有所增啊！
					
					[还有别的我能做的事儿吗？:5]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==26):
				say = """去见完比奇省的王大人，还要请您去拜访本馆的清明子！
					王大人在比奇省的西南部就可以找到。准确位置在比奇县<font color=\"0xff00ff00\">  （389:396）</font>  。
					通过村子东北部的通路<font color=\"0xff00ff00\">  （563:68）</font>  到达比奇县后，就可以找到首都比奇省。
					比奇省就在比奇县<font color=\"0xff00ff00\">  （480:410）</font>  附近，本来就是个大城，很容易找到的。\
					清明子就在本馆内。从本馆左边往上走就可以找到了。准确位置在<font color=\"0xff00ff00\">  （429:96）</font>  。
					
					[结束:0]"""
			else:
				say = """您好！
					如果你还不了解这个世界，就让贫道简单的给你介绍一下吧。
					
					[与士官探讨自己可做的事情:1]
					
					[结束:0]"""
		elif Sender.Class == Sender.Class.Wizard:
			say = """请问施主是。。。?
				贫道是专门帮助那些想成为道士的年轻修炼者的。
				施主是魔法师， 你还是去 银杏山谷 寻求帮助吧。
				
				如果贫道没记错的话。。
				要去银杏山谷应该先走东南通路  <font color=\"0xff00ff00\">（516:580）</font>  到比奇县，经过比奇省再往东南方向走就能看到通往银杏山谷的入口了  <font color=\"0xff00ff00\">（779:698）</font>  。
				
				[结束:0]"""
		elif Sender.Class == Sender.Class.Warrior:
			say = """请问施主是。。。?
				贫道是专门帮助那些想成为道士的年轻修炼者的。
				施主是战士， 你还是去 边境城市 寻求帮助吧。
				
				如果贫道没记错的话。。
				要去边境城市应该先走东南通路  <font color=\"0xff00ff00\">（516:580）</font>  到比奇县，经过比奇省再往南走就能看到通往边境城市的入口了  <font color=\"0xff00ff00\">（333:796）</font>  。
				
				[结束:0]"""
		else:
			say = """......
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(245,"OnClick",OnClick)
