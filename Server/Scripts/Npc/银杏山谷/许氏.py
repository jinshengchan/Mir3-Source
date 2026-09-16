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
		
		[结束:0]"""	
#跳转菜单1商品	
	elif (Menu == 1):
		Dict['Goods'] =goods                #定义可购买商品
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.BuySell  #类型为Library.Enums里的买卖类
		say = """高价收购优质肉。
		沾上土或者被火烧过的肉廉价收购。
		
		[返回:5]
		[结束:0]"""	
	elif (Menu == 2):
		say = """可以通过屠宰鸡、鹿、羊、狼等动物获取肉。
		首先抓住那些动物，然后按Alt键，在动物尸体上点击鼠标，
		然后看到切肉的动作，你的包裹里就会出现大块大块的肉。
		要记住越是不愿意被抓住而拼命逃跑的动物品质越好，
		使用魔法抓住的动物品质为0。
		
		[前一步:5]"""
#跳转菜单3卖				
	elif (Menu == 3):
		Dict['Types'] =types		        #定义类别
		Dict['DialogType'] = NPCDialogType.RootSell   #类型为Library.Enums里的卖类
		say = """高价收购优质肉。
		沾上土的或被火烧过的肉廉价收购。
		
		[前一步:99]"""		
	elif (Menu == 800):
		say = """是南宫小姐让你来的吗？
			嗯...... 
			现在最好先从送东西开始做起吧。
			也没什么特别的，就是把这碗肉汤给铁匠师傅送去就行，本来我是想亲自去的，可是现在手头上有点儿忙......
			
			[就交给我吧:801]"""
	elif (Menu == 801):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==11):
			if (Sender.GiveItem("肉汤",1)):
				PlayerSetV(Sender,BV_NQ_MAIN,12)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """那么，趁着没凉之前赶快送过去吧！
				他现在一定饿极了......
				对了，铁匠师傅往右一直走就到了。途中要经过南宫小姐的喷泉池，准确位置可能在    <font color=\"0xff00ff00\">284:197</font> 附近！
			
				[结束:0]"""
			else:
				say ="""你的包裹满了，整理下在来。

				[结束:0]"""
	elif (Menu == 802):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==13):
			PlayerSetV(Sender,BV_NQ_MAIN,14)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """知道的话那就太好了！\
				我在这等你， <font color=\"0xff00ff00\"> 鸡肉</font>  就拜托给你了哦！
				
				[结束:0]"""
	elif (Menu == 803):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==14):
			if (Sender.GetItemCount('鸡肉') < 1):
				say = """嗯？ 看来这不是 <font color=\"0xff00ff00\"> 鸡肉</font>  啊？
				你好象是看错了？
				
				[结束:0]"""
			else:
				Sender.TakeItem('鸡肉',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """辛苦了！
				多亏了你才满足了回头客儿们的要求。
				这是给你的辛苦费！
				现在没什么事了，再去南宫小姐 <font color=\"0xff00ff00\"> (461:257)</font>  那儿看看吧！
				或者还有别的事情要你去做呢！
				
				[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			say = """你是来卖肉的？
				
				[卖:3]肉
				[询问获取肉的途径:2]
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==11):
			say = """你是来卖肉的？
				
				[卖:3]肉
				[询问获取肉的途径:2]
				
				[传达:800] 上官小姐 的话
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==12):
			say = """一直往右走，快点把肉汤送给在铁匠师傅。去 <font color=\"0xff00ff00\">284:197</font>  那儿可以找到的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==13):
			say = """做的很不错啊！拜托你做其他的事情吧！
				是这样的，村中长老的花甲寿筵马上就要到了，饭店准备宴席需要质量最好的鸡肉，可是要一下子弄那么多鸡肉可不是一件容易的事儿啊！
				而且肉这东西是不能保存太长时间的，谁知道会有这样的事而把仓库都堆满呢?
				不管怎么样，现在正为了收集上好的鸡肉忙得团团转，
				所以也希望你能帮我的忙，就是帮我去四处抓鸡 ，采集  <font color=\"0xff00ff00\">鸡肉</font>  给我带过来。
				你想听听是如何捉鸡的吗？
				
				[请告诉我吧！:2]
				
				[已经知道了！:802]
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==14):
			say = """哦，找来上等的鸡肉吗？
				
				[找来了！:803]"""
		else:
			say = """你是来卖肉的？
				
				[卖:3]肉
				[询问获取肉的途径:2]
				
				[结束:0]"""
				
	Dict['Say']=say                         #定义聊天框对话内容
	return Dict
	
#类型为 Library.Enums里的肉类
types =[ItemType.Meat]

NpcEvent.add_listener(135,"OnClick",OnClick)