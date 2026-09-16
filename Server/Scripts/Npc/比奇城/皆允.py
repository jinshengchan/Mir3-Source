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
			say = """那么，首先我会教你做一些简单但值得去做的事情，一边做一边慢慢的熟悉一下比奇城。\
				啊，这之前如果有什么不明白的地方，尽管来问吧！
				
				[我要做的事情是什么？:4]
				[刺客是什么？:31]
				[比奇县是个什么样的地方？:32]
				[皆允是做什么的人？:33]"""
		else:
			say = """看来你已经不再需要我的帮助啦！
				
				[结束:0]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			PlayerSetV(Sender,BV_NQ_MAIN,31)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """这个，嗯......请去肉店打听一下具体的情况吧！
				从这往左向下走就可以找到肉店了。
				肉店主人是个叫 肉店金氏 的大叔，现在可能在 446:405 附近，去和他聊聊吧！
				
				[结束:0]"""
	elif (Menu == 5):
		if (Sender.Level < 6):
			say = """下次交给你做的事可能有点难，
				修炼到了6级再来吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==35):
			say = """现在你的实力也有大有所增了啊！
				所以现在要把视野放到更加宽广的地方去才行！
				正好我有样东西要送给王大人，这件事就拜托给你去办吧！ 
				
				[明白了:6]"""
	elif (Menu == 6):
		Sender.GiveItem('古籍',1)
		PlayerSetV(Sender,BV_NQ_MAIN,36)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """往比奇城西南方向走就能找到一个叫做  <font color=\"0xff00ff00\">王大人</font>  的人了。
			准确位置在比奇县  <font color=\"0xff00ff00\">389:396</font>  。
			到他那儿以后把这本书转交给他，他会给你报酬的。
			对了，去之前先找一下刺客高手  <font color=\"0xff00ff00\">导师</font>  ，千万别忘了。
			导师会传授给像您这样的刺客入门者一些基本武功，只要去了就一定能学到不少东西的！
			导师就在我们的密室<font color=\"0xff00ff00\">  （451:304）</font>  大厅里。
			
			[明白了:0]"""
	elif (Menu == 31):
		say = """所谓刺客就是依靠偷袭、刺杀来完成任务的人。
			完成刺杀任务需要极强的爆发力和敏捷，能成为刺客大师的人，可是万里挑一啊。
			
			[返回:1]"""
	elif (Menu == 32):
		say = """比奇县是全国的政治、经济、文化的中心地，这里有许多达官显贵，自然有着各种各样的需求。
			古时候，许多亡命之徒通过接受暗杀任务来养家糊口，久而久之这里就成了我们的聚集地。
			
			[返回:1]"""
	elif (Menu == 33):
		say = """为了吸纳更多的优秀人才，组织上特意派我在此引导像你这样的可造之材加入我们。
			
			[返回:1]"""
#主菜单
	else:
		if Sender.Class == Sender.Class.Assassin:
			if(0 < PlayerGetV(Sender,BV_NQ_MAIN) < 35 ):
				say = """和肉店金氏<font color=\"0xff00ff00\">  （448:405）  </font>聊过了吗？
					
					[结束:0]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==35):
				say = """看来在肉店交给你的事情都做完了吧!
					
					[还有别的我能做的事儿吗？:5]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==36):
				say = """去拜访比奇省的王大人,在去之前请先去拜访一下导师。
					在比奇省西南方就可以找到王大人。准确位置在比奇县<font color=\"0xff00ff00\">  （389:396）</font>  。
					
					导师就在我们的密室<font color=\"0xff00ff00\">  （451:304）</font>  大厅里。
					
					[结束:0]"""
			else:
				say = """您好！
					如果你还不了解游戏，就让我简单的给你介绍一下吧。
					
					[与皆允探讨自己可做的事情:1]
					
					[结束:0]"""
		elif Sender.Class == Sender.Class.Wizard:
			say = """您好！
				我专门从事帮助那些想成为刺客的人修炼的工作。
				想成为魔法师的人还是去 银杏山谷 修炼比较好。那里也有从事和我一样职业的人。
				
				如果我没记错的话
				从比奇县往东走，就能看到通往银杏山谷的入口  <font color=\"0xff00ff00\">（779:698）</font>  了。
				
				[结束:0]"""
		elif Sender.Class == Sender.Class.Taoist:
			say = """您好！
				我专门从事帮助那些想成为刺客的人修炼的工作。
				想成为道士的人还是去 道馆 修炼比较好。那里也有从事和我一样职业的人。
				
				如果我没记错的话
				从比奇县往东北方向走，就能看到去往道馆的入口  <font color=\"0xff00ff00\">（209:49）</font>  了。
				
				[结束:0]"""
		else:
			say = """您好！
				我专门从事帮助那些想成为刺客的人修炼的工作。
				想成为战士，还是去 边境城市 寻求帮助吧。
				
				如果我没记错的话。。
				从比奇县往南走就能看到通往边境城市的入口了  <font color=\"0xff00ff00\">（333:796）</font>  。
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(248,"OnClick",OnClick)
