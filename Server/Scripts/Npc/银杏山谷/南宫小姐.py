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
			say = """好的。首先我会教你做一些简单但值得去做的事情，一边做一边慢慢的熟悉一下道馆内的事情！
				这之前如果有什么不明白的地方，尽管来问吧！
				
				[我要做的事情是什么？:4]
				[魔法师是什么？:31]
				[银杏山谷是个什么样的地方？:32]
				[南宫小姐是做什么事情的人？:33]"""
		else:
			say = """好的。首先我会教你做一些简单但值得去做的事情，一边做一边慢慢的熟悉一下道馆内的事情！
				这之前如果有什么不明白的地方，尽管来问吧！
				
				[魔法师是什么？:31]
				[银杏山谷是个什么样的地方？:32]
				[南宫小姐是做什么事情的人？:33]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			PlayerSetV(Sender,BV_NQ_MAIN,11)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """这个, 嗯…… 详细的情况请到收罗杂货的 
				从这往左走就可以找到肉店了。
				肉铺店主人是个叫 许氏 的人，现在可能在 228:194 附近，去那儿和她聊聊吧！
				
				[结束:0]"""
	elif (Menu == 5):
		if (Sender.Level < 3):
			say = """下次交给你做的事可能有点难，
				修炼到了3级再来吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==15):
			say = """现在你的实力也有大有所增了啊！
				所以现在要慢慢脱离银杏山谷，把视野放到更加宽广的地方去才行！
				从这儿通过西方的通路  <font color=\"0xff00ff00\">（29:452）</font>  到达比奇县后，就可以找到首都比奇省。
				那里是政治、经济、文化的中心地。也是想要成为魔法师一定要去的地方。
				正好我有样东西要送到比奇省去，这件事就拜托给你去办吧！ 
				
				[明白了:6]"""
	elif (Menu == 6):
		if (Sender.GiveItem('古籍',1)):
			PlayerSetV(Sender,BV_NQ_MAIN,16)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """往比奇省西南方向走就能找到一个叫做  <font color=\"0xff00ff00\">王大人</font>  的人了。
			准确位置在比奇县  <font color=\"0xff00ff00\">389:396</font>  。
			到他那儿以后把这本书转交给他，他会给你报酬的。
			从这儿通过村子西部的通路  <font color=\"0xff00ff00\">（563:68）</font>  到达比奇县后，就可以找到首都比奇省。
			对了，去之前先找一下魔法师高手  <font color=\"0xff00ff00\">霹雳尊者</font>  ，千万别忘了。
			那位先生会喜欢传授给像您这样的魔法师入门者一些基本魔法，只要去了就一定能学到不少东西的！
			听说霹雳尊者住在村子北部山路左边的一棵大树下面。
			具体位置可能在  <font color=\"0xff00ff00\">（265:145）</font>  附近。
			
			[明白了:0]"""
		else:
			say ="""你的包裹满了，整理下在来。

				[结束:0]"""
	elif (Menu == 31):
		say = """法神是可以使用多种强大魔法的人。
			不过相反的是，法神身体很虚弱，所以在战斗的时候要一直十分小心才行。
			仅靠修炼是不能成为法神的，作为法神一定要拥有法神的资质，主要是从血统上来继承这种资质的。
			
			[返回:1]"""
	elif (Menu == 32):
		say = """拥有法神资质的几个家族集中居住的地方就是银杏山谷的起始地。
			此后这里便成了众多法神聚集的名所！
			不过大部分都只是法神的入门者！
			
			[返回:1]"""
	elif (Menu == 33):
		say = """我也是这村中法神家族的一员！
			为了保持为数不多拥有法神血统的法神们之间的同志意识，培养提高法神整体的势力，我在这里帮助像您这样的人能够相对容易的进行修炼！
			
			[返回:1]"""
#主菜单
	else:
		if Sender.Class == Sender.Class.Wizard:
			if(0 < PlayerGetV(Sender,BV_NQ_MAIN) < 15 ):
				say = """
					和肉店<font color=\"0xff00ff00\">  （228:194）  </font>的许氏聊过了吗？
					
					[结束:0]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==15):
				say = """看来在肉店交给你的事情都做完了吧!
					
					[还有别的我能做的事儿吗？:5]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==16):
				say = """去拜访比奇省的王大人，另外还要找一下霹雳尊者。
					在比奇省西南方就可以找到王大人。准确位置在比奇县<font color=\"0xff00ff00\">  （389:396）</font>  。
					通过村子东北部的通路<font color=\"0xff00ff00\">  （563:68）</font>  到达比奇县后，就可以找到首都比奇省。
					比奇省就在比奇县<font color=\"0xff00ff00\">  （480:410）</font>  附近，本来就是个大城，很容易找到的。\
					听说霹雳尊者住在村子北部山路左边的一棵大树下面。
					准确位置可能在<font color=\"0xff00ff00\">  （265:145）</font>  附近。
					
					[结束:0]"""
			else:
				say = """您好！
					如果你还不了解游戏，就让我简单的给你介绍一下吧。
					
					[与南宫小姐探讨自己可做的事情:1]
					
					[结束:0]"""
		elif Sender.Class == Sender.Class.Warrior:
			say = """您好！
				我专门从事帮助那些想成为魔法师的人修炼的工作。
				想成为战士的人还是去 边境城市 修炼比较好。那里也有从事和我一样职业的人。
				
				如果我没记错的话
				要去边境城市应该先穿过村子的西南通路  <font color=\"0xff00ff00\">（29:492）</font>  到比奇县，然后再往西走，就能看到通往边境城市的入口  <font color=\"0xff00ff00\">（333:796）</font>  了。
				
				[结束:0]"""
		elif Sender.Class == Sender.Class.Taoist:
			say = """您好！
				我专门从事帮助那些想成为魔法师的人修炼的工作。\
				想成为道士的人还是去 道馆 修炼比较好。那里也有从事和我一样职业的人。
				
				如果我没记错的话
				要去道馆应该先穿过村子的西南通路  <font color=\"0xff00ff00\">（29:492）</font>  到比奇县，然后再往东北方向走，就能看到去往道馆的入口  <font color=\"0xff00ff00\">（209:49）</font>  了。
				
				[结束:0]"""
		else:
			say = """......
				
				[结束:0]"""


	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(244,"OnClick",OnClick)
