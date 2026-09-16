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
		say = """我不愿意和你这样的人进行交易。
			
			[关闭:0]"""
#跳转菜单1
	elif (Menu == 1):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.Storage   #类型为NPCDialogType里的仓库类
		say = """你想寄存什么东西？
			
			[前一步:99]"""
	elif (Menu == 100):
		say = """啊,这位侠客, 拜托您一件事。
			有个客人在我们旅馆白吃白住了一个多月。
			您能不能先替他垫上这笔钱或者干脆帮我把他赶出去呢？
			
			[好的，让我跟他说说吧:101]
			
			[我好想实在是没有这个闲工夫啊！:102]"""
	elif (Menu == 101):
		PlayerSetV(Sender,BV_NQ_MAIN,40)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """那就太谢谢了！
			那个客人白天时一般在酒摊儿附近喝的烂醉！
			
			[结束:0]"""
	elif (Menu == 102):
		say = """是吗? 嗯……这真是郁闷啊，真愁人啊！
			
			[结束:0]"""
	elif (Menu == 103):
		PlayerSetV(Sender,BV_NQ_MAIN,48)
		MainQuestRewards(Sender)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """是吗……那个人要是自觉的话现在应该已经离开旅馆了。那些欠下的住宿费就算了吧！
			
			[结束:0]"""
	elif (Menu == 104):
		if Sender.Gold < 1000:
			say = """嗯…… 真是近来少见的善心人啊。住宿费一共是1000钱。
				
				[下次我来的时候再付给您吧！:105]"""
		else:
			say = """嗯…… 真是近来少见的善心人啊。住宿费一共是1000钱。
				
				[给您:106]"""
	elif (Menu == 105):
		say = """这样啊? 好吧！那么下次再会！
			
			[结束:0]"""
	elif (Menu == 106):
		SubGold(Sender,1000)
		MainQuestRewards(Sender)
		Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
		say = """谢谢啦！还有这个略表一下我的谢意吧！
			
			[结束:0]"""
#主菜单
	else:	
		if(PlayerGetV(Sender,BV_NQ_MAIN)==39):
			say = """唉.. 真是担心啊！论人情吧！又不能把他赶走。要是谁来替我让那个客人走就好了……
				
				[什么事情啊？:100]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==40):
			say = """那么多多拜托您了！去小酒馆附近就能找到那个客人！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==42):
			say = """遇到那个客人了吗？
				
				[已经把话转达给他了。:103]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==43):
			say = """遇到那个客人了吗？
				
				[已经把话跟他转达了。另外欠下的住宿费我来支付吧！:104]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==44):
			say = """嗯…… 真是近来少见的善心人啊。
				
				[结束:104]"""
		else:
			say = """要我帮忙吗？
				
				[存取:1]物品
				
				[结束:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
#类型为 Enums里的普通类
types =[ItemType.Nothing]

NpcEvent.add_listener(78,"OnClick",OnClick)
