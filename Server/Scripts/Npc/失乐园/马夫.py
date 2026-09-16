# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
from Defines import *   #调用变量模块
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
#跳转菜单买马选择
	elif (Menu == 110):
 		say = """欢迎来到我的马厩。
			好马配英雄，马的价位虽然贵，但你值得拥有！
			
			<font color=\"0xff00ff00\">『马匹属性介绍』</font>
            
			赤兔马：舒适+5、负重+300，攻魔道：0-5
					
			[买:1] 非常稀有的赤兔马（9000万金币，需要等级51级）
			[买:2] 非常稀有的赤兔马（5000赞助币）
		
			[卖马:5]
			[关闭:0]"""
#跳转菜单马匹购买
	elif(Menu == 1):
		say = """马匹购买信息：
		
			类型：赤兔马
			金额：90,000,000 金币
		
			如果你想买这匹马，请 [在这里签字:31]
		
			[返回:99]
			[关闭:0]"""
	elif(Menu == 2):
		say = """马匹购买信息：
		
			类型：赤兔马
			金额：5000赞助币
		
			如果你想买这匹马，请 [在这里签字:71]
		
			[返回:99]
			[关闭:0]"""
	elif(Menu == 31):
		if(Sender.Level < 51):
			say = """我无法卖给你这匹马。
			你还不够强大，当你等级更高的时候再来吧。
		
			[返回:99]
			[关闭:0]"""
		elif(Sender.Gold < 90000000):
			say = """你买不起这匹马，
			等你有钱了再来吧。
			
			[返回:99]
			[关闭:0]"""
		elif(not(Sender.Character.Horse ==HorseType.None)):
			say = """你现在已经有一匹马了。
			如果你想买一匹新马，请卖掉你现有的马。
			
			[返回:99]
			[关闭:0]"""
		else:
			SubGold(Sender,90000000)
			GiveHose(Sender,HorseType.Red)
			say = """恭喜你买了一匹新马。
			请好好照顾它。
			
			[关闭:0]"""
	elif(Menu == 71):
		if(Sender.GameGold < 500000):
			say = """你买不起这匹马，
			你的赞助币不足。
			
			[返回:99]
			[关闭:0]"""
		elif(not(Sender.Character.Horse ==HorseType.None)):
			say = """你现在已经有一匹马了。
			如果你想买一匹新马，请卖掉你现有的马。
			
			[返回:99]
			[关闭:0]"""
		else:
			PlayerSetV(Sender,GV_PLAYER_REDHORSE,1)  #赋值红马定义1，代表是元宝购买的
			SubGameGold(Sender,5000)
			GiveHose(Sender,HorseType.Red)
			say = """恭喜你买了一匹新马。
			请好好照顾它。
			
			[关闭:0]"""
#跳转菜单马匹出售			
	elif (Menu == 5):
		say = """看到一匹马将要被主人抛弃，我很难过。
		我的报价如下：
		
		赤兔马 - 45,000,000 金币
		稀有赤兔马 - 2,500 元宝
		
		[返回:99]
		[卖马:51]
		
		[关闭:0]"""
	elif(Menu == 51):
		horse = Sender.Character.Horse
		if(horse ==HorseType.None):
			say = """我没办法从你那买马。
			你目前一匹马也没有。
			
			[返回:99]
			[关闭:0]"""
		elif (horse == HorseType.Brown):
			say = """马匹出售信息：
			
			类型：棕马
			金额：250,000 金币
			
			如果你想卖这匹马，请 [在这里签字:511]
			
			[返回:99]
			[关闭:0]"""
		elif(horse == HorseType.White):
			say = """马匹出售信息：
			
			类型：白马
			金额：10,000,000 金币
			
			如果你想卖这匹马，请 [在这里签字:511]
			
			[返回:99]
			[关闭:0]"""
		elif(horse == HorseType.Red):
			if(PlayerGetV(Sender,GV_PLAYER_REDHORSE)==0):        #判断是否金币或者元宝购买，通过变量判断
				say = """马匹出售信息：
				
				类型：赤兔马
				金额：45,000,000 金币
				
				如果你想卖这匹马，请 [在这里签字:511]
				
				[返回:99]
				[关闭:0]"""
			else:
				say = """马匹出售信息：
				
				类型：赤兔马
				金额：2,500 元宝
				
				如果你想卖这匹马，请 [在这里签字:511]
				
				[返回:99]
				[关闭:0]"""
		elif(horse == HorseType.Black):
			if(PlayerGetV(Sender,GV_PLAYER_BLACKHORSE)==0):        #判断是否金币或者元宝购买，通过变量判断
				say = """马匹出售信息：
				
				类型：黑马
				金额：300,000,000 金币
				
				如果你想卖这匹马，请 [在这里签字:511]
				
				[返回:99]
				[关闭:0]"""
				
			else:
				say = """马匹出售信息：
				
				类型：黑马
				金额：5,000 元宝
				
				如果你想卖这匹马，请 [在这里签字:511]
				
				[返回:99]
				[关闭:0]"""
		else:
			return
#跳转菜单马匹卖出			
	elif(Menu == 511):
		horse = Sender.Character.Horse
		say = """你已经卖了你的马。
		即使你给它喂胡萝卜，它不再爱你了。
			
		[返回:99]
			
		[关闭:0]"""
		if(horse ==HorseType.None):
			say = """我没办法从你那买马。
			你目前一匹马也没有。
			
			[返回:99]
			[关闭:0]"""
		elif (horse == HorseType.Brown):
			GiveGold(Sender,250000)	
			GiveHose(Sender,HorseType.None)
		elif(horse == HorseType.White):
			GiveGold(Sender,10000000)
			GiveHose(Sender,HorseType.None)
		elif(horse == HorseType.Red):
			if(PlayerGetV(Sender,GV_PLAYER_REDHORSE)==0):        #判断是否金币或者元宝购买，通过变量判断 
				GiveGold(Sender,45000000)
				GiveHose(Sender,HorseType.None)
			else:
				PlayerSetV(Sender,GV_PLAYER_REDHORSE,0)   #卖马时将变量归0
				GiveGameGold(Sender,2500)
				GiveHose(Sender,HorseType.None)
		elif(horse == HorseType.Black):
			if(PlayerGetV(Sender,GV_PLAYER_BLACKHORSE)==0):        #判断是否金币或者元宝购买，通过变量判断
				GiveGold(Sender,300000000)
				GiveHose(Sender,HorseType.None)
			else:
				PlayerSetV(Sender,GV_PLAYER_BLACKHORSE,0)   #卖马时将变量归0
				GiveGameGold(Sender,5000)
				GiveHose(Sender,HorseType.None)
		else: 
			return
#主菜单
	else:
		say = """欢迎来到我的马厩。
				这里有很多的马可供挑选。
				
				[查看:110] 马厩
				
				[关闭:0]"""

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

#####################################################################
#public enum HorseType : byte
#    {
#        None,       没马
#        Brown,      棕马
#        White,      白马
#        Red,        红马
#        Black,      黑马
#    }
#####################################################################
##卖马判断函数
def GiveHose(Sender,type):
	Sender.Character.Horse = type;
	Sender.RemoveMount();
	Sender.RefreshStats();
	if (Sender.Character.Horse != HorseType.None):
		Sender.Mount();
		
#NpcEvent.add_listener(299,"OnClick",OnClick)
