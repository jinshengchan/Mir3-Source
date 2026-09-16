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
		say = """是上官小姐让你来的吗？
			嗯...... 
			现在最好先从送东西开始做起吧。
			也没什么特别的，就是把这碗肉汤给铁匠铺的德秀送去就行，本来我是想亲自去的，可是现在手头上有点儿忙......
			
			[就交给我吧:801]"""
	elif (Menu == 801):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==1):
			if (Sender.GiveItem('肉汤',1)):
				PlayerSetV(Sender,BV_NQ_MAIN,2)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """那么，趁着没凉之前赶快送过去吧！
				他现在一定饿极了......
				对了，德秀的铁匠铺往右走一点就到了。大概在 <font color=\"0xff00ff00\">459:279</font> 附近！
				
				[结束:0]"""
			else:
				say ="""你的包裹满了，整理下在来。

				[结束:0]"""
	elif (Menu == 802):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==3):
			PlayerSetV(Sender,BV_NQ_MAIN,4)
			Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
			say = """知道的话那就太好了！\
				我在这等你， <font color=\"0xff00ff00\"> 牛肉</font>  就拜托给你了哦！
				
				[结束:0]"""
	elif (Menu == 803):
		if(PlayerGetV(Sender,BV_NQ_MAIN)==4):
			if (Sender.GetItemCount('牛肉') < 1):
				say = """嗯？ 看来这不是 <font color=\"0xff00ff00\"> 牛肉</font>  啊？
					你好象是看错了？
					
					[结束:0]"""
			else:
				Sender.TakeItem('牛肉',1)
				MainQuestRewards(Sender)
				Sender.Connection.ReceiveChat("任务日志更新！", MessageType.System)
				say = """辛苦了！
					多亏了你才满足了回头客儿们的要求。
					这是给你的辛苦费！
					现在没什么事了，再去上官小姐 <font color=\"0xff00ff00\"> (461:257)</font>  那儿看看吧！
					或者还有别的事情要你去做呢！
					
					[结束:0]"""
#主菜单
	else:
		if(PlayerGetV(Sender,BV_NQ_MAIN)==0):
			say = """你是来卖肉的？
				
				[卖:3]肉
				[询问获取肉的途径:2]
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==1):
			say = """你是来卖肉的？
				
				[卖:3]肉
				[询问获取肉的途径:2]
				
				[传达:800] 上官小姐 的话
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==2):
			say = """汤都快要凉了！一直向右走就是德秀的铁匠铺！
				去 <font color=\"0xff00ff00\">459:279</font> 那儿可以找到的！
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==3):
			say = """做的很不错啊！拜托你做其他的事情吧！
				我们店有很多的回头客，他们的食性不是一般的挑剔，不是最好的肉他们连看都不看一眼！
				好肉利润也高，当然不能回绝这样的生意。
				但供应量不足却一直是个问题！要是不能提供足量高质量的肉的话，没准儿什么时候顾客就会被别的店给抢过去！
				所以拜托你帮我找些  <font color=\"0xff00ff00\">牛肉</font>  来。
				嗯，想要听听采集肉的注意事项吗？
				
				[请告诉我吧！:2]
				
				[已经知道了！:802]
				
				[结束:0]"""
		elif(PlayerGetV(Sender,BV_NQ_MAIN)==4):
			say = """哦，找来上等的牛肉吗？
				
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
#商品列表  '商品名称'  商品价格比例,固定格式为float(1.0)比例倍数

NpcEvent.add_listener(120,"OnClick",OnClick)