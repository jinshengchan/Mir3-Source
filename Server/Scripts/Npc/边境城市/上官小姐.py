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
			say = """那么，首先我会教你做一些简单但值得去做的事情，一边做一边慢慢的熟悉一下这个边境城市。
				啊，这之前如果有什么不明白的地方，尽管来问吧！
				
				[我要做的事情是什么？:4]
				[战士是什么？:31]
				[边境城市是个什么样的地方？:32]
				[上官小姐是做什么的人？:33]"""
		else:
			say = """看来你已经不再需要我的帮助啦！
				
				[结束:0]"""
	elif (Menu == 4):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			PlayerSetV(Sender,BV_NQ_MAIN,1)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """这个，嗯......请去肉店打听一下具体的情况吧！
				从这往左向下走就可以找到肉店了。
				肉铺店主人是个叫 肉店金老板 的大叔，现在可能在 425:274 附近，去和他聊聊吧！
				
				[结束:0]"""
	elif (Menu == 5):
		if (Sender.Level < 3):
			say = """下次交给你做的事可能有点难，
				修炼到了3级再来吧！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==5):
			say = """现在你的实力也有大有所增了啊！
				所以现在要慢慢脱离边境城市，把视野放到更加宽广的地方去才行！
				从这儿通过村子东北部的通路  <font color=\"0xff00ff00\">（563:68）</font>  到达比奇县后，就可以找到首都比奇省。
				那里是政治、经济、文化的中心地。也是想要成为战士一定要去的地方。
				正好我有样东西要送到比奇省去，这件事就拜托给你去办吧！ 
				
				[明白了:6]"""
	elif (Menu == 6):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==5):
			if (Sender.GiveItem('古籍',1)):
				PlayerSetV(Sender,BV_NQ_MAIN,6)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """往比奇省西南方向走就能找到一个叫做  <font color=\"0xff00ff00\">王大人</font>  的人了。
				准确位置在比奇县  <font color=\"0xff00ff00\">389:396</font>  。
				到他那儿以后把这本书转交给他，他会给你报酬的。
				从这儿通过村子东北部的通路  <font color=\"0xff00ff00\">（563:68）</font>  到达比奇县后，就可以找到首都比奇省。
				对了，去之前先找一下战士高手  <font color=\"0xff00ff00\">龙血先生</font>  ，千万别忘了。
				那位先生会喜欢传授给像您这样的战士入门者一些基本武功，只要去了就一定能学到不少东西的！
				龙血先生常常会来欣赏我们村庄右边樱花和瀑布交相映衬的景致，准确位置在  <font color=\"0xff00ff00\">（456:302）</font>  附近。
				
				[明白了:0]"""
			else:
				say ="""你的包裹满了，整理下在来。

				[结束:0]"""
	elif (Menu == 31):
		say = """所谓战士就是依靠体力打仗的人。
			虽然刚开始的时候主要是靠力气，但是进入更高的境界后掌握了内功，就会成为能够灵活自如的运用剑气的武士。
			（不过还是要有力气才行！不是吗？ 呵呵呵......）
			
			[返回:1]"""
	elif (Menu == 32):
		say = """这个地方在建国初期是曾经是国境守备队驻扎的要塞。
			不过以后随着领土的扩张，作为要塞的意义已经慢慢褪色了，现在跟一般的村庄已经没有什么不同的了。
			但由于原来是军队驻扎基地，所以军事文化留下了很浓的痕迹，成为选择了战士之路的人们聚集的场所。
			
			[返回:1]"""
	elif (Menu == 33):
		say = """强悍的战士很多的话就可以与怪物们作战，这对国家是非常有利的。
			我已经和政府签了协议，帮助在这里的战士志愿者成长为优秀的武士。
			
			[返回:1]"""
#主菜单
	else:
		if Sender.Class == Sender.Class.Warrior:
			if(0 < PlayerGetV(Sender,BV_NQ_MAIN) < 5 ):
				say = """和肉店金老板<font color=\"0xff00ff00\">  （425:274）  </font>聊过了吗？
					
					[结束:0]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==5):
				say = """看来在肉店交给你的事情都做完了吧!
					
					[还有别的我能做的事儿吗？:5]"""
			elif(PlayerGetV(Sender,BV_NQ_MAIN)==6):
				say = """去拜访比奇省的王大人,在去之前请先去拜访一下龙血先生。
					在比奇省西南方就可以找到王大人。准确位置在比奇县<font color=\"0xff00ff00\">  （389:396）</font>  。
					通过村子东北部的通路<font color=\"0xff00ff00\">  （563:68）</font>  到达比奇县后，就可以找到首都比奇省。
					比奇省就在比奇县<font color=\"0xff00ff00\">  （480:410）</font>  附近，本来就是个大城，很容易找到的。\
					龙血先生就在我们村子<font color=\"0xff00ff00\">  （456:302）</font>  附近。
					
					[结束:0]"""
			else:
				say = """您好！
					如果你还不了解游戏，就让我简单的给你介绍一下吧。
					
					[与上官小姐探讨自己可做的事情:1]
					
					[结束:0]"""
		elif Sender.Class == Sender.Class.Wizard:
			say = """您好！
				我专门从事帮助那些想成为战士的人修炼的工作。
				想成为魔法师的人还是去 银杏山谷 修炼比较好。那里也有从事和我一样职业的人。
				
				如果我没记错的话
				要去银杏山谷应该先经过村子的东北通路  <font color=\"0xff00ff00\">（563:68）</font>  到比奇县，然后再往东走，就能看到通往银杏山谷的入口  <font color=\"0xff00ff00\">（779:698）</font>  了。
				
				[结束:0]"""
		elif Sender.Class == Sender.Class.Taoist:
			say = """您好！
				我专门从事帮助那些想成为战士的人修炼的工作。\
				想成为道士的人还是去 道馆 修炼比较好。那里也有从事和我一样职业的人。
				
				如果我没记错的话
				要去道馆应该先经过村子的东北通路  <font color=\"0xff00ff00\">（563:68）</font>  到比奇县，然后再往东北方向走，就能看到去往道馆的入口  <font color=\"0xff00ff00\">（209:49）</font>  了。
				
				[结束:0]"""
		else:
			say = """.....
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
NpcEvent.add_listener(243,"OnClick",OnClick)
