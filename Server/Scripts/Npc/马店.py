# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import collections
import clr
clr.AddReference("Library")
from Library import *
import NpcEvent
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
		
		[离开:0]"""	
#跳转菜单马匹购买	
	elif (Menu == 1):
		say = """马匹购买信息：
		
			类型：棕马
			金额：500,000 金币
		
			如果你想买这匹马，请 [在这里签字:11]
		
			[返回:99]
			[离开:0]"""	
	elif(Menu == 2):
		say = """马匹购买信息：
		
			类型：白马
			金额：20,000,000 金币
		
			如果你想买这匹马，请 [在这里签字:21]
		
			[返回:99]
			[离开:0]"""
	elif(Menu == 3):
		say = """马匹购买信息：
		
			类型：红马
			金额：100,000,000 金币
		
			如果你想买这匹马，请 [在这里签字:31]
		
			[返回:99]
			[离开:0]"""
	elif(Menu == 4):
		say = """马匹购买信息：
		
			类型：黑马
			金额：600,000,000 金币
		
			如果你想买这匹马，请 [在这里签字:41]
		
			[返回:99]
			[离开:0]"""
	elif(Menu==11):	
		if(Sender.Level < 15):
			say = """我无法卖给你这匹马。
			你还不够强大，当你等级更高的时候再来吧。
		
			[返回:99]
			[离开:0]"""
		elif(Sender.Gold < 500000):
			say = """你买不起这匹马，
			等你有钱了再来吧。
			
			[返回:99]
			[离开:0]"""
		elif(not(Sender.Character.Account.Horse ==HorseType.None)):
			say = """你现在已经有一匹马了。
			如果你想买一匹新马，请卖掉你现有的马。
			
			[返回:99]
			[离开:0]"""
		else:
			SubGold(Sender,500000)			
			GiveHose(Sender,HorseType.Brown)				
			say = """恭喜你买了一匹新马。
			请好好照顾它。
			
			[离开:0]"""
	elif(Menu==21):	
		if(Sender.Level < 42):
			say = """我无法卖给你这匹马。
			你还不够强大，当你等级更高的时候再来吧。
		
			[返回:99]
			[离开:0]"""
		elif(Sender.Gold < 20000000):
			say = """你买不起这匹马，
			等你有钱了再来吧。
			
			[返回:99]
			[离开:0]"""
		elif(not(Sender.Character.Account.Horse ==HorseType.None)):
			say = """你现在已经有一匹马了。
			如果你想买一匹新马，请卖掉你现有的马。
			
			[返回:99]
			[离开:0]"""
		else:
			SubGold(Sender,20000000)			
			GiveHose(Sender,HorseType.White)				
			say = """恭喜你买了一匹新马。
			请好好照顾它。
			
			[离开:0]"""
	elif(Menu==31):	
		if(Sender.Level < 51):
			say = """我无法卖给你这匹马。
			你还不够强大，当你等级更高的时候再来吧。
		
			[返回:99]
			[离开:0]"""
		elif(Sender.Gold < 100000000):
			say = """你买不起这匹马，
			等你有钱了再来吧。
			
			[返回:99]
			[离开:0]"""
		elif(not(Sender.Character.Account.Horse ==HorseType.None)):
			say = """你现在已经有一匹马了。
			如果你想买一匹新马，请卖掉你现有的马。
			
			[返回:99]
			[离开:0]"""
		else:
			SubGold(Sender,100000000)			
			GiveHose(Sender,HorseType.Red)				
			say = """恭喜你买了一匹新马。
			请好好照顾它。
			
			[离开:0]"""
	elif(Menu==41):	
		if(Sender.Level < 75):
			say = """我无法卖给你这匹马。
			你还不够强大，当你等级更高的时候再来吧。
		
			[返回:99]
			[离开:0]"""
		elif(Sender.Gold < 600000000):
			say = """你买不起这匹马，
			等你有钱了再来吧。
			
			[返回:99]
			[离开:0]"""
		elif(not(Sender.Character.Account.Horse ==HorseType.None)):
			say = """你现在已经有一匹马了。
			如果你想买一匹新马，请卖掉你现有的马。
			
			[返回:99]
			[离开:0]"""
		else:
			SubGold(Sender,600000000)			
			GiveHose(Sender,HorseType.Black)				
			say = """恭喜你买了一匹新马。
			请好好照顾它。
			
			[离开:0]"""
#跳转菜单马匹出售			
	elif (Menu == 5):
		say = """看到一匹马将要被主人抛弃，我很难过。
		我的报价如下：
		
		棕马 - 250,000 金币
		白马 - 10,00,000 金币
		红马 - 50,000,000 金币
		黑马 - 300,000,000 金币
		
		[返回:99]
		[卖马:51]
		
		[离开:0]"""			
	elif(Menu == 51):
		horse = Sender.Character.Account.Horse
		if(horse ==HorseType.None):
			say = """你并没有拥有任何马。
			
			[返回:99]
			[离开:0]"""
		elif (horse == HorseType.Brown):
			say = """马匹出售信息：
			
			类型：棕马
			金额：250,000 金币
			
			如果你想卖这匹马，请 [在这里签字:511]
			
			[返回:99]
			[离开:0]"""
		elif(horse == HorseType.White):
			say = """马匹出售信息：
			
			类型：白马
			金额：10,000,000 金币
			
			如果你想卖这匹马，请 [在这里签字:511]
			
			[返回:99]
			[离开:0]"""
		elif(horse == HorseType.Red):
			say = """马匹出售信息：
			
			类型：红马
			金额：50,000,000 金币
			
			如果你想卖这匹马，请 [在这里签字:511]
			
			[返回:99]
			[离开:0]"""	
		elif(horse == HorseType.Black):
			say = """马匹出售信息：
			
			类型：黑马
			金额：300,000,000 金币
			
			如果你想卖这匹马，请 [在这里签字:511]
			
			[返回:99]
			[离开:0]"""				
		else:
			return
#跳转菜单马匹卖出			
	elif(Menu == 511):
		horse = Sender.Character.Account.Horse
		say = """你已经卖了你的马。
			
		[返回:99]
			
		[离开:0]"""
		if(horse ==HorseType.None):
			say = """你并没有拥有任何马。
			
			[返回:99]
			[离开:0]"""
		elif (horse == HorseType.Brown):
			GiveGold(Sender,250000)	
			GiveHose(Sender,HorseType.None)
		elif(horse == HorseType.White):
			GiveGold(Sender,10000000)
			GiveHose(Sender,HorseType.None)
		elif(horse == HorseType.Red):
			GiveGold(Sender,50000000)
			GiveHose(Sender,HorseType.None)
		elif(horse == HorseType.Black):
			GiveGold(Sender,300000000)
			GiveHose(Sender,HorseType.None)
		else: 
			return		
#主菜单
	else:
		say = """欢迎光临比奇马厩。马是高价产品，请慎重选择。
		
			[购买 棕 马（50万金币，需要等级15）:1]
			[购买 白 马（2000万金币，需要等级42）:2]
			[购买 红 马（1亿金币，需要等级51）:3]
			[购买 黑 马（6亿金币，需要等级75）:4]
		
			[卖所拥有的马:5]
			[离开:0]"""
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
	Sender.Character.Account.Horse = type;
	Sender.RemoveMount();
	Sender.RefreshStats();
	if (Sender.Character.Account.Horse != HorseType.None):
		Sender.Mount();
		
#NpcEvent.add_listener(88,"OnClick",OnClick)
#NpcEvent.add_listener(130,"OnClick",OnClick)
	
