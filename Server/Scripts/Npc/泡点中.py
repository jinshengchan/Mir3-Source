# -*- coding: utf-8 -*-
#载入模块SYS
import sys
#引用模块的地址
from Globals import *
import clr
clr.AddReference("Library")
from Library import *
import collections
import NpcEvent
from Npc.商店列表 import *
from Player.泡点 import *
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
	
	guild = SEnvir.GetGuildFromCastleName("沙巴克")
	
#红名判断	
	if(Sender.Stats[Stat.PKPoint] > 199):
		say = """我不愿意和你这样的人进行交易。
		
		[结束:0]"""	
	elif (Menu == 1):
		StartPaoDian(Sender)
		say = """已开启泡点。
		
		[结束:0]"""	
	elif (Menu == 2):
		StartPaoDian(Sender)
		say = """已结束泡点。
		
		[结束:0]"""		
	elif (Menu == 3):
		StopPaoDian(Sender)
		say = """关闭泡点。
		
		[结束:0]"""	

#主菜单
	else:
		if not guild:
			say = """在线泡点
			泡点说明：只能在道馆的安全区泡点哦！！！
			
	1-10级       扣除0金币                      100000经验/60秒 
	11-21级     扣除10000金币             500000经验/300秒 
	22-29级     扣除50000金币             11000000经验/600秒 
	30-34级     扣除2000000金币         2200000经验/600秒 
	35-39级     扣除2000000金币         3300000经验/600秒 
	40-44级     扣除2000000金币         6000000经验/600秒 
	45-47级     扣除2000000金币         8000000经验/600秒 
	48-51级     扣除2000000金币         12000000经验/600秒 
	52-57级     扣除2000000金币         15000000经验/600秒 
	58-64级     扣除2000000金币         20000000经验/600秒 
	65-70级     扣除2000000金币         25000000经验/600秒 
	71-75级     扣除2000000金币         30000000经验/600秒 
	76-80级     扣除2000000金币         35000000经验/600秒 
	81-999级   扣除2000000金币         40000000经验/600秒 
	
			
			[开启泡点:1]      [结束泡点:3]
			
			
			
			[结束:0]欢迎加入玩家QQ群：739812701"""
		else:
			owner = SEnvir.GetGuildLeader(guild.GuildName)
			say = """这里是<font color=\"0xff00ff00\">沙巴克城</font><font color=\"0xffffff00\">{}</font>行会的领地。
			泡点说明：只能在道馆的安全区泡点哦！！！
			
			[开启泡点:1]      [结束泡点:2]
			
			
			
			[结束:0]""".format(guild.GuildName)

	Dict['Say']=say                         #定义聊天框对话内容
	return Dict

NpcEvent.add_listener(66,"OnClick",OnClick)